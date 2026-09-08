---
name: mojopad-research-report
description: "Produce a MojoPad-native, deep-linked research report (a .mojopad wiki) on any topic. Enumerates candidate papers per subtopic with Firecrawl Research / PubMed (verified PMIDs/DOIs), retrieves the full-text PDFs into the wiki's PDF Library, and assembles a navigable wiki that mirrors the Bookends research report: Introduction & Scope, How to Read, per-subtopic source/stance pages with a stance table, a deep-linked scholarly synthesis, a Word-ready Academic Summary, and both a citation-order References page and a chronological References page (Vancouver). Every quote deep-links to the full-text PDF IN MojoPad; where the full text is not in MojoPad it falls back to a PMID / PMC / DOI web link. Defers to the mojopad-wiki skill for the wiki container (page skeleton, link rules, delivery to iCloud + DEVONthink). Use when the user says 'Mojopad Report', 'Mojopad Research Report', or 'run the Mojopad research report'."
---

## Trigger phrases

Invoke this skill when the user says **"Mojopad Report"**, **"Mojopad Research Report"**,
**"run the Mojopad research report"**, or asks for a deep-linked / highlighted research
report, literature review, or evidence synthesis delivered **as a MojoPad `.mojopad` wiki**.
It is the MojoPad sibling of `bookends-research-skill` (Bookends) and
`devonthink-research-report` (DEVONthink HTML). The report content, section set, stance
table, scholarly synthesis, Academic Summary, and Vancouver References are the SAME across
all three — only the STORE and the deep-link scheme change.

---

## Life expectancy baseline (R-SSA-LIFE-EXPECTANCY-BASELINE-01)

If this report states, relies on, or rebuts a **life expectancy** — remaining years,
projected age at death, or the horizon a cost projection runs to — **read
`ssa-life-expectancy/SKILL.md` first.** It is authoritative for the baseline. The short
version: **SSA is always the starting, unadjusted baseline** (not CDC/NCHS, not a
commercial table); **COHORT basis, never period**; the longer cohort figure is intentional,
never "corrected" down; **always state basis AND vintage** with the figure (TR2025 does not
exist — the sequence steps TR2024 → TR2026); never mix age bases. Period tables and the
Alt1/Alt3 low-high range stay available as **labelled** non-defaults.

---

## The container is a MojoPad wiki — defer to `mojopad-wiki` (R-WIKI-DEFER-TO-MOJOPAD-SKILL-01)

The deliverable **is** a MojoPad `.mojopad` wiki, so the **`mojopad-wiki` skill is
authoritative for everything about the container.** Read `mojopad-wiki/SKILL.md` before
creating or editing the wiki, and use its de-identified template at
`mojopad-wiki/templates/evidence-review/` as the starting skeleton. This skill keeps
ownership of its own CONTENT rules (the six format rules, the source-discovery pipeline, the
stance apparatus); `mojopad-wiki` owns:

- the required **page skeleton** — `Home`/`Index`, **`Introduction and Scope`** (with a real
  `Report completed: <D Month YYYY>` line), `How to Read This Report`, the content pages, the
  per-subtopic source/stance pages + stance table, the synthesis pages, the **`Academic
  Summary`** page (R-WIKI-ACADEMIC-SUMMARY-01), `Limitations and Provenance`, a citation-order
  **`References`** page, and a **`References — Chronological`** page (oldest first, last page in
  the wiki);
- **reachability** (R-WIKI-REACHABILITY-01): `homePageId` set to the report's own Home page;
  a **Start here** block on Home linking `[[Introduction and Scope]]`; `wikiWords:false`
  (R-WIKI-NO-WIKIWORDS-01, set in `document.json` before writing content) with `autoLink:true`;
- **what MojoPad's renderer actually preserves and silently drops** (§3a) — markdown tables
  and callouts survive; explicit markdown links on any non-denied scheme survive; **only
  `color` + `background-color` on a span** survive and **all other raw HTML and every HTML
  entity is silently dropped** (write the literal character, e.g. a literal U+00A0 for a
  non-breaking space, never `&nbsp;`); **only `https?://` and `mojopad://` are autolinked**
  (so `x-devonthink-item://` and `bookends://` must be **explicit markdown links**);
