# Strip inventory, 2026-09-18

Scope: every tracked path in this repository at branch point `be08618`.
Rule applied: the public repository holds data, provenance, the tooling that builds the
data, verification of the data, the bibliography, credits and licences. It holds no
claims, no findings, no benchmarks, no decipherment work, no model-written analysis and
no agent examples.

Class values: `data`, `data tooling`, `verification`, `bibliography`, `claim-or-analysis`,
`example-or-slop`, `repo admin`.

## Top level

| Path | What it is | Class | Verdict |
|---|---|---|---|
| `.gitignore` | Ignore rules. | repo admin | keep |
| `BIBLIOGRAPHY.md` | Every third-party work the project reads, with local path and status. | bibliography | keep, two lines neutralised |
| `LICENSE` | CC-BY-4.0 text. Branch `fix/b-licensing` owns the final text. | repo admin | keep, not touched |
| `README.md` | Project description with a findings section and a benchmark section. | claim-or-analysis | rewrite |
| `benchmarks/` | 14 benchmark folders. | claim-or-analysis | remove |
| `examples/` | One AI agent starter. | example-or-slop | remove |
| `linear_a/` | Data, data model, importer, analysis code. | mixed | keep in part |
| `scripts/` | 22 scripts plus one shell script. | mixed | remove |
| `verification/` | Data defect records. | verification | keep |

## linear_a

| Path | What it is | Class | Verdict |
|---|---|---|---|
| `FINDINGS.md` | Findings report: Zipf exponent, language-isolate score, vocabulary readings, morphology. | claim-or-analysis | remove |
| `SUCCESS_CRITERIA.md` | Tiered decipherment goal ladder. | claim-or-analysis | remove |
| `analysis/` | `cross_reference.py`, `frequency_analysis.py`, `morphology.py`, `role_clustering.py`: the analysis engine behind FINDINGS.md. | claim-or-analysis | remove |
| `corpus_model.py` | Dataclasses and enums for Document, Face, Line, Word, SignOccurrence. Read in full: it is a data model only, and `import_sigla.py` imports it. | data tooling | keep |
| `decipher.py` | Decipherment pipeline, imports `analysis/`, prints a decipherment assessment. | claim-or-analysis | remove |
| `import_sigla.py` | Builds the corpus from the SigLA snapshot. | data tooling | keep |
| `imagelist` | Empty file, 2 bytes. | example-or-slop | remove |
| `data/__init__.py` | Empty. | data tooling | keep |
| `data/corpus.json` | The corpus. Owned by branch `fix/a1-importer`. | data | keep, not touched |
| `data/signs.json` | The sign catalogue. Owned by branch `fix/a3-signs`. | data | keep, not touched |
| `data/VALIDATION_REPORT.md` | Record of the document-ID defect in the old Python corpus. | verification | move to `verification/` |
| `data/corpus/*.py` | The old hand-entered Python corpus, 129 entries, with proposed meanings in the notes fields. Its own validation report states the document IDs are wrong. Superseded by `corpus.json`. | claim-or-analysis | remove |
| `data/glossary.json`, `data/glossary.py` | Word meanings with confidence levels and evidence lines. | claim-or-analysis | remove |
| `data/morphological_analysis.json` | Suffix inventory with percentages. | claim-or-analysis | remove |
| `data/scribe_profiles.json`, `data/scribe_similarity.json`, `data/scribe_attribution_predictions.json` | Scribe attribution output. | claim-or-analysis | remove |
| `data/sign_behavior_atlas.json` | Per-sign behaviour aggregate with an interpretive layer. | claim-or-analysis | remove |
| `data/signs.py` | Python sign inventory, superseded by `signs.json`, carries interpretive source notes. | claim-or-analysis | remove |
| `data/corpus_audit_matrix.json` | Corpus checked row by row against the GORILA sign index and concordance. | verification | keep |
| `data/corpus_enrichment_audit.json` | Which concordance entries matched a corpus row. | verification | keep |
| `data/word_dedup_audit.json` | The 114 documents whose `words[]` the parser doubled. | verification | keep |
| `data/sign_301_cross_check.json` | Counts for sign A301 in the corpus against the GORILA index. | verification | keep |
| `data/gorila_concordances.json`, `data/gorila_concordances_full.json` | GORILA concordance, transcribed. | data | keep |
| `data/gorila_page_map.json`, `data/gorila_sign_plates.json` | GORILA page and plate references. | data | keep |
| `data/gorila_sign_index.json`, `data/gorila_sign_index_rows.json`, `data/gorila_sign_index.xlsx` | GORILA Volume 5 sign index, transcribed. | data | keep |
| `data/gorila_sign_variants.json` | GORILA sign variants. | data | keep |
| `data/rila_2025_concordances.json` | RILA Supplement 1 numbering. | data | keep |
| `data/signs_to_gorila_index.json` | Join table, sign id to GORILA index rows. | data | keep |
| `data/doc`, `data/image_decode`, `data/image_names`, `data/role_count`, `data/summary` | FileMaker XML exports of the working database. | data | keep |
| `data/images/test.txt` | Placeholder. | repo admin | keep |
| `data/sources/intermediate/canonical_id_map.json` | Id alias map across sources. | data | keep |
| `data/sources/intermediate/cross_reference_report.json` | Counts of the SigLA and lineara.xyz merge. | verification | keep |
| `data/sources/intermediate/physical_objects.json` | Face to object grouping. | data | keep |
| `data/sources/intermediate/sign_attestation_index.json`, `word_attestation_index.json` | Index of where each sign and word occurs. | data | keep |
| `data/sources/intermediate/sign_reconciliation.json` | Sign inventory reconciled against corpus occurrences. | verification | keep |
| `data/sources/intermediate/positional_analysis.json` | Bigram counts and top bigram list. | claim-or-analysis | remove |
| `data/sources/intermediate/unified_corpus_index.json`, `unified_corpus_v2.json` | Merge output. | data | keep |
| `data/sources/intermediate/sites/*.json` | Per-site record sets, 18 files. | data | keep |
| `data/sources/lineara/lineara_xyz_corpus.js`, `lineara_xyz_parsed.json` | lineara.xyz source snapshot and its parse. | data | keep |
| `data/sources/sigla/corpus_structured.json` | SigLA import output. | data | keep |
| `data/sources/sigla/filemaker_export/fm_*.csv`, `fm_summary.md`, `fm_role_count.md` | FileMaker exports and their column tables. | data | keep |
| `data/sources/sigla/filemaker_export/fm_ingest.py` | Parses those CSV files. Imports nothing that is removed. | data tooling | keep |
| `data/sources/old_corpus/` | A second copy of the old Python corpus, plus `sign_inventory.py` and `sign_inventory_complete.py`. Same defects as `data/corpus/`. | claim-or-analysis | remove |

