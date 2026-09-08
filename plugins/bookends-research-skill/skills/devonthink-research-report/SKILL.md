---
name: devonthink-research-report
description: "Produce a DEVONthink-native, deep-linked research report on any topic: enumerate candidate papers per subtopic with Firecrawl Research / PubMed (verified PMIDs/DOIs), import the full-text PDFs into a DEVONthink group, write a persistent highlight + page-accurate x-devonthink-item:// deep link per source, and assemble ONE combined HTML report saved INTO that same group. The report mirrors the Bookends research report: executive summary, stance / source-type table, per-article cards with inline highlighted deep-linked quotes, a navigable scholarly synthesis, a Word-ready Academic Summary, and Vancouver References. In-report links are native x-devonthink-item:// deep links to the DEVONthink-stored PDFs; where a PDF is not in DEVONthink it falls back to a PMID / PMC / DOI web link; chat-facing links use the klcp.synology.me/dt4links proxy. Use when the user says 'Devonthink Report', 'Devonthink Research Report', or 'run the Devonthink research report'."
---

## Trigger phrases

Invoke this skill when the user says **"Devonthink Report"**, **"Devonthink Research Report"**,
**"run the Devonthink research report"**, or asks for a deep-linked / highlighted research
report, literature review, or evidence synthesis delivered as a **combined HTML report stored
in a DEVONthink group**. It is the DEVONthink sibling of `bookends-research-skill` (Bookends)
and `mojopad-research-report` (MojoPad wiki). The report content — section set, stance table,
scholarly synthesis, Academic Summary, Vancouver References — is the SAME across all three;
only the STORE and the deep-link scheme change.

---

## Life expectancy baseline (R-SSA-LIFE-EXPECTANCY-BASELINE-01)

If this report states, relies on, or rebuts a **life expectancy** — remaining years, projected
age at death, or the horizon a cost projection runs to — **read `ssa-life-expectancy/SKILL.md`
first.** It is authoritative for the baseline. The short version: **SSA is always the starting,
unadjusted baseline** (not CDC/NCHS, not a commercial table); **COHORT basis, never period**;
the longer cohort figure is intentional, never "corrected" down; **always state basis AND
vintage** with the figure (TR2025 does not exist — the sequence steps TR2024 → TR2026); never
mix age bases. Period tables and the Alt1/Alt3 low-high range stay available as **labelled**
non-defaults.

---

## DEVONthink delivery — build outside, then import (R-DT-BUILD-THEN-IMPORT-01)

**Never create, write, rename, move or delete a file inside a DEVONthink database package.** A
DEVONthink database is a package (`.dtBase2`, `.dtSparse`, `.dtArchive`), not a folder;
filesystem writes inside it corrupt the database because DEVONthink's index never learns about
the change. Whenever the destination is a DEVONthink group (a UUID or an `x-devonthink-item://`
link), follow this order:

1. **Build the artifact outside the database** — the session outputs folder, `~/Downloads`, or
   a temp directory.
2. **Import through the connector** — `import_file` for a file on disk (each source PDF), or
   `create_record` for content authored inline (the HTML report), targeting the destination
   group UUID.
3. **Set label 3** ("AI").
4. **Name it with the `" (AI)"` suffix.**
5. **Verify** with `get_record_properties` that the record exists in the intended group before
   reporting success. Do not report success on the strength of the import/create call returning.
6. **Never trash anything.** Superseded originals move to a `Temp AI Files` subgroup.

This rule is stated here because the DEVONthink connector's own instructions carry only the
prohibition, never the positive procedure — and a task session spawned without that connector
receives neither.

---

# DEVONthink Research Report

This skill produces a deep-linked, highlighted DEVONthink research report, **parameterized so
that only the RESEARCH TOPIC changes from run to run.** Everything else — the pipeline, the
report structure, the link forms — is fixed. The citation list at the end is titled
**"References"** and is formatted in **Vancouver** style.