- the **status-badge convention** (R-WIKI-STATUS-BADGE-01) — a status value is a filled badge
  `<span style="background-color:#c0392b;color:#ffffff"> Active </span>` with **literal U+00A0**
  padding, never coloured text (colour alone reads as a link);
- MojoPad's **URL-scheme trust handling** (§7): a deny-list plus a per-scheme "Open this link
  in another app?" prompt; on this workstation `trustedLinkSchemes` already contains
  `bookends` and `x-devonthink-item`, and `mojopad`/`https`/`mailto` never prompt;
- **observed-navigation verification of every distinct link — document AND page — before
  shipping**; and the `validate_academic_summary.py` gate;
- **delivery**: build the package **outside** any DEVONthink database, verify it with
  `mojopad-wiki/scripts/validate_mojopad_package.py`, write the iCloud copy under
  `~/Library/Mobile Documents/com~apple~CloudDocs/Mojopad/`, then `import_file` +
  `move_record` + **label 3** + **`" (AI)"`** suffix + verify, superseding (never trashing) any
  prior wiki into a `Temp AI Files` subgroup.

If any rule here and a rule in `mojopad-wiki` appear to conflict, **`mojopad-wiki` wins for
the container; this skill wins for report content.**

---

## DEVONthink delivery — build outside, then import (R-DT-BUILD-THEN-IMPORT-01)

**Never create, write, rename, move or delete a file inside a DEVONthink database package.**
A DEVONthink database is a package (`.dtBase2`, `.dtSparse`, `.dtArchive`), not a folder;
filesystem writes inside it corrupt the database. A `.mojopad` is itself a package
(directory), so build it in `~/Downloads` or a temp dir, then import the finished package
through the connector, set **label 3**, name it with the **`" (AI)"`** suffix, and **verify**
with `get_record_properties` that the record exists in the intended group before reporting
success. **Never trash anything** — superseded originals move to a `Temp AI Files` subgroup.
Confirm the imported record's kind is **"MojoPad Document"** (a directory that lands as a
plain group is a failed import).

---

# MojoPad Research Report

This skill produces a deep-linked MojoPad wiki research report, **parameterized so that only
the RESEARCH TOPIC changes from run to run.** Everything else — the pipeline, the page
skeleton, the link forms — is fixed. The citation pages are titled **"References"** (citation
order) and **"References — Chronological"** (oldest first) and are formatted in **Vancouver**
style.

Every claim in the finished wiki is traceable: each verbatim quotation is a hyperlink that
opens the **full-text PDF in MojoPad's PDF Library at the exact passage** (a `mojopad://` deep
link). Where the full text is not obtainable into MojoPad, the quote/citation falls back to a
**PMID / PMC / DOI web link**. The report fuses a **literature package** (executive summary,
stance table, per-source pages each embedding 1–3 highlighted, deep-linked quotes) with an
**academic narrative synthesis** (a navigable, multi-page argument whose author-date citations
deep-link to their passages), closing with a **Word-ready Academic Summary** and the two
**Vancouver References** pages.

**By default everything is ONE MojoPad wiki.** Only split into separate deliverables if the
user explicitly asks.

## What you can use this for