## benchmarks, all 14

Every folder holds a `metadata.json` and a `results.md`, and four also hold a `README.md`
and a `method.md`. Each one states a result against the corpus. All are
`claim-or-analysis`. All removed, with `benchmarks/README.md`.

`case-system-analysis`, `commodity-distribution`, `compound-words`,
`ku-ro-summation-marker`, `libation-formula-detection`, `loanword-identification`,
`po-to-ku-ro-grand-total`, `sign-A301-analysis`, `sign-cooccurrence`,
`site-dialect-variation`, `tablet-translations`, `word-boundary-preferences`,
`word-class-detection`, `word-order-analysis`.

## examples

| Path | What it is | Class | Verdict |
|---|---|---|---|
| `examples/ai-agent-starter/README.md`, `agent.py`, `tools.py` | A starter agent that runs the decipherment tools. | example-or-slop | remove |

## scripts

No script in `scripts/` builds or validates a published data file. Two read
`linear_a/data/` and both are analysis. The other twenty read and write the private
references repository through `scripts/_paths.py`. All removed.

| Path | What it is | Class | Verdict |
|---|---|---|---|
| `_paths.py` | Resolver for the private references repository. No kept file imports it. | data tooling | remove |
| `build_acquisition_priority.py` | Ranks works to acquire. | claim-or-analysis | remove |
| `build_citation_graph.py` | Citation graph over the private PDF text. No published table. | claim-or-analysis | remove |
| `build_collaboration_graph.py` | Co-authorship and co-citation graph over the same text. No published table. | claim-or-analysis | remove |
| `build_pdf_registry.py` | Registry of the private PDF library. The registry is not published here. | private pipeline | remove |
| `build_sign_behavior_atlas.py` | Builds `sign_behavior_atlas.json`. | claim-or-analysis | remove |
| `classify_images.py`, `cull_images.py`, `review_images.py` | Image triage for the private extraction. | private pipeline | remove |
| `deep_corpus_analysis.py` | Mines the private extracted text. | claim-or-analysis | remove |
| `detect_multipaper.py` | Finds PDFs that hold several papers. | private pipeline | remove |
| `extract_all_pdfs.py`, `extract_pdf_to_rich_md.py` | PDF text and image extraction. | private pipeline | remove |
| `find_oa_papers.py`, `oa_sweep2.py`, `oa_sweep3.py` | Open-access acquisition sweeps. | private pipeline | remove |
| `git-sync.sh` | Multi-agent pull and push helper. Builds no data. | repo admin | remove |
| `improved_reference_parser.py` | Reference-list parser for the private text. | private pipeline | remove |
| `reassemble_chunked_pdfs.py`, `rename_pdfs.py` | PDF file handling in the private repository. | private pipeline | remove |
| `sites_index.py` | Site index over tablet mentions in the private text. It does not build a published index. | claim-or-analysis | remove |
| `tablet_cooccurrence.py` | Tablet co-mention graph. | claim-or-analysis | remove |
| `test_syllabic_ordering.py` | Tests the Duhoux syllabic-ordering hypothesis. | claim-or-analysis | remove |
| `tfidf_keywords.py` | Per-paper keyword extraction. | claim-or-analysis | remove |
| `vision/prepare_pages.py` | Page image preparation for a vision pass. | private pipeline | remove |

## verification

| Path | What it is | Class | Verdict |
|---|---|---|---|
| `signs-json-fix-2026-09-06.md` | The signs.json glyph defect and its fix. | verification | keep |
| `strip-inventory-2026-09-18.md` | This file. | verification | keep |
| `corpus-validation-2026-04-01.md` | Moved here from `linear_a/data/VALIDATION_REPORT.md`. | verification | keep |
