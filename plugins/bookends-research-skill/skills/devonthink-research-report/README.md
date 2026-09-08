# devonthink-research-report

The **DEVONthink** sibling of `bookends-research-skill` and `mojopad-research-report`.
Produces a deep-linked research report **as one combined HTML document stored in a DEVONthink
group**: candidate papers are enumerated per subtopic with Firecrawl Research / PubMed
(verified PMIDs/DOIs), the full-text PDFs are imported into the same DEVONthink group, a
persistent highlight + page-accurate `x-devonthink-item://` deep link is written per source,
and the report mirrors the Bookends report (executive summary, stance / source-type table,
per-article cards with inline highlighted deep-linked quotes, a navigable scholarly synthesis,
a Word-ready Academic Summary, and Vancouver References).

**Triggers:** "Devonthink Report", "Devonthink Research Report", "run the Devonthink research report".

**Links:** in-report links are native `x-devonthink-item://` page-anchored deep links to the
DEVONthink-stored PDFs; where a PDF is not in DEVONthink they fall back to a PMID / PMC / DOI
web link. **Chat-facing** links use the `https://klcp.synology.me/dt4links/#<UUID>` proxy
(standing rule) — the report body stays native.

Delivery follows R-DT-BUILD-THEN-IMPORT-01 (build outside the `.dtBase2`, import, label 3,
" (AI)" suffix, verify, never trash — supersede to `Temp AI Files`). All examples are
de-identified / PHI-free. See `SKILL.md`.