The topic is the only variable, so this skill works for **any question that has a
literature** — clinical or not. Invoke it as **"Mojopad Research Report on `<your
question>`"**. Same coverage as the Bookends skill: clinical evidence syntheses /
treatment-efficacy reviews, drug/therapy comparisons, prognosis / natural-history /
life-expectancy questions, diagnosis / work-up reviews, complication / adverse-event
profiles, standard-of-care questions, medical-legal / life-care-planning evidence packs,
occupational / aviation / toxicology medicine, and any non-clinical scholarly topic with a
literature. Whatever the question, the deliverable is the same MojoPad wiki.

---

## Configuration

- **Wiki build directory** — build the `.mojopad` package **outside any DEVONthink database**:
  `~/Downloads` or a temp directory. Resolve from `$HOME`; **never hardcode a username or an
  absolute personal path.**
- **iCloud copy** — `~/Library/Mobile Documents/com~apple~CloudDocs/Mojopad/<Wiki Name>.mojopad`
  (create the `Mojopad` folder if missing). This satisfies the standing rule that researched
  results are saved to iCloud. If iCloud Drive is not present at
  `$HOME/Library/Mobile Documents/com~apple~CloudDocs/`, fall back to a documented local
  default and **report the path actually used**. **PHI never goes to iCloud** — for a PHI case,
  keep the wiki only in DEVONthink and skip the iCloud copy.
- **DEVONthink destination** — the group the user names, else a **new subgroup created for the
  topic** (`<Topic> — MojoPad Research Report`) inside the **"Claude Research"** group
  (`x-devonthink-item://4301FD67-5F93-4627-86EC-F01E7EC96C4F`). Never the database root.
- **PDF Library** — the wiki's own **`PDF Library`** collection, into which the full-text PDFs
  are imported (see workflow step 3). This is the wiki's reference store, the MojoPad analogue
  of a Bookends group's attachments or a DEVONthink group's PDFs.

---

## Home is MojoPad (always)

This skill is MojoPad-native. Full-text PDFs live in the wiki's **PDF Library** collection;
deep links are **`mojopad://open?…` links** into those PDFs. Drive MojoPad through its MCP
(`mcp__mojopad__*`) — never through screen automation.

**REQUIRED at runtime:** the MojoPad MCP (`mcp__mojopad__*`) and a literature-search MCP
(Firecrawl Research tools and/or a PubMed MCP) for source discovery. No PDF-highlighting
Python library is required — highlights and page anchors come from MojoPad itself (see step 4).

The bundled `mojopad-wiki` scripts (`validate_mojopad_package.py`,
`validate_academic_summary.py`) and the shared `bookends-research-skill` link validators are
**OPTIONAL developer/QA tooling.** Run each **if the file is present; if it is absent, perform
the equivalent check inline and continue.** A missing validator NEVER blocks a run — it only
downgrades an automated gate to a manual one. All link forms and rules are written out in this
SKILL.md, so it is self-sufficient when only its text is installed (Cowork / Dispatch).

---

## Reading the deep links (MojoPad link scheme + how to follow them)

Every highlighted quote is a `mojopad://` link into the source PDF in the wiki's PDF Library.
The `mojopad://` scheme is autolinked in MojoPad prose and resolves inside the app.

### R-MOJOPAD-DEEPLINK-01 — the link forms (in preference order)

1. **PRIMARY — exact-passage link (Scroll-To-Text-Fragment form).** For an exact-passage jump
   to the highlighted sentence, emit:

   ```
   mojopad://open?doc=<url-encoded absolute .mojopad path>&page=<pageId>#:~:text=<url-encoded verbatim quote>
   ```

   - `doc` = the **URL-encoded absolute filesystem path** to the `.mojopad` package (spaces →
     `%20`, etc.).
   - `page` = the **opaque wiki page id** of the PDF Library page that holds this PDF (the
     `pages/<pageId>.json` basename), kept verbatim — do NOT url-encode it.
   - `#:~:text=` carries the **URL-encoded verbatim quote** (the same sentence that was
     highlighted). Encode with `urllib.parse.quote(quote, safe="")`.

   > **Verification note (fork flagged 2026 authoring).** The `#:~:text=` Scroll-To-Text-Fragment
   > form is the form Richard has identified as the confirmed-working exact-passage link. The
   > repo's sibling `mojopad-pdf-highlights` skill instead documents a **page-level** jump form
   > (item 2 below) and no text-fragment form. **On every run, VERIFY the primary form resolves
   > by observed navigation** (fire it, confirm MojoPad opens that PDF scrolled to the passage).
   > **If the `#:~:text=` form does not scroll to the passage on this MojoPad version, fall back
   > to the page-level form (2) and say so in the report-back.** Do not ship an exact-passage
   > link that has not been observed to work.