Every claim in the finished report is traceable: each verbatim quotation is a hyperlink that
opens the source PDF **in DEVONthink at the exact highlighted passage** (page-accurate
`x-devonthink-item://` deep link), with a persistent highlight already written into the PDF. The
report fuses a **literature package** (executive summary, stance table, per-article cards each
embedding 1–3 highlighted, deep-linked quotes) with an **academic narrative synthesis** (a
navigable, multi-section argument whose author-date citations deep-link to their highlights),
closing with a **Word-ready Academic Summary** and a **Vancouver References** list.

**By default everything is COMBINED into one HTML document**, saved into the DEVONthink group.
Only split into separate deliverables if the user explicitly asks.

## What you can use this for

The topic is the only variable, so this skill works for **any question that has a literature**
— clinical or not. Invoke it as **"DEVONthink Research Report on `<your question>`"**. Same
coverage as the Bookends skill: clinical evidence syntheses, drug/therapy comparisons,
prognosis / natural-history / life-expectancy questions, diagnosis / work-up reviews,
complication / adverse-event profiles, standard-of-care questions, medical-legal /
life-care-planning evidence packs, occupational / aviation / toxicology medicine, and any
non-clinical scholarly topic with a literature. Whatever the question, the deliverable is the
same combined HTML report stored in DEVONthink.

---

## Configuration

- **Build directory** — build the HTML report and download the source PDFs **outside any
  DEVONthink database**: the session outputs folder, `~/Downloads`, or a temp dir. Resolve from
  `$HOME`; **never hardcode a username or an absolute personal path.**
- **DEVONthink destination group** — the group the user names (or an otherwise-relevant existing
  group that fits), else a **new subgroup created for the topic** — `<Topic> (Deep Link Report)`
  — inside the **"Claude Research"** group
  (`x-devonthink-item://4301FD67-5F93-4627-86EC-F01E7EC96C4F`). **Never the database root.** The
  imported source PDFs and the finished label-3 report all live in this one group.

Both the PDFs (the references) and the report live in the **same** DEVONthink group — that is
the DEVONthink analogue of a Bookends group holding its sources plus a Reports subfolder.

---

## Home is DEVONthink (always)

This skill is DEVONthink-native. Source PDFs live as **records in the destination group**; deep
links are **page-accurate `x-devonthink-item://` links**. Drive DEVONthink through its MCP
(`mcp__DEVONthink__*`) — never through screen automation.

**REQUIRED at runtime:** the DEVONthink MCP (`mcp__DEVONthink__*`); the
`pdf-highlight-and-deep-link` MCP (`mcp__pdf-highlight-and-deep-link__*`) for the persistent
highlight + page-accurate anchor; and a literature-search MCP (Firecrawl Research tools and/or
a PubMed MCP) for source discovery. Plus **Google Chrome** (headless) only if a PDF render of
the HTML is wanted; the primary deliverable is the HTML record itself, so Chrome is optional.

There is **no DEVONthink-side validator script** — the DEVONthink QA is procedural (build-then-
import step 5: verify with `get_record_properties`). The shared link/title/dual-link validators
that ship with `bookends-research-skill` are Bookends-specific and do not apply here. Run any
present tool if it fits; otherwise verify inline. A missing tool NEVER blocks a run.

---

## Reading the deep links (DEVONthink link scheme + how to follow them)

Every highlighted quote is an `x-devonthink-item://` link to its source PDF. The scheme opens
the record in DEVONthink on the Mac.

### R-DT-DEEPLINK-01 — the link forms (in preference order)

1. **PRIMARY — exact-passage / page-anchored link (the report body uses this).** After writing
   the highlight (step 4), emit the exact-passage anchor:

   ```
   x-devonthink-item://<UUID>?page=<0-based page>&annotation=Highlight&x=<x0>&y=<y0>
   ```

   Worked example: `x-devonthink-item://F19E00D2-52B7-4462-8153-9EDDDBC6142B?page=0&annotation=Highlight&x=89&y=388`.

   - `<UUID>` = the DEVONthink record UUID of the source PDF (36 chars).
   - **CRITICAL index convention:** with `&annotation=Highlight`, `page` is **0-BASED** (PDF
     page 1 ⇒ `page=0`). Note the bare `?page=N` `deepLink` that the highlight MCP returns is
     **1-BASED** — the two disagree by one; do **not** conflate them.
   - `x` = `round(rects[0][0])` (left edge of the first highlight rect); `y` =
     `round(rects[0][1])` (top edge). `rects` come back from the highlight MCP.
   - **Inside an HTML attribute the `&` MUST be written `&amp;`**, e.g.
     `href="x-devonthink-item://UUID?page=0&amp;annotation=Highlight&amp;x=89&amp;y=388"`.

   A **search/quote-anchored** form is also valid where an x/y anchor is not available:
   `x-devonthink-item://<UUID>?page=<N>&search=<URL-encoded verbatim quote>`.

