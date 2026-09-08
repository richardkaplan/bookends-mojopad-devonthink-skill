# mojopad-research-report

The **MojoPad** sibling of `bookends-research-skill` and `devonthink-research-report`.
Produces a deep-linked research report **as a MojoPad `.mojopad` wiki**: candidate papers
are enumerated per subtopic with Firecrawl Research / PubMed (verified PMIDs/DOIs), the
full-text PDFs are imported into the wiki's **PDF Library**, and the wiki mirrors the
Bookends report (Introduction & Scope, How to Read, per-subtopic source/stance pages + a
stance table, a deep-linked scholarly synthesis, a Word-ready Academic Summary, and both a
citation-order and a chronological Vancouver References page).

**Triggers:** "Mojopad Report", "Mojopad Research Report", "run the Mojopad research report".

**Links:** every quote deep-links to the full-text PDF **in MojoPad** via a `mojopad://open?…`
link (primary: the `#:~:text=` exact-passage form, verified per run, with a `&frag=page%3D<N>`
page-level fallback); where the full text is not in MojoPad it falls back to a PMID / PMC / DOI
web link.

The wiki container (page skeleton, renderer rules, delivery to iCloud + DEVONthink) defers to
the **`mojopad-wiki`** skill. All examples are de-identified / PHI-free. See `SKILL.md`.