2. **FALLBACK — page-level link (documented working form).** If the exact-passage form does not
   resolve, link to the PDF **at its page**:

   ```
   mojopad://open?doc=<url-encoded absolute .mojopad path>&page=<pageId>&frag=page%3D<N>
   ```

   where `<N>` is the highlight's **1-based PDF page number**. `frag` is itself URL-encoded, so
   `page=<N>` becomes `frag=page%3D<N>` (`urllib.parse.quote("page=%d" % N, safe="")`). The
   document-level open (no page anchor) is `mojopad://open?doc=<...>&page=<pageId>`.

3. **WEB FALLBACK — when the full text is NOT in MojoPad.** If a source's full-text PDF could
   not be obtained into the PDF Library (open-access sweep in step 3 came up empty), link the
   quote/citation to the paper on the **web**, in priority order: **DOI → `https://doi.org/<doi>`**,
   else **PMID → `https://pubmed.ncbi.nlm.nih.gov/<pmid>/`**, else **PMC →
   `https://pmc.ncbi.nlm.nih.gov/articles/<PMCID>/`**, else the stored publisher URL. Flag the
   source **abstract-only** in the report and do NOT emit a `mojopad://` link for it. **Never
   fabricate a quote** for a paper whose full text could not be retrieved — drop it and say so.

**Renderer constraints (from `mojopad-wiki` §3a — obey exactly):** write every deep link as an
**explicit markdown link** — `[anchor text](mojopad://…)` — because only `https?://` and
`mojopad://` autolink, and only explicit markdown links carry a custom scheme. Never rely on a
raw `x-devonthink-item://` or `bookends://` autolink. Write literal characters, never HTML
entities (a dropped `&nbsp;` renders as visible `&amp;nbsp;`). The status-badge convention is
the only place raw `<span style>` is used, and only `color`/`background-color` survive.

**The `/selection/` and bare-id forms of `bookends://`, and any fabricated URL, remain BANNED**
here exactly as in the sibling skills — but this skill's citation links are `mojopad://`, so
those Bookends-specific traps do not normally arise.

---

## Interpreting the invocation — parse, then expand

Treat the request as a terse one-liner. **Parse ONE thing: the TOPIC.** Everything else is
fixed.

- **TOPIC / question** — the only variable. If none is given, ask for it (it is the one field
  you cannot guess). Otherwise **do not ask permission to proceed** — run the whole pipeline
  end-to-end, and **deep-link EVERY source** (never stop at a "core" subset, and never ask
  whether to do them all).
- **SOURCE DISCOVERY is Firecrawl-PubMed-first (ROUTINE).** For EVERY report, begin by running
  a Firecrawl Research / PubMed search per subtopic to enumerate candidate peer-reviewed papers
  with **verified PMID / DOI / exact article URL**. THEN retrieve each paper's full-text PDF
  into MojoPad's PDF Library. **SOURCE IS KING:** every citation/URL must be the exact verified
  article link; **NEVER fabricate a quote** for a paper you cannot retrieve.
- **STORAGE** is always the MojoPad wiki (plus the iCloud copy and the DEVONthink import).
- Honor an explicit reference count if given; otherwise target **≥25** quality sources when the
  literature supports it (favor guidelines, systematic reviews, meta-analyses first), and say
  so explicitly if the literature genuinely supports fewer.

---

## Standing rules (honor on every run)

- **Create-new, never-trash.** Never delete or trash any page, PDF, collection, or prior wiki.
  When regenerating, save the new wiki as a new record and supersede the prior one into
  `Temp AI Files` (rename `… — superseded <date>`), never delete it.
- **Label = AI content.** The finished wiki record carries **label 3 / "AI Content"** and the
  **`" (AI)"`** name suffix. **Never tag** the record or add any marker.