2. **DOCUMENT-LEVEL link.** For a "DEVONthink copy" citation link (open the record, no page
   anchor): `x-devonthink-item://<UUID>`.

3. **WEB FALLBACK — when the PDF is NOT in DEVONthink.** If a source's full-text PDF could not
   be obtained into the group (open-access sweep came up empty), link the quote/citation to the
   paper on the **web**, in priority order: **DOI → `https://doi.org/<doi>`**, else **PMID →
   `https://pubmed.ncbi.nlm.nih.gov/<pmid>/`**, else **PMC →
   `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`**, else the stored publisher URL. Flag the
   source **abstract-only** and emit no `x-devonthink-item://` link for it. **Never fabricate a
   quote** for a paper whose full text could not be retrieved — drop it and say so.

### R-DT-CHATLINK-PROXY-01 — chat-facing links use the dt4links proxy (standing rule)

`x-devonthink-item://` is a macOS app scheme: it launches DEVONthink only on the Mac that has
the database. **In-report links stay NATIVE `x-devonthink-item://`** (the report lives in
DEVONthink and opens on the Mac). **But any link Claude puts into the CHAT reply must use the
Synology proxy**, which resolves the UUID to the record over HTTPS:

```
https://klcp.synology.me/dt4links/#<UUID>
```

so a chat citation reads `[<Title>](https://klcp.synology.me/dt4links/#<UUID>)`. **Never paste a
bare `x-devonthink-item://` link into chat**, and **never** rewrite the report body to the proxy
form (the proxy is document-level and drops the page/annotation anchor). Report body = native
`x-devonthink-item://` with the page anchor; chat = the `dt4links` proxy.

---

## Interpreting the invocation — parse, then expand

Treat the request as a terse one-liner. **Parse ONE thing: the TOPIC.** Everything else is
fixed.

- **TOPIC / question** — the only variable. If none is given, ask for it. Otherwise **do not ask
  permission to proceed** — run the whole pipeline end-to-end, and **deep-link EVERY source**
  (never stop at a "core" subset, never ask whether to do them all).
- **DESTINATION** — if the user names a DEVONthink group, use it; otherwise create the new
  `<Topic> (Deep Link Report)` subgroup under "Claude Research".
- **SOURCE DISCOVERY is Firecrawl-PubMed-first (ROUTINE).** For EVERY report, begin by running a
  Firecrawl Research / PubMed search per subtopic to enumerate candidate peer-reviewed papers
  with **verified PMID / DOI / exact article URL**, THEN retrieve each paper's full-text PDF into
  the DEVONthink group. **SOURCE IS KING:** every citation/URL is the exact verified article
  link; **NEVER fabricate a quote** for a paper you cannot retrieve.
- **STORAGE** is always the DEVONthink group (report + PDFs together).
- Honor an explicit reference count if given; otherwise target **≥25** quality sources when the
  literature supports it (favor guidelines, systematic reviews, meta-analyses first), and say so
  explicitly if the literature supports fewer.

---

## Standing rules (honor on every run)

- **Create-new, never-trash.** Never delete or trash any record, PDF, group, or prior report.
  When regenerating, save the new report as a new label-3 record and move the prior one to a
  `Temp AI Files` subgroup (move, never delete).
- **Label = AI content.** The finished report record carries **label 3 / "AI Content"** and the
  **`" (AI)"`** name suffix. **Never tag** the record or add any marker.
