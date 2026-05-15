# Linear A — Research Project

A working catalog of the scholarly literature about **Linear A**, the undeciphered writing system of Minoan Crete (c. 1800–1450 BCE), plus a set of tools for searching and cross-referencing it.

The aim is to be a useful, free resource — a maintained collection of what's been written about Linear A, by whom, when, and on what basis — kept current as new work appears. This is a catalog and a query layer, not a new decipherment attempt; the project's value is in making the existing scholarship navigable and the disagreements within it visible.

Public outputs live at **[lineara.eu](https://lineara.eu)**. There's also an AI-assisted research chat tool at **[lineara-ask.fly.dev](https://lineara-ask.fly.dev)** (invite-only) for asking the corpus questions in natural language.

This repository contains the canonical structured corpus data and analysis code. The source PDFs of the scholarly literature (most of which is third-party copyrighted), the website source, and internal working files live in a separate private companion repository — see [Companion repository](#companion-repository) below.

---

## What's in here

```
linear_a/                Research code + canonical data
  data/                    Corpus and sign-catalog JSON files (the data layer)
    corpus.json              1,881 inscriptions, merged from SigLA + lineara.xyz + GORILA
    signs.json               Sign catalog
    glossary.json            Working glossary
    gorila_concordances_full.json   468 entries × 33 sites, extracted from GORILA
    gorila_sign_index.json   Sign index from GORILA Vol 5
    gorila_sign_variants.json  181 signs, 694 attestation references
    sign_301_cross_check.json    Sign-*301-specific cross-references
    sign_behavior_atlas.json     Per-sign behavior aggregator
    corpus/                  Per-site Python helpers (haghia_triada, khania, …)
    images/                  Sign image assets
  corpus_model.py          Corpus data model
  decipher.py              Decipherment helpers
  glossary.py              Glossary tooling
  import_sigla.py          SigLA-format ingester
  signs.py                 Sign helpers
  FINDINGS.md              Findings report (Zipf, language-isolate scoring, etc.)
  SUCCESS_CRITERIA.md      Tiered success ladder for the project

scripts/                 Python tooling (analysis, extraction, OA acquisition)
  build_acquisition_priority.py    Citation-gap analysis (unique-doc metric)
  build_citation_graph.py          Citation network from extracted PDFs
  build_collaboration_graph.py     Co-authorship network
  build_pdf_registry.py            PDF inventory
  build_sign_behavior_atlas.py     Per-sign behavior aggregator
  extract_all_pdfs.py              PDF → text + images (UUID5-keyed)
  deep_corpus_analysis.py          Corpus statistics
  tablet_cooccurrence.py           Tablet-level co-occurrence
  tfidf_keywords.py                TF-IDF keyword extraction
  sites_index.py                   Per-site index builder
  classify_images.py / cull_images.py / review_images.py    Image triage
  detect_multipaper.py             Multi-paper PDF detection
  improved_reference_parser.py     Reference-list parser
  find_oa_papers.py / oa_sweep2.py / oa_sweep3.py    Open-access discovery
  reassemble_chunked_pdfs.py       Re-stitch large PDFs split for git
  rename_pdfs.py
  test_syllabic_ordering.py        Test for syllabic-ordering hypothesis
  vision/                          Vision pipeline (work in progress)
  _paths.py                        Path resolver — see "Companion repository" below

benchmarks/              Structured tests against the corpus
  README.md                        Categories: replication / exploratory / disproof
  ku-ro-summation-marker/          Replication: ku-ro = "total"
  po-to-ku-ro-grand-total/         Replication: po-to-ku-ro grand-total
  libation-formula-detection/      Replication: ritual formula family
  sign-A301-analysis/              Active: sign *301 analysis
  case-system-analysis/, commodity-distribution/, compound-words/,
  loanword-identification/, sign-cooccurrence/, site-dialect-variation/,
  tablet-translations/, word-boundary-preferences/, word-class-detection/,
  word-order-analysis/

BIBLIOGRAPHY.md          Citation registry (HELD vs MISSING)
```

## Companion repository

PDFs of source literature, the lineara.eu website source, and internal working files live in a separate **private** repository called `minoan-linear-a-references`. That companion repo is large — tens of thousands of files, several GB on disk — because it holds:

- The full PDF library (~1.6 GB) — all the published Linear A scholarship the project draws on, organised under `references/` (core, comparative, fringe, bibliographic).
- All five volumes of GORILA (Godart & Olivier's *Recueil des inscriptions en linéaire A*) as page scans.
- The extracted text + image assets from every PDF in the library (~45 GB), used by the analysis pipeline.
- The lineara.eu website source HTML/CSS/JS and supporting data files.
- Internal working notes, agent coordination, and acquisition logs.

That repo stays private because most of its contents are third-party copyrighted scholarship that we're allowed to use locally for research but not redistribute. The **canonical research data and analysis code in *this* repo are fully public**, released under CC-BY-4.0 (see [License](#license)).

Most analysis scripts in `scripts/` read from the companion repo via `scripts/_paths.py`. The resolver looks for a sibling directory `../minoan-linear-a-references/` by default, and can be overridden with the `MINOAN_REFS_ROOT` environment variable. If you clone this repo standalone, the analysis scripts that need the companion repo will warn but the canonical data under `linear_a/data/` is fully self-contained — you can read, query, and analyse it directly without the companion repo.

## Reading the corpus

`linear_a/data/corpus.json` is keyed by document ID. Each entry is a dict with fields like `id`, `site`, `type`, `period`, `signs`, and source provenance:

```python
import json
corpus = json.load(open("linear_a/data/corpus.json"))
print(len(corpus))                      # 1881
ht31 = corpus["HT 31"]
print(ht31["site"], ht31["type"])
```

Document IDs follow GORILA conventions (`HT 31`, `KH 5`, `ZA 8`, etc.). Sites are spelling-normalised; periods follow the standard MM/LM dating frame.

## Running benchmarks

Each benchmark folder has a `metadata.json` and a `results.md`. Read `benchmarks/README.md` for the categorisation system (replication / exploratory / disproof) and the status labels.

## Findings

See `linear_a/FINDINGS.md` for the headline results, and **[lineara.eu/findings](https://lineara.eu/findings)** for the public-facing version. Highlights:

- Linear A records a natural language (Zipf exponent ≈ 1.10, R² = 0.90).
- Strong evidence for the language-isolate hypothesis vs. Semitic / Anatolian.
- Replicated `ku-ro` as a summation marker and `po-to-ku-ro` as the grand-total expression from corpus structure alone.
- Detected a ritual-exclusive libation-formula family.
- Active work on sign **\*301** — its phonetic value, iconographic origin, and administrative role.

## License

The data, code, and analyses in this repository are released under **[Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/)**. You're free to use, adapt, and build on anything here — please cite the project and include a link back to this repository or to lineara.eu.

The PDFs and extracted text in the private companion repo are NOT covered by this license — those remain under the copyright of their original authors and publishers.

## Citation

> Navarre, M. (2026). *Minoan Linear A — Computational Research Project*. https://github.com/Navarre-AI/linear-a · https://lineara.eu

## Author

Matt Navarre — based in Crete. Database developer, AI-integration specialist, and trainer. Not a Linear A specialist by training; this project is a serious-amateur attack on the puzzle, with AI assistance, where every claim aims to be auditable from the data in this repo.

Contact via [lineara.eu](https://lineara.eu) or via this repo's issue tracker.