- **Deep-link EVERY source.** Every source that has a full-text PDF in the PDF Library gets a
  highlighted, deep-linked quote. Do not sample; do not ask whether to link them all.
- **Never use Sci-Hub** or any pirated / shadow-library mirror. The open-access sweep uses only
  legitimate aggregators (step 3).
- **Idempotent + resumable.** Every step is idempotent — on a transient error retry the failed
  item; never start over and never create duplicates (look a page/PDF up by identifier before
  adding).
- **Escape ONLY at a real HTML boundary.** MojoPad pages hold Markdown (with literal
  characters), not HTML entities — do not HTML-escape page content. Store every name/field as
  the RAW literal.
- **PHI-FREE examples.** Every example in this skill is de-identified. Real case material never
  enters the repo and PHI never goes to iCloud.

---

## The six format rules (canonical — reproduce exactly every run)

The report content MUST follow these six rules exactly — they are the same rules the Bookends
report follows, adapted to the MojoPad medium.

1. **Per-source summaries carry 1–3 highlighted, hyperlinked quotes woven INLINE.** Each
   source's write-up embeds 1–3 exact verbatim quotes from *that* source, each highlighted in
   the PDF (step 4) and rendered as an active `mojopad://` deep link to the exact passage.
   **Weave each quoted phrase directly into the running sentence** — never stack detached
   block-quotes. Applies to BOTH the per-subtopic source pages and the synthesis pages.
2. **In-report source links are NATIVE `mojopad://` links, and every source carries a link.**
   Link every source that is in the PDF Library with a `mojopad://` exact-passage (or
   page-level) deep link. A source not in the PDF Library carries its web citation link
   (DOI → PMID → PMC → URL) and is flagged abstract-only.
3. **Source links are typographically obvious.** Render every link-to-source as an explicit,
   clearly-labeled markdown link; the anchor text of a citation link is the source's title or
   citation, never a bare "link".
4. **Close with a Word-ready "Academic Summary," then a "References" list.** The **Academic
   Summary** page synthesizes ALL positions (supportive, equivocal, not-supportive) in flowing
   scholarly prose, using **in-text author-date citations as PLAIN TEXT — NOT hyperlinks** (so
   it survives a paste into Word), and ends with its own plain-text numbered Vancouver
   `## References`. Then the wiki carries a linked **`References`** page (citation order) AND a
   **`References — Chronological`** page (oldest first, last page in the wiki), both Vancouver.
5. **The narrative synthesis is internally navigable.** Open the synthesis with a short table of
   contents whose items are **internal `[[Page Name]]` wiki links** to the numbered synthesis
   pages/sections. These internal links live only in the synthesis — distinct from the external
   quote deep links (rule 1) and the native source links (rule 2). Do **not** put internal
   links in the Academic Summary or References.
6. **R-MOJOPAD-DUAL-CITE-01 — every References entry carries a web citation link AND, when the
   source is in the PDF Library, a `mojopad://` PDF link.** On the `References` and
   `References — Chronological` pages, render each source as: **(a)** the citation/title
   hyperlinked to the article on the WEB (DOI → PMID → PMC → URL; plain text only if none),
   **plus (b)** a **`Full text in MojoPad`** link → the source's `mojopad://` PDF deep link when
   its PDF is in the PDF Library. A source with no PDF in the library carries only the web link
   and is annotated *full text not in MojoPad — abstract-only* (never a fabricated link). This
   mirrors the Bookends dual-link rule (group + citation) as closely as the MojoPad medium
   allows.

### In-narrative citation style (R-BOOKENDS-NARRATIVE-CITE-STYLE-01 — deferred to)

The in-text citations inside the synthesis pages use **author-date (APA-like) by default**:
`(Jones et al, 2015)` / `(Jones & Smith, 2015)` / `(Jones, 2015)`; multiple works
semicolon-separated; narrative mentions read `"Jones et al (2015) found…"`. **Each in-text
citation on a synthesis page is itself a LIVE `mojopad://` (or web-fallback) deep link** to
that source's passage — a synthesis whose citations are dead text is a FAILED run. The
`numeric-superscript` (AMA) style is available only on explicit request. The **Academic
Summary** page keeps its citations **plain text** (Word-ready); the two linked References pages
do not change with the style.