- **Deep-link EVERY source.** Every source with a PDF in the group gets a highlighted,
  deep-linked quote. Do not sample; do not ask whether to link them all.
- **Never use Sci-Hub** or any pirated / shadow-library mirror. The open-access sweep uses only
  legitimate aggregators (step 2).
- **Idempotent + resumable.** Every step is idempotent — retry a failed item; never start over
  and never create duplicates (`lookup_records` by name/DOI/filename before importing).
- **Escape ONLY at the HTML boundary.** HTML entity escaping (`&`→`&amp;`, `<`→`&lt;`, etc.) is
  applied only when emitting the HTML report body — never to a DEVONthink record name or field,
  or a filename. Store every such value as the RAW literal and escape a COPY only at render time.
  Include `<meta charset="utf-8">` and emit typographic glyphs as numeric entities so the report
  never shows mojibake.
- **PHI-FREE examples.** Every example in this skill is de-identified. DEVONthink is PHI-safe
  (local, single-user), so real PHI case reports may live in DEVONthink — but this skill's
  repo/examples stay de-identified, and a PHI report is never copied anywhere but DEVONthink.

---

## The six format rules (canonical — reproduce exactly every run)

The report MUST follow these six rules exactly — the same rules the Bookends report follows,
adapted to DEVONthink.

1. **Per-article summaries carry 1–3 highlighted, hyperlinked quotes woven INLINE.** Each
   article's card embeds 1–3 exact verbatim quotes from *that* article, each highlighted in the
   attached PDF (step 4) and rendered as an active hyperlink to the page-accurate
   `x-devonthink-item://` exact-passage anchor. **Weave each quoted phrase directly into the
   running sentence** — never stack detached block-quotes. Applies to BOTH the Part I cards and
   the Part II narrative. Style the span as a highlight (light background) and a bold link.
2. **In-report source links are NATIVE `x-devonthink-item://` links, never the proxy, and every
   source carries a link.** Link every source whose PDF is in the group with the page-anchored
   `x-devonthink-item://` deep link. A source not in the group carries its web citation link
   (DOI → PMID → PMC → URL) and is flagged abstract-only. (Chat replies use the `dt4links`
   proxy — R-DT-CHATLINK-PROXY-01 — but the report BODY stays native.)
3. **Source links are typographically obvious.** Render every link-to-source **bold** and
   visibly link-styled (color + underline), consistently across inline quote links, per-article
   citation links, and the summary table.
4. **Close with a Word-ready "Academic Summary," then a "References" list.** The **Academic
   Summary** synthesizes ALL positions (supportive, equivocal, not-supportive) in flowing
   scholarly prose, using **in-text author-date citations as PLAIN TEXT — NOT hyperlinks** (so
   it survives a paste into Word). Immediately after it, a section titled **`References`** (NOT
   "Works Cited") in **Vancouver** style — numbered, in citation order.
5. **The narrative synthesis is internally navigable.** Open Part II with a short TOC of internal
   `<a href="#sec-N">` links to numbered sections, each with a stable `<h2 id="sec-N">` anchor.
   These `#sec-N` links live only in the narrative — distinct from the external quote deep links
   (rule 1) and the native source links (rule 2). Do **not** put internal section links in the
   Academic Summary or References.
6. **R-DT-DUAL-CITE-01 — every per-source entry carries a web citation link AND, when the PDF is
   in the group, a native `DEVONthink copy` deep link.** In the Summary / source-type table, the
   per-article cards, and the References list, render each source with **(a)** the citation /
   complete verbatim title hyperlinked to the article on the WEB (DOI → PMID → PMC → URL; plain
   text only if none) **plus (b)** a link labeled **`DEVONthink copy`** → the source PDF's
   `x-devonthink-item://<UUID>` record (and, for the quote links specifically, the page-anchored
   exact-passage form). A source with no PDF in the group carries only the web link, annotated
   *full text not in DEVONthink — abstract-only*. This mirrors the Bookends dual-link rule as
   closely as the DEVONthink medium allows.

### In-narrative citation style (R-BOOKENDS-NARRATIVE-CITE-STYLE-01 — deferred to)

