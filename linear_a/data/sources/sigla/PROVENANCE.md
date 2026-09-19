# Provenance: SigLA-derived data in this folder

Licence for this folder: CC BY-NC-SA 4.0. See `LICENSE` in this folder, and
part 2 of [LICENSE](../../../../LICENSE) at the repository root.

## Upstream source

SigLA: The Signs of Linear A, a palaeographical database, by Ester Salgarella
and Simon Castellan. <https://sigla.phis.me/>

The database paper: Salgarella, E., and Castellan, S. (2021). SigLA: signs of
Linear A.

Credit line, verbatim, required on any use or derivative:

> Sign drawings from SigLA: The Signs of Linear A, a palaeographical database,
> by Ester Salgarella and Simon Castellan (https://sigla.phis.me/), licensed
> under CC BY-NC-SA 4.0.

## What is here, and what changed

| File | Records | What this project did to it |
|---|---|---|
| `corpus_structured.json` | 772 documents | Structured from the SigLA document pages by `linear_a/import_sigla.py`. Keyed by document id. Per-document fields and a per-position sign list. No sign data was altered. |
| `filemaker_export/fm_doc.csv` | one row per document | Flattened from `corpus_structured.json` for import into FileMaker. |
| `filemaker_export/fm_decode.csv` | one row per sign position | Flattened from the per-position sign lists. |
| `filemaker_export/fm_role_count.csv`, `fm_role_count.md` | aggregate | Counts of sign roles, computed over the 772 documents. A derivative measurement. |
| `filemaker_export/fm_summary.csv`, `fm_summary.md` | aggregate, by site | Document and sign counts per site, computed over the 772 documents. A derivative measurement. |
| `filemaker_export/fm_ingest.py` | code | This project's own script. CC BY 4.0, not CC BY-NC-SA 4.0. |

Changes indicated, as CC BY requires: the data was reshaped (scraped page
structure to JSON, then JSON to CSV and Markdown tables) and aggregated. No
reading, no `certain` flag and no sign type was changed.

## Where this data reaches in the repository

- `linear_a/data/corpus.json` merges these 772 documents with other sources.
  A merged record is SigLA-derived when its `sources` array contains `"sigla"`.
  Those records are CC BY-NC-SA 4.0.
- `linear_a/data/signs.json` counts occurrences over the merged corpus, so its
  counts are derivative measurements and the file is CC BY-NC-SA 4.0.

## Known defects in this data, 2026-09-18

1. `import_sigla.py` matched SigLA's own overview page `index-word.html` as if
   it were a word record, which made one pseudo-word per document. Fixed on
   2026-09-18: see `verification/pseudo-word-fix-2026-09-18.md`.
2. `import_sigla.py` kept only the `sure-reading` spans of a word page. A word
   of unsure or unidentified signs was dropped, unsure signs vanished from
   inside words, and a subscript such as ra2 was cut to ra. The importer is
   fixed, and the full word lists of the 58 records that fell short of
   SigLA's word count were restored from SigLA's word pages. The rest is still
   open: 35 SigLA records hold no words, and the other word lists and the
   sign-array readings can still lack an unsure mark or a subscript. See
   `verification/layer-check-2026-09-18.md`, section 1.

## No images

No SigLA image file is tracked in this repository today. When the tracings and
crops are published, they carry the same licence and the same credit line, with
their own `LICENSE` file per folder. Part 2.3 of the root LICENSE reserves the
paths.