---

## End-to-end workflow

Do these in order. Idempotent and resumable throughout.

### 1. Create the wiki + derive topic-appropriate subtopics

Create a NEW `.mojopad` package named for the topic (e.g. `<Topic> — MojoPad Research Report`)
in the build directory with `mcp__mojopad__create_wiki`. **Immediately set `"wikiWords": false`
in its `document.json`** (leave `autoLink: true`) per R-WIKI-NO-WIKIWORDS-01 — `create_wiki`
hardcodes `wikiWords:true` and there is no parameter for it. Lay in the `mojopad-wiki`
evidence-review page skeleton (Home/Index, Introduction and Scope, How to Read This Report,
Executive Summary, the content/stance pages, the synthesis pages, Academic Summary, Limitations
and Provenance, References, References — Chronological).

**Derive the subtopics from the topic** — mirror how the literature is actually organized
(typically some mix of Etiology/Pathophysiology, Diagnosis/Assessment, one or more
Treatment/Management buckets, Special populations/subtypes, Prognosis/Outcomes). Aim for ~4–8
subtopics, each with its own `Sources — <Subtopic>` page and a stance column in the stance
table.

### 2. Discover & retrieve authoritative sources — Firecrawl-PubMed discovery (routine), then retrieve

Assemble a stance-balanced set of authoritative sources — **clinical practice guidelines,
systematic reviews / meta-analyses, key primary studies** — spanning supportive, equivocal, and
critical findings. **Target ≥25 references** when that many quality sources exist; favor
reviews, meta-analyses, and guidelines first. Say so explicitly if the literature supports
fewer. Honor an explicit user count.

**Step 0 — ROUTINE Firecrawl-PubMed discovery (FIRST, every run).** Enumerate candidate
literature per subtopic with `mcp__mcp-server-firecrawl__firecrawl_research_search_papers`
(+ `_related_papers`) and/or the PubMed MCP (`search_articles` → `get_article_metadata`). For
each candidate capture its **PMID / DOI / exact article URL** and verify it resolves to the real
article page (never a bare domain or section page). Prefer/defer to the
`firecrawl-research-index` skill for the finding pass. This produces an auditable,
stance-balanced candidate set. **Never fabricate a quote for a paper you cannot retrieve.**

**Retrieve the full text.** For each candidate, obtain the open-access full-text PDF to a file
on disk (outside any database):
- prefer `mcp__DEVONthink__download_pdf_from_doi { doi, contact_email }` or a direct
  open-access PDF fetch;
- run the **open-access aggregator sweep** in order until one serves a real PDF: **Unpaywall →
  OpenAlex → Europe PMC / PMC → Semantic Scholar → CORE → DOAJ → a matching preprint (arXiv /
  bioRxiv / medRxiv / SSRN)**. **Sci-Hub and any pirated mirror are NEVER used.**
- If no full text can be obtained, keep the source as **abstract-only** (web-fallback link,
  step-2 provenance logged) — do not drop it silently and do not fabricate a quote from it.

Log each source's retrieval provenance (which aggregator, or abstract-only) for the step-8
report-back.

### 3. Import the PDFs into the wiki's PDF Library

Canonicalize each PDF's filename first with `mcp__mojopad__read_identifier` (PMID/PMC/DOI →
canonical key + filename), so the files match what MojoPad expects. Import the folder of
full-text PDFs into the wiki's **`PDF Library`** collection with
`mcp__mojopad__import_documents` (PDFs are attached and open in MojoPad's reader; their text
becomes searchable once opened). Record, for each source, the **PDF Library page id (`pageId`)**
and the **package-relative file path** — these are what the `mojopad://` deep link needs
(R-MOJOPAD-DEEPLINK-01). Resolve each PDF's **real published title** (embedded PDF metadata →
first-page title → page title); a `PMC1234567.pdf` filename is not a title. De-duplicate by
identifier before importing so a re-run adds no duplicates.