In-text citations inside the Part II synthesis use **author-date (APA-like) by default**:
`(Jones et al, 2015)` / `(Jones & Smith, 2015)` / `(Jones, 2015)`; multiple works
semicolon-separated; narrative mentions read `"Jones et al (2015) found…"`. **Each in-text
citation is itself a LIVE hyperlink** to that source's page-accurate `x-devonthink-item://`
exact-passage anchor — a synthesis whose citations are dead text is a FAILED run. The
`numeric-superscript` (AMA) style is available only on explicit request. The **Academic
Summary** keeps its citations **plain text** (Word-ready); the **References** list does not
change with the style — it stays numbered, in citation order.

---

## End-to-end workflow

Do these in order. Idempotent and resumable throughout.

### 1. Create the destination group + derive topic-appropriate subtopics

Resolve the destination group (user-named, else create `<Topic> (Deep Link Report)` under
"Claude Research" with `mcp__DEVONthink__create_group_path`). **Derive the subtopics from the
topic** — mirror how the literature is actually organized (typically some mix of
Etiology/Pathophysiology, Diagnosis/Assessment, one or more Treatment/Management buckets,
Special populations/subtypes, Prognosis/Outcomes). Aim for ~4–8 subtopics; they organize the
stance table and the narrative sections. (DEVONthink keeps the PDFs in the one group; the
subtopic structure lives in the report, not as nested groups, unless the user asks for subgroups.)

### 2. Discover & retrieve authoritative sources — Firecrawl-PubMed discovery (routine), then retrieve

Assemble a stance-balanced set of authoritative sources — **clinical practice guidelines,
systematic reviews / meta-analyses, key primary studies** — spanning supportive, equivocal, and
critical findings. **Target ≥25 references** when that many quality sources exist; favor
reviews, meta-analyses, and guidelines first. Say so explicitly if the literature supports
fewer. Honor an explicit user count.

**Step 0 — ROUTINE Firecrawl-PubMed discovery (FIRST, every run).** Enumerate candidate
literature per subtopic with `mcp__mcp-server-firecrawl__firecrawl_research_search_papers`
(+ `_related_papers`) and/or the PubMed MCP (`search_articles` → `get_article_metadata`). Capture
each candidate's **PMID / DOI / exact article URL** and verify it resolves to the real article
page. Prefer/defer to the `firecrawl-research-index` skill for the finding pass. **Never
fabricate a quote for a paper you cannot retrieve.**

**Retrieve and import each full-text PDF into the group.** For each candidate:
- de-duplicate first with `mcp__DEVONthink__lookup_records` (by name / DOI / filename) so a
  re-run never creates a duplicate;
- prefer `mcp__DEVONthink__download_pdf_from_doi { doi, contact_email, destination: <group UUID> }`
  — it fetches the open-access PDF and imports it into the group in one call;
- else run the **open-access aggregator sweep** in order until one serves a real PDF — **Unpaywall
  → OpenAlex → Europe PMC / PMC → Semantic Scholar → CORE → DOAJ → a matching preprint (arXiv /
  bioRxiv / medRxiv / SSRN)** — download the PDF to disk (outside the database), then
  `mcp__DEVONthink__import_file { path, destination: <group UUID> }`. **Sci-Hub and any pirated
  mirror are NEVER used.**
- record each PDF's returned **UUID** — it is the locator for highlighting and linking;
- if no full text can be obtained, keep the source **abstract-only** (web-fallback link) — do
  not drop it silently and do not fabricate a quote.

Log each source's retrieval provenance for the step-8 report-back.

### 3. Confirm each PDF is the right paper, in the group

Before highlighting, confirm each imported PDF is the correct paper and lives in the destination
group (`get_record_properties`). A wrong-attachment PDF yields a well-formed link that opens the
wrong paper — verify first, highlight second.

### 4. One persistent highlight + page-accurate deep link per source

For each source with a PDF in the group, pick a **verbatim, contiguous** key sentence **from the
PDF's own text layer** (read it via `mcp__DEVONthink__get_record_text` / the highlight MCP's
layout, not from the abstract webpage — an abstract sentence frequently fails to match the PDF
text layer). Then:

