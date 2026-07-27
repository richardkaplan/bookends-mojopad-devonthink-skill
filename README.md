# Bookends Research Skill

**You ask a research question. You get back a report in which every quotation is a link
that opens the source PDF in Bookends, scrolled to the exact sentence — already
highlighted.**

This is a *skill* for Claude — an add-on that teaches Claude a specific job. This one's job
is to research a topic and build the evidence trail inside your
[Bookends](https://www.sonnysoftware.com/bookends-for-mac) library: it finds the
literature, files it into a new Bookends group, downloads and attaches the full-text PDFs,
**writes a persistent yellow highlight over the key passage in each PDF**, and then writes
one HTML report whose every quote deep-links back to that highlighted sentence.

You land on the evidence itself, not on a bibliography entry. And the highlights live in
the PDFs in your library — they are still there the next time you open the article, report
or no report.

*New to Claude Cowork and skills? Don't worry — the [Install](#install) section below is
one block of text you copy and paste. Claude does the rest.*

macOS only. Requires Bookends, a paid Mac app. See [Requirements](#requirements).

---

## What a run produces

One combined, styled HTML report, saved into Bookends (as a linked PDF) and to a folder on
disk (as HTML).

**An executive summary with a stance tally** — the bottom line up front, plus how many
sources supported, were equivocal on, or did not support the proposition.

![Report header and executive summary](examples/screenshots/01-executive-summary.png)

**A summary / source-type table** — one row per study: a one-line finding, the journal, the
source type (guideline, RCT, systematic review, cohort…), and a colored stance pill. Each
study name is a deep link.

![Stance and source-type table](examples/screenshots/02-stance-table.png)

**Per-article cards with the quotes woven in** — each card embeds one to three exact
verbatim quotes from that article. Each quote is highlighted in the source PDF and is a
live `bookends://` link to that exact page.

![An article card with a highlighted, deep-linked quote](examples/screenshots/03-article-card.png)

**A Vancouver-style reference list**, numbered in citation order. Every entry carries a web
link (DOI → PubMed → publisher URL) plus links back into Bookends.

![Vancouver references](examples/screenshots/04-references.png)

**And this is where a quote link actually lands** — the source article itself, open in
Bookends at the right page, with the skill's persistent yellow highlight sitting on the
quoted sentence:

![The highlighted passage in the source PDF, opened in Bookends](examples/screenshots/05-pdf-highlight-deeplink.png)

The report also contains a navigable narrative synthesis (an argued, multi-section review
with an internal table of contents) and a plain-text "Academic Summary" section you can
paste straight into Word.

---

## Prerequisites

Installing the plugin is trivial (see [Install](#install)) — it will always add cleanly.
But the plugin only *installs* the skill; whether the skill can actually *run* depends on a
few things being in place on your Mac. **Without the two REQUIRED items below, the skill
installs but cannot produce a report.** None of these is a manual code/`pip` step — they are
apps and connected tools.

This is a **macOS + Bookends** tool. It is not portable to Windows, Linux, Zotero or
Mendeley, and it is not a general-purpose literature search — the deep links are Bookends'
own `bookends://` URL scheme.

**REQUIRED — Bookends 15.4.2 or later, with its built-in MCP server switched on.** Bookends
is a paid Mac app from Sonny Software (~$60; the free demo is capped at 50 references).
Version 15.4.2 introduced Bookends' built-in **MCP server**, which is how Claude drives
Bookends *and* how every highlight and `bookends://` deep link is written and read back —
there is deliberately **no separate PDF-highlighting tool or PDF library** involved. There is
**nothing separate to install** for the MCP; it ships inside Bookends. You just switch it on:
**Bookends → Settings → Servers → MCP Server**. If you are on an older Bookends, upgrade
first; the skill cannot work without it.

**REQUIRED — a literature-search MCP connected to Claude.** The skill discovers candidate
papers and verifies their PMIDs/DOIs before handing them to Bookends to retrieve. A
[Firecrawl](https://firecrawl.dev) MCP server (its research / paper-search tools) or a PubMed
MCP server does the job. Bookends fetches the PDFs; the search tool finds the papers. Without
one of these connected, source discovery will be thin to non-existent.

**REQUIRED — Claude Cowork** (or Dispatch) — the agent mode of the Claude desktop app, which
is where skills and plugins run.

**Recommended (runtime, auto-handled) — Google Chrome.** Almost certainly already on your
Mac. It is used *headlessly* (no window opens, nothing is automated on screen) to render the
finished HTML report into a PDF that keeps its hyperlinks clickable, including the
`bookends://` ones. If Chrome is absent the report still generates as HTML — only the
link-preserving PDF render is skipped, and the run says so.

**Nothing to `pip install`; PyMuPDF is NOT required.** The core flow needs no Python package
at all — highlighting and page-finding go through the Bookends MCP
(`bookends_annotate_pdf` + `bookends_get_pdf_content`), not a PDF library. Two *optional*
pre-ship validators use `pyobjc-framework-Quartz` and `pypdf`, and they **install those
themselves at runtime** the first time they run — there is no manual dependency step, and
none should be added. Every other script is standard-library only. **There is deliberately
no PyMuPDF / `fitz` / `pymupdf` dependency anywhere in this skill — do not add one.**

---

## Install

There is no build step, no configuration file, and **nothing to copy into a skills folder or
`pip install` by hand.** How you install differs slightly by environment, because the
`/plugin marketplace` command exists **only in Claude Code**. In **Cowork** and **Dispatch**
you install by giving Claude the repo URL and asking it to install the skill. Do Step 1
first in every case.

### Step 1 (all environments) — turn on Bookends' MCP server (the one thing Claude can't do for you)

In Bookends: **Settings → Servers → MCP Server**, and switch it on. Bookends will offer to
configure your AI assistant for you (it can auto-configure Claude Desktop, Codex, Cursor and
LM Studio) — accept that. This lives inside Bookends' own preferences, so it's a click you
have to make yourself. It takes about ten seconds. (See [Prerequisites](#prerequisites) for
the literature-search MCP you'll also want connected.)

### Step 2 — install the skill (pick your environment)

#### Claude Code — full plugin (scripts included)

Claude Code has the plugin-marketplace commands. This installs the **whole** plugin — SKILL.md
plus the optional QA scripts and reference doc. Run:

```
/plugin marketplace add richardkaplan/bookends-research-skill
/plugin install bookends-research-skill@bookends-research
```

Two names are involved, and they are **different**: `marketplace add` registers a
**marketplace** named `bookends-research` (that name comes from the repo's `marketplace.json`,
not the repo name), and inside it is a **plugin** named `bookends-research-skill`. That is why
the install target is `bookends-research-skill@bookends-research`. `marketplace add` also
accepts the full URL (`https://github.com/richardkaplan/bookends-research-skill`) instead of
the `owner/repo` shorthand. Once the marketplace is added, the shorter
`/plugin install bookends-research-skill` works too, since the plugin name is unambiguous.
Restart Claude Code and the skill loads as **bookends-research-skill**.

#### Cowork / Dispatch — install from the repo URL

Cowork and Dispatch do **not** have the `/plugin marketplace` command — that is a Claude Code
feature. Install by pasting this:

```
Install the Bookends Research Skill from this public repo:
https://github.com/richardkaplan/bookends-research-skill

Fetch the repo and save its skill — the SKILL.md at
plugins/bookends-research-skill/skills/bookends-research-skill/SKILL.md — as an installed skill.
Then verify Bookends is reachable — list my Bookends libraries and groups as a test —
and show me how to invoke the skill.
```

Cowork / Dispatch fetch the repo and save the skill. **This saves the SKILL.md text only** —
the optional validator scripts and the reference doc do **not** travel with a save-skill
install, and the skill is built to run fine without them: its core work (search → attach →
highlight → deep-link → report) goes entirely through the Bookends MCP. (See *Runtime
requirements & portability* in SKILL.md.) If you want the full bundle including the QA
scripts, install it in **Claude Code** instead.

No environment needs a manual copy into `~/.claude/skills`, a `pip install`, or a Terminal
step.

---

## Using it — worked examples

You invoke the skill by asking for it in plain English. The topic is the only thing you
supply. Any of these openers work:

```
Run the Bookends Research Skill on <your question>
Bookends deep-link report on <your question>
Deep-linked literature review in Bookends on <your question>
```

This is not a medical tool. It works on **any question with a published literature behind
it.** Six examples, across six very different fields:

### 1. Clinical medicine — does the treatment work?

> **Run the Bookends Research Skill on: is surgery effective for chronic low back pain?**

Claude pulls the specialty guidelines, the systematic reviews, and the landmark randomized
trials, then scores each source as supporting, equivocal on, or not supporting the
proposition.

**What lands in Bookends:** a new group *Chronic Low Back Pain — Surgery* with subtopic
folders (fusion, disc replacement, decompression, conservative comparators) and a `Reports`
folder; roughly 15–25 references with their full-text PDFs attached; a yellow highlight
written into each PDF over the sentence carrying that paper's conclusion; and the report
filed in `Reports`. Click a quote in the report and the source article opens at the
highlighted line.

### 2. Pharmacology — two drug classes, head to head

> **Bookends deep-link report on SGLT2 inhibitors versus GLP-1 receptor agonists for renal
> outcomes in type 2 diabetes**

Comparison questions are where the stance table earns its keep: one row per trial, with the
journal, the study design, and a colored pill telling you which way it cut.

**What lands in Bookends:** subtopic folders for each drug class plus one for head-to-head
and network meta-analyses; each outcome trial highlighted at its primary-endpoint sentence,
so a quote link drops you on the actual result rather than the abstract.

### 3. Law and policy — what does the evidence say about the rule?

> **Deep-linked literature review in Bookends on the effect of right-to-repair legislation
> on consumer electronics repair markets**

Law-review articles, regulatory impact assessments, economic evaluations. Sources with no
DOI still work: Bookends takes the citation, the PDF gets attached, the passage gets
highlighted.

**What lands in Bookends:** a group with folders like *Statutory framework*, *Empirical
effects on repair markets*, *Manufacturer objections*; every quoted passage in the report
links to the exact page of the exact filing or article — which is precisely what you want
when someone asks, "where does that claim actually come from?"

### 4. Psychology and social science

> **Run the Bookends Research Skill on: does mindfulness-based stress reduction improve
> outcomes for clinician burnout?**

Meta-analyses, trials, and the methodological critiques of them. The narrative-synthesis
section is where this one shines — it argues the literature rather than listing it, and
every sentence that leans on a study links to that study's highlighted passage.

**What lands in Bookends:** the group, the attached PDFs, the highlights, and the report —
plus a Word-ready "Academic Summary" at the end of the report you can paste straight into a
manuscript.

### 5. Environmental science and engineering

> **Bookends deep-link report on the effectiveness of urban congestion pricing at reducing
> traffic and emissions**

The London, Stockholm, Singapore and Milan evaluations; the modelling papers; the
equity-critique literature.

**What lands in Bookends:** subtopic folders by city and by outcome (congestion, emissions,
equity); a stance table showing at a glance how many evaluations found a durable effect; and
quote links that land on the measured percentages themselves, in the source, on the right
page.

### 6. History and the humanities

> **Deep-linked literature review in Bookends on the historiographical debate over the
> causes of the English enclosure movement**

No trials, no p-values — and it works exactly the same way. The stance column becomes the
interpretive position; the quotes are the passages where each historian actually stakes a
claim.

**What lands in Bookends:** a group organized by school of interpretation, the monographs
and journal articles attached, each highlighted at the point where it commits itself. In
other words, an annotated bibliography in which every quotation is one click from its source
page — the use case this output format was built for.

---

## What actually happens when you run it

You type one sentence. Then, without further prompting, Claude:

1. **Makes a home for the topic in Bookends.** A new group named for your question, with
   subtopic child groups derived from how the literature on that topic actually divides
   itself, plus a `Reports` folder.
2. **Goes and finds the literature.** Guidelines, systematic reviews and meta-analyses,
   landmark primary studies — verifying each one's DOI or PMID rather than trusting a search
   result.
3. **Brings the sources into your library.** Bookends retrieves each reference and downloads
   and attaches its full-text PDF. Where no full text is reachable, the skill attaches a
   rendered abstract page and flags that source as abstract-only, so you are never misled
   about what it actually read.
4. **Highlights the key passage in each PDF.** It finds the sentence carrying that paper's
   contribution and writes a real, persistent highlight over it — in the PDF, in your
   library. It stays there.
5. **Captures a page-accurate link to that highlight**, read back out of Bookends itself.
6. **Files each reference into its subtopic folder** and classifies its stance on your
   question.
7. **Writes the report** — executive summary, stance table, per-article cards, narrative
   synthesis, Vancouver references — renders it to a link-preserving PDF, files that PDF in
   the `Reports` folder, and saves an HTML copy to disk.
8. **Checks every link before it ships.** A report whose deep links don't resolve is treated
   as a failed run, not a delivered one.

**The payoff, in one sentence: you click a claim in the report and you land on the evidence
for it — the actual page of the actual paper, with the sentence already highlighted.**

### Where the output goes

- **Into Bookends** — the report PDF is attached to its own reference in the
  `<Topic> — Reports` subgroup, with the deep-link list in that record's Notes.
- **To disk** — the HTML copy is written to `RESEARCH_DIR`, set near the top of `SKILL.md`.
  It defaults to your iCloud Drive
  (`$HOME/Library/Mobile Documents/com~apple~CloudDocs/Research`), falling back to
  `$HOME/Research`. Change it to anywhere you like; nothing is hardcoded to a particular
  user.

### Following the deep links

`bookends://` links work inside Bookends and from a web browser (the browser hands the
scheme to macOS, which routes it to Bookends). One quirk worth knowing: for a link to be
clickable *inside* a Bookends field, it has to be styled text carrying a live hyperlink — so
paste with a normal **⌘V**, not "Paste and Match Style," which strips the link down to dead
plain text.

---

## Optional: reporting on a DEVONthink group

*This section is only for people who **also use DEVONthink**. It is an optional extra, not a
requirement: the skill's main path needs Bookends and nothing else. It depends on a DEVONthink
MCP server, which is not part of this repo — if you don't have one, skip this section entirely
and nothing else changes.*

If you keep folders of source documents in DEVONthink — papers, reports, filings, primary
sources, whatever you have collected — you can point the skill at a group instead of typing out
a question. In DEVONthink, right-click the group → **Copy Item Link** (you get an
`x-devonthink-item://…` URL) and hand that to Claude.

There are two ways to run it: let Claude work out the questions from the documents, or bring
your own.

### A. Let it work out the questions

You have a folder of material and you want to know what the published literature says about
whatever is actually in it. You don't spell out the topics — Claude reads the documents and
decides what the live questions are.

**A1 — a folder of clinical papers**

> **Here's a DEVONthink group: `x-devonthink-item://<your-group-uuid>`**
> **Run the Bookends Research Skill on it — read the documents, work out the pertinent issues
> they raise, and research those.**

Claude opens the group, reads each document, extracts the questions the collection is really
circling (say: how well blood concentration tracks impairment, whether roadside tests are
valid, what happens in long-term users), and runs the normal pipeline on them.

**A2 — a folder of policy papers** (it is not a medicine-only feature)

> **This DEVONthink group — `x-devonthink-item://<your-group-uuid>` — has the consultation
> responses and impact assessments I've collected on short-term rental regulation. Read them,
> figure out the contested questions, and run the Bookends Research Skill on those.**

Same behavior, different field: Claude works out that the collection is arguing about housing
supply effects, enforcement costs, and displacement, and researches the empirical literature on
each.

### B. Bring your own questions

Same group link, but you already know what you want answered about it. Claude still reads the
documents for context, then researches *your* questions rather than inferring its own.

**B1 — specific questions about a document set**

> **Here's a DEVONthink group: `x-devonthink-item://<your-group-uuid>`. Run the Bookends
> Research Skill on it, focused on these questions: (1) how well does blood concentration
> actually predict impairment? (2) do the roadside screening tests hold up? (3) what does the
> evidence show for long-term daily users?**

**B2 — test a claim the documents make**

> **The documents in `x-devonthink-item://<your-group-uuid>` are the expert reports and filings
> in a matter I'm working on. Run the Bookends Research Skill: what does the peer-reviewed
> literature actually say about the causation theory they rely on, and is the claim that the
> effect persists years after exposure supported?**

Claude reads the documents to ground itself in what they assert, then goes to the literature to
answer exactly what you asked — including, where the evidence points that way, that a claim
isn't supported.

### What you get, either way

The usual Bookends output — a new Bookends group for the topic, the literature retrieved and
filed into subtopic folders, the PDFs attached and highlighted, and the report PDF in its
`Reports` folder — **plus a separate HTML copy of the report filed back into the DEVONthink
group your documents live in.**

Both copies carry two cross-navigation links at the top: one back to the **source DEVONthink
group**, one to the **matching Bookends folder**. So the report sits beside the material it was
written about, one click from your documents and one click from the library — and the Bookends
side links back the other way.

---

## Privacy

Bookends and DEVONthink are local, on-disk apps, and the report copies stored in them stay
on your machine. The disk copy of the report defaults to iCloud Drive — if you are working
with confidential material, point `RESEARCH_DIR` somewhere local instead.

---

## Files

This repo is a single-plugin **marketplace**: a marketplace manifest at the root points to
one plugin, and that plugin contains the skill.

```
bookends-research-skill/                        # the repo = a Claude plugin marketplace
├── .claude-plugin/
│   └── marketplace.json                        # marketplace manifest (lists the plugin)
├── plugins/
│   └── bookends-research-skill/                # the plugin
│       ├── .claude-plugin/
│       │   └── plugin.json                     # plugin manifest
│       └── skills/
│           └── bookends-research-skill/        # the skill
│               ├── SKILL.md                    # the pipeline (topic = the only variable)
│               ├── references/bookends.md      # Bookends calls, link forms, Vancouver style
│               ├── scripts/
│               │   ├── validate_bookends_links.py       # pre-ship gate: every link resolves
│               │   ├── validate_bookends_attachment.py  # pre-ship gate: right PDF, readable
│               │   ├── validate_duallink.py
│               │   ├── validate_titles.py
│               │   ├── publish_to_web_share.py
│               │   └── styled_links_to_clipboard.sh
│               └── LICENSE
├── README.md                                   # this file (install + usage)
├── LICENSE
└── examples/screenshots/                       # the images above
```

## License

MIT — see [LICENSE](LICENSE).

## Author

**Richard S. Kaplan, MD** — Kaplan Life Care Planning

- Email: rkaplan@kaplanlifecareplan.com
- Website: https://kaplanlifecareplan.com/

Questions and suggestions welcome.