### 4. One persistent highlight + exact-passage deep link per source

For each source with a PDF in the library, pick a **verbatim, contiguous** key sentence **from
the PDF's own text layer** (read it via MojoPad / the PDF text, not from the abstract webpage —
a sentence copied from the abstract frequently fails to match the PDF's text layer). Write a
persistent highlight over that sentence in the PDF and record its **1-based PDF page number** and
the exact quote text. Then build the source's deep link per R-MOJOPAD-DEEPLINK-01:

- **primary:** the `#:~:text=<url-encoded quote>` exact-passage form;
- **verify by observed navigation** that it scrolls to the passage; **if it does not, fall back**
  to the `&frag=page%3D<N>` page-level form and note it.

**Ensure every in-library source ends with 1–3 highlighted, deep-linked quotes.** If a passage
genuinely cannot be highlighted after retrying with a real sentence from the text layer, **fail
loudly** — flag that source *quote-not-highlightable* in the report and surface it in step 8;
never let a swallowed failure pass as success, and never loosen the match to a paraphrase.

### 5. Sort each source into its subtopic + classify stance

Record each source under its subtopic's `Sources — <Subtopic>` page and give it a stance label
appropriate to the question (for an efficacy review: **Supportive / Equivocal / Not
supportive**), based on what the paper actually concludes, not its title. Keep a running tally
for the stance table. Use the `mojopad-wiki` **status-badge** convention for stance pills
(filled `background-color` badge with literal U+00A0 padding — never coloured text).

### 6. Build the wiki pages (the report body)

Populate the pages so the wiki reads as the SAME report the Bookends skill produces, in this
order:

- **Home / Index** — a Start-here block linking `[[Introduction and Scope]]`, plus a link list
  to every section.
- **Introduction and Scope** — purpose (what it answers / does NOT assert), coverage (subject
  areas + source count), method (stance legend + tally + full-text-vs-abstract split), a real
  **`Report completed: <D Month YYYY>`** line, scope limits, and links to
  `[[How to Read This Report]]` and `[[Limitations and Provenance]]`.
- **How to Read This Report** — 2–4 sentences: the parts under one cover; quotes deep-link to the
  full-text PDF in MojoPad's PDF Library; each source carries a web citation link plus, when in
  the library, a `Full text in MojoPad` link; closes with a Word-ready Academic Summary and two
  Vancouver References pages. Include a short **"How to open the deep links"** note: *each quote
  is a `mojopad://` link that opens the source PDF in MojoPad at the passage; web citation links
  (DOI / PMID / PMC) work anywhere.*
- **Executive Summary** — 4–8 sentence bottom line: what the evidence shows, the stance tally,
  the single most important caveat. A reader can stop here and know the answer.
- **Stance Table — All Sources** — a markdown table: source title (COMPLETE, VERBATIM published
  title — never truncated or ellipsed) as a web link, plus a `Full text in MojoPad` deep link
  when in the library · a DETAILED finding (the specific result + effect size/direction + study
  population + relevance, a full sentence, never a bare statistic) · Journal · Year · Source type
  · Stance badge; with a tally line.
- **`Sources — <Subtopic>` pages** — one entry per paper: the COMPLETE VERBATIM title + stance
  badge, full citation (web link + `Full text in MojoPad` link), a 3–5 sentence factual summary
  with 1–3 HIGHLIGHTED, deep-linked verbatim quotes WOVEN INLINE. Abstract-only sources flagged.
- **`Synthesis — <Theme>` pages** — a navigable multi-page argument opened by a TOC of internal
  `[[Page Name]]` links; EVERY quotation is an inline highlighted `mojopad://` deep link woven
  into the prose; in-text citations are author-date and each is itself a live deep link; a
  reasoned conclusion.