```
mcp__pdf-highlight-and-deep-link__pdf_link_for_quote {
  params: { locator: "x-devonthink-item://<UUID>", quote: "<verbatim sentence from the PDF>" }
}
-> { found, deepLink, page (0-based), pageLabel (1-based), matchedText,
     rects ([[x0,y0,x1,y1],…]), highlightCreated, uuid, ... }
```

This writes a persistent `/Highlight` into the PDF (a one-time `.bak` is kept) and returns the
match geometry. **Build the exact-passage anchor yourself** from the return (R-DT-DEEPLINK-01):
`page` (0-based) → `page=`; `round(rects[0][0])` → `x=`; `round(rects[0][1])` → `y=`; assembling
`x-devonthink-item://<UUID>?page=<0-based>&annotation=Highlight&x=<x0>&y=<y0>`. That anchor is
the quote link AND the per-article `DEVONthink copy` (page-anchored) link. After writing
highlights into a PDF inside the `.dtBase2`, re-index it so DEVONthink notices the annotation:
`tell application id "DNtp" to synchronize record (get record with uuid "<UUID>")`.

**If `found:false`**, the quote is wrong or the text layer is justified/spaced oddly — shorten to
a distinctive contiguous sub-fragment, call `mcp__pdf-highlight-and-deep-link__pdf_get_layout` to
place it exactly, or pick another verbatim sentence. **Never** loosen to a paraphrase. Ensure
every in-group source ends with **1–3 highlighted, deep-linked quotes**. If a passage genuinely
cannot be highlighted after retrying, **fail loudly** — flag the source *quote-not-highlightable*
in the report and surface it in step 8; never let a swallowed failure pass as success.

### 5. Classify stance

Give each article a stance label appropriate to the question (for an efficacy review:
**Supportive / Equivocal / Not supportive**), based on what the paper actually concludes, not its
title. Keep a running tally for the stance table.

### 6. Build ONE combined styled HTML report

Assemble a single self-contained HTML document (inline `<style>`, `<meta charset="utf-8">`) with
these sections, in order, applying all six format rules:

```
Header            — title, subtitle, prepared-date, one line on the evidence base, and (near
                    the top) a "Source DEVONthink group" cross-link x-devonthink-item://<group-uuid>.
Executive Summary — up-front bottom line (4–8 sentences): what the evidence shows, the stance
                    tally, the single most important caveat. A reader can stop here.
"How to read"     — 2–4 sentences: three parts under one cover; quotes deep-link to the
                    highlighted passage in the DEVONthink PDF; each source carries a web citation
                    link plus a "DEVONthink copy" link; closes with a Word-ready Academic Summary
                    and a Vancouver References list.
"How to open      — a short callout near the top: each highlighted quote is a native
 the deep links"    x-devonthink-item:// link that opens the source PDF in DEVONthink at the
                    passage on this Mac; web citation links (DOI / PMID / PMC) work anywhere.
PART I — Literature Package
  Introduction    — topic framing + the stance legend.
  Summary / Source-type Table — Article (COMPLETE, VERBATIM published title — never truncated or
                    ellipsed — as a BOLD web link, PLUS a bold "DEVONthink copy" link) · a
                    DETAILED finding (specific result + effect size/direction + population +
                    relevance, a full sentence, never a bare statistic) · Journal · Year · Source
                    type · Stance pill + a tally line.
  Article-by-Article Summaries — one card per paper: the COMPLETE VERBATIM title + stance pill,
                    full citation (BOLD web link + bold "DEVONthink copy" link), a 3–5 sentence
                    factual summary with 1–3 HIGHLIGHTED, deep-linked verbatim quotes WOVEN
                    INLINE. Abstract-only sources flagged.
PART II — Scholarly Synthesis (Deep-Linked)
  Navigable TOC of INTERNAL <a href="#sec-N"> links over numbered sections, each with a stable
  <h2 id="sec-N"> anchor. Then the multi-section narrative: EVERY quotation is an inline
  highlighted span woven into the prose — a BOLD link to its x-devonthink-item:// exact-passage
  anchor, never a detached block-quote. In-text citations are AUTHOR-DATE and EACH ONE IS ITSELF
  A LIVE LINK to that source's exact-passage anchor. A reasoned conclusion.
Academic Summary  — flowing narrative synthesizing ALL positions with in-text (Author, Year)
                    citations as PLAIN TEXT (no hyperlinks); Word-ready Rich Text.
References         — titled "References" (NOT "Works Cited"), VANCOUVER style: numbered, citation
                    order; each entry carries the citation → article web page (DOI → PMID → PMC →
                    URL) PLUS a "DEVONthink copy" link when the PDF is in the group
                    (R-DT-DUAL-CITE-01); plain-text citation only if no DOI/PMID/URL.
Footer            — provenance, non-PHI note, "verify against primary sources", not medical/legal
                    advice.
```

