#!/usr/bin/env python3
"""fetch_open_fulltext.py — resolve a LEGITIMATE open-access full-text PDF URL
for a DOI, trying several open-access aggregators in a sensible order and
returning the first one that actually serves a PDF.

Richard has NO institutional / EZproxy access and works commercially, so
legitimate open-access aggregators are the realistic way to raise the
full-text hit rate. This script queries ONLY legitimate OA sources.

    *** Sci-Hub and any pirated / shadow-library mirror are NEVER queried and
        are actively blocked (see PIRATE_BLOCKLIST). ***

Source order (each step is skipped gracefully if unconfigured or it errors):
    1. Unpaywall         (needs an email; api.unpaywall.org/v2/{DOI}?email=...)
    2. OpenAlex          (api.openalex.org/works/doi:{DOI})
    3. Europe PMC / PMC  (fullTextUrlList + PMCID -> OA PDF)
    4. Semantic Scholar  (/graph/v1/paper/DOI:{DOI}?fields=openAccessPdf)
    5. CORE              (needs an API key; api.core.ac.uk/v3)
    6. DOAJ              (doaj.org/api/search/articles — OA journals)
    7. Preprints         (arXiv / bioRxiv / medRxiv, when a match exists)

Config (env var, or an untracked KEY=VALUE file
~/.config/bookends-research/oa-fulltext.env — so no secret is committed):
    UNPAYWALL_EMAIL   (alias: OA_EMAIL)   — required for Unpaywall; else skipped
    CORE_API_KEY                          — required for CORE; else skipped
    OA_HTTP_TIMEOUT   (default 20 seconds)

Usage:
    python3 fetch_open_fulltext.py <DOI> [--json] [--no-validate] [--verbose]

Output:
    default : prints the first working OA PDF URL to stdout, exit 0
              exit 3 (nothing found) with no stdout URL
    --json  : prints {"doi","url","source","tried":[{source,status,url}]}

Only the Python standard library is used (no third-party dependencies).
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

CONFIG_FILE = os.path.expanduser("~/.config/bookends-research/oa-fulltext.env")
UA = "bookends-research-skill/oa-fulltext (mailto:%s)"

# Domains we refuse to touch — pirated / shadow libraries. Never queried;
# any candidate URL landing on one of these is discarded.
PIRATE_BLOCKLIST = (
    "sci-hub", "scihub", "libgen", "library.lol", "libgen.is", "libgen.rs",
    "b-ok", "z-lib", "zlibrary", "booksc",
)


def load_config():
    cfg = {}
    if os.path.isfile(CONFIG_FILE):
        try:
            for line in open(CONFIG_FILE, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip()
        except OSError:
            pass
    # environment overrides file
    for k in ("UNPAYWALL_EMAIL", "OA_EMAIL", "CORE_API_KEY", "OA_HTTP_TIMEOUT"):
        if os.environ.get(k):
            cfg[k] = os.environ[k]
    return cfg


CFG = load_config()
EMAIL = CFG.get("UNPAYWALL_EMAIL") or CFG.get("OA_EMAIL") or ""
CORE_KEY = CFG.get("CORE_API_KEY") or ""
try:
    TIMEOUT = float(CFG.get("OA_HTTP_TIMEOUT", "20"))
except ValueError:
    TIMEOUT = 20.0
VERBOSE = False


def log(*a):
    if VERBOSE:
        print(*a, file=sys.stderr)


def is_pirate(url):
    u = (url or "").lower()
    return any(bad in u for bad in PIRATE_BLOCKLIST)


def _get(url, headers=None, accept_json=True):
    hdrs = {"User-Agent": UA % (EMAIL or "anonymous")}
    if accept_json:
        hdrs["Accept"] = "application/json"
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.status, r.read()


def get_json(url, headers=None):
    try:
        status, body = _get(url, headers=headers, accept_json=True)
        if status == 200:
            return json.loads(body.decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001 — degrade gracefully on any error
        log("  json fail", url, e)
    return None


def looks_like_pdf(url):
    """Cheap validation: HEAD/GET and accept application/pdf, or a .pdf URL."""
    if not url or is_pirate(url):
        return False
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": UA % (EMAIL or "anonymous")}, method="HEAD")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            ct = (r.headers.get("Content-Type") or "").lower()
            if "application/pdf" in ct:
                return True
            if r.status == 200 and url.lower().split("?")[0].endswith(".pdf"):
                return True
    except Exception as e:  # HEAD often unsupported; fall through to a ranged GET
        log("  HEAD fail", url, e)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": UA % (EMAIL or "anonymous"),
                          "Range": "bytes=0-1023"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            ct = (r.headers.get("Content-Type") or "").lower()
            head = r.read(5)
            if "application/pdf" in ct or head[:4] == b"%PDF":
                return True
            if r.status in (200, 206) and url.lower().split("?")[0].endswith(".pdf"):
                return True
    except Exception as e:  # noqa: BLE001
        log("  GET fail", url, e)
    return False


# ---- per-source resolvers: each returns a candidate URL string or None ----

def src_unpaywall(doi):
    if not EMAIL:
        return None, "skipped: no UNPAYWALL_EMAIL configured"
    d = get_json("https://api.unpaywall.org/v2/%s?email=%s"
                 % (urllib.parse.quote(doi), urllib.parse.quote(EMAIL)))
    if not d:
        return None, "no data"
    for loc in ([d.get("best_oa_location")] + (d.get("oa_locations") or [])):
        if loc and loc.get("url_for_pdf"):
            return loc["url_for_pdf"], "ok"
    return None, "no oa pdf"


def src_openalex(doi):
    d = get_json("https://api.openalex.org/works/doi:%s"
                 % urllib.parse.quote(doi))
    if not d:
        return None, "no data"
    for loc in ([d.get("best_oa_location"), d.get("primary_location")]
                + (d.get("locations") or [])):
        if loc and loc.get("pdf_url"):
            return loc["pdf_url"], "ok"
    return None, "no oa pdf"


def src_europepmc(doi):
    q = 'DOI:"%s"' % doi
    d = get_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                 "?query=%s&format=json&resultType=core"
                 % urllib.parse.quote(q))
    try:
        res = d["resultList"]["result"][0]
    except Exception:
        return None, "no match"
    for u in (res.get("fullTextUrlList", {}) or {}).get("fullTextUrl", []) or []:
        if (u.get("documentStyle") == "pdf"
                and u.get("availabilityCode") == "OA" and u.get("url")):
            return u["url"], "ok"
    pmcid = res.get("pmcid")
    if pmcid:
        return ("https://www.ebi.ac.uk/europepmc/webservices/rest/%s/"
                "fullTextPDF" % pmcid), "pmc"
    return None, "no oa pdf"


def src_semanticscholar(doi):
    d = get_json("https://api.semanticscholar.org/graph/v1/paper/DOI:%s"
                 "?fields=openAccessPdf" % urllib.parse.quote(doi))
    if d and d.get("openAccessPdf") and d["openAccessPdf"].get("url"):
        return d["openAccessPdf"]["url"], "ok"
    return None, "no oa pdf"


def src_core(doi):
    if not CORE_KEY:
        return None, "skipped: no CORE_API_KEY configured"
    d = get_json("https://api.core.ac.uk/v3/search/works?q=%s&limit=1"
                 % urllib.parse.quote('doi:"%s"' % doi),
                 headers={"Authorization": "Bearer %s" % CORE_KEY})
    try:
        w = d["results"][0]
    except Exception:
        return None, "no match"
    if w.get("downloadUrl"):
        return w["downloadUrl"], "ok"
    return None, "no oa pdf"


def src_doaj(doi):
    d = get_json("https://doaj.org/api/search/articles/doi:%s"
                 % urllib.parse.quote(doi))
    try:
        links = d["results"][0]["bibjson"]["link"]
    except Exception:
        return None, "no match"
    for ln in links:
        if ln.get("type") in ("fulltext", None) and ln.get("url"):
            if ln.get("content_type", "").lower() == "application/pdf" \
               or ln["url"].lower().endswith(".pdf"):
                return ln["url"], "ok"
    # DOAJ often points at an HTML landing page; return it only if it is a PDF
    return None, "no oa pdf"


def src_preprint(doi):
    """Best-effort preprint match. bioRxiv/medRxiv expose a DOI API; arXiv is
    matched only when the DOI itself is an arXiv DOI."""
    low = doi.lower()
    # arXiv DOIs look like 10.48550/arXiv.XXXX
    m = re.search(r'arxiv[./](\d{4}\.\d{4,5})', low)
    if m:
        return "https://arxiv.org/pdf/%s.pdf" % m.group(1), "arxiv"
    for server in ("biorxiv", "medrxiv"):
        d = get_json("https://api.biorxiv.org/details/%s/%s"
                     % (server, urllib.parse.quote(doi)))
        try:
            coll = d["collection"][0]
        except Exception:
            continue
        # bioRxiv/medRxiv canonical PDF URL
        pre_doi = coll.get("doi") or doi
        return ("https://www.%s.org/content/%s.full.pdf"
                % (server, pre_doi)), server
    return None, "no match"


SOURCES = [
    ("unpaywall", src_unpaywall),
    ("openalex", src_openalex),
    ("europepmc", src_europepmc),
    ("semanticscholar", src_semanticscholar),
    ("core", src_core),
    ("doaj", src_doaj),
    ("preprint", src_preprint),
]


def resolve(doi, validate=True):
    tried = []
    for name, fn in SOURCES:
        try:
            url, note = fn(doi)
        except Exception as e:  # noqa: BLE001
            url, note = None, "error: %s" % e
        if url and is_pirate(url):
            url, note = None, "discarded: pirated-domain"
        status = "none"
        if url:
            if not validate or looks_like_pdf(url):
                tried.append({"source": name, "status": "ok", "url": url})
                return url, name, tried
            status = "unverified"
        tried.append({"source": name, "status": note if not url else status,
                      "url": url})
    return None, None, tried


def main(argv):
    global VERBOSE
    args = [a for a in argv[1:]]
    as_json = "--json" in args
    validate = "--no-validate" not in args
    VERBOSE = "--verbose" in args
    pos = [a for a in args if not a.startswith("--")]
    if not pos:
        print("usage: fetch_open_fulltext.py <DOI> [--json] [--no-validate] "
              "[--verbose]", file=sys.stderr)
        return 2
    doi = pos[0].strip()
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi, flags=re.I)
    url, source, tried = resolve(doi, validate=validate)
    if as_json:
        print(json.dumps({"doi": doi, "url": url, "source": source,
                          "tried": tried}, indent=2))
    elif url:
        print(url)
    else:
        print("no legitimate open-access PDF found for %s" % doi,
              file=sys.stderr)
    return 0 if url else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv))