- **Academic Summary** — flowing narrative synthesizing ALL positions with **plain-text**
  `(Author, Year)` citations (no hyperlinks), Word-ready, ending with its own plain-text numbered
  Vancouver `## References`.
- **Limitations and Provenance** — selection, exclusions, known gaps, the retrieval provenance
  tally.
- **References** — citation order, Vancouver, each entry with its web citation link plus a
  `Full text in MojoPad` link when applicable (R-MOJOPAD-DUAL-CITE-01).
- **References — Chronological** — the same entries **oldest first, then first author**, last
  page in the wiki, with the ordering note naming any entry that has no citation link and why.

### 7. Deliver — verify, iCloud, DEVONthink

1. **Gate the package.** Run `mojopad-wiki/scripts/validate_mojopad_package.py <Name>.mojopad`
   (flat `document.json`, `homePageId` resolves and is in `pageOrder`, every page non-empty) and
   `mojopad-wiki/scripts/validate_academic_summary.py --type research` (populated Academic
   Summary, author-date in-text, numbered Vancouver list, every in-text citation has a matching
   reference entry, every numbered reference entry resolves to a legal link). If a script is
   absent, perform the equivalent check by hand. **Do not deliver a wiki that fails a gate.**
2. **Observed-navigation link check (R-WIKI, non-negotiable).** Fire EVERY distinct deep link and
   confirm MojoPad opens the right PDF **and** scrolls to the right passage/page. `probes` must
   equal `distinct links` — no sampling. Re-run after any edit that touches links.
3. **iCloud copy** (non-PHI only) → `~/Library/Mobile Documents/com~apple~CloudDocs/Mojopad/<Name>.mojopad`.
4. **Import into DEVONthink** — `import_file` the package into the destination group (user-named,
   else the new `<Topic>` subgroup under "Claude Research"); it may land at DB root, so follow
   with `move_record` and re-check `location`; set **label 3**, suffix the name **`" (AI)"`**,
   and **verify with `get_record_properties`** that the record exists in the intended group and
   its kind is **"MojoPad Document"**. Supersede any prior wiki into `Temp AI Files` (rename
   `… — superseded <date>`, move — never trash).

### 8. Report back

Give the user: the wiki's name and its DEVONthink location; the iCloud path (or an explicit
statement that no iCloud copy was written because the case is PHI); the stance tally; the
retrieval-source tally (which aggregator per source / abstract-only count); the total number of
quotes highlighted and deep-linked; **and an explicit statement of which `mojopad://` link form
verified as working** (the `#:~:text=` exact-passage form, or the `&frag=page%3D<N>` page-level
fallback) — plus the note that `mojopad://` links resolve only on the Mac that has MojoPad,
while the web citation links work anywhere. Confirm the PDF Library was populated and the page
skeleton verified.

---

## Example output

A representative, **de-identified, zero-PHI** run: *"Is Surgery Effective for Chronic Low Back
Pain?"* — a MojoPad wiki with an Introduction and Scope page (dated), a How to Read page, a
Stance Table — All Sources page, per-subtopic Sources pages whose cards carry inline
highlighted `mojopad://` quotes, a navigable Synthesis, a Word-ready Academic Summary, and both
a citation-order References page and a chronological References page (Vancouver). Every patient
/ case identifier is removed; only published literature and the analytical structure are shown.
Model the look-and-feel on the Bookends skill's
`examples/example-deep-linked-report.html` (also zero-PHI).

---

## Reference

- Container rules, page skeleton, renderer preserve/drop table, status-badge palette,
  `mojopad://` autolinking, delivery, and the validators: **`mojopad-wiki/SKILL.md`**
  (authoritative) and its `templates/evidence-review/` skeleton.
- The exact `mojopad://open?…&frag=page%3D<N>` page-level form and PDF Library JSON schema:
  the sibling **`mojopad-pdf-highlights/SKILL.md`**.
- Report content parity (six format rules, stance table, synthesis, Academic Summary, Vancouver
  References) and the author-date citation style: **`bookends-research-skill/SKILL.md`**.