Use colored stance pills and inline highlighted quote spans (light highlight background + bold
link styling). Model the CSS/DOM idioms on `deep-link-report`'s canonical rendered sample
(`examples/ESI-back-pain-combined-deep-linked-report-sample.html`) so the look matches the
Bookends report: serif body; `.wrap{max-width:860px}`; `a.q` highlighted quote span; `a.src`
bold source links; `.pill.s-sup/.s-equ/.s-not` stance pills; `#sec-N` TOC.

### 7. Save the report into DEVONthink

Author the report as HTML **outside** the database, then create it as a record **in the
destination group** with `mcp__DEVONthink__create_record { type: "html", content, destination:
<group UUID>, name: "<Topic> — Combined Deep-Linked Report (AI)" }`. Set **label 3**
(`update_record { uuid, label: 3 }`). **Never tag** it; **never trash** the prior report — move
any prior version to a `Temp AI Files` subgroup. **Verify with `get_record_properties`** that the
record exists in the intended group and renders its content (non-blank) before declaring done.
(A PDF render via headless Chrome is optional and only if the user wants a PDF; the HTML record
is the deliverable.) DEVONthink is PHI-safe, so a PHI report stays here and is not copied
elsewhere.

### 8. Report back

Give the user: the report's **name**; its DEVONthink location and its **native
`x-devonthink-item://` link** — and, because this reply is chat, present that link to the user as
the **`dt4links` proxy form** `https://klcp.synology.me/dt4links/#<report-UUID>`
(R-DT-CHATLINK-PROXY-01), never a bare `x-devonthink-item://` in chat; the stance tally; the
retrieval-source tally (which aggregator per source / abstract-only count); and the total number
of quotes highlighted and deep-linked (cards + narrative). Note that the report's
`x-devonthink-item://` deep links resolve only on the Mac that has DEVONthink, while the web
citation links work anywhere.

---

## Example output

A representative, **de-identified, zero-PHI** run: *"Is Surgery Effective for Chronic Low Back
Pain?"* — a combined HTML report stored in a DEVONthink group alongside its ≥25 imported source
PDFs, with an executive summary, a stance / source-type table, per-article cards whose inline
highlighted quotes are page-accurate `x-devonthink-item://` deep links, a navigable Part II
synthesis whose author-date citations are themselves live deep links, a Word-ready Academic
Summary, and a Vancouver References list. Every patient / case identifier is removed; only
published literature and the analytical structure are shown. Model the look-and-feel on
`deep-link-report/examples/ESI-back-pain-combined-deep-linked-report-sample.html` (zero-PHI).

---

## Reference

- DEVONthink deep-link anchor, the dt4links proxy rule, PDF import, build-then-import, label 3 /
  never-trash, and the report look-and-feel: the sibling **`deep-link-report/SKILL.md`** and its
  `references/devonthink.md`, plus **`dt-to-html/SKILL.md`** §2 (full catalog of DT link forms).
- Report content parity (six format rules, stance table, synthesis, Academic Summary, Vancouver
  References) and the author-date citation style: **`bookends-research-skill/SKILL.md`**.
- The highlight + page-accurate anchor MCP: `mcp__pdf-highlight-and-deep-link__*`
  (`pdf_link_for_quote`, `pdf_create_highlight`, `pdf_get_layout`).
