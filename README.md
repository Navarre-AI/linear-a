# Linear A corpus dataset

This repository holds a collated, cross-referenced dataset of the Linear A inscriptions.
It is a research tool. It holds the data, the provenance of every field, the code that
builds the data, and the records of the data defects that were found and fixed.

The repository makes no claim about the Linear A language. It proposes no reading and no
translation. Where a phonetic value or a reading appears in a data file, that value is
transcribed from a named source, and the field list below says which source.

What changed on 2026-09-18, and why, is in
[RELEASE-NOTES-2026-09-18.md](RELEASE-NOTES-2026-09-18.md). A large body of claims,
findings and benchmarks was withdrawn in that release, because it was not supported by
the data.

The scholarly literature that the project reads is listed in `BIBLIOGRAPHY.md`. The PDFs
of that literature, the website source for lineara.eu, and the working files stay in a
private companion repository, because most of the PDFs are third-party copyright.

## Sources

| Short name | Full source | What the project takes from it |
|---|---|---|
| GORILA | Godart, L., & Olivier, J.-P. (1976-1985). *Recueil des inscriptions en linéaire A*, Études Crétoises 21, volumes 1 to 5. | Sign numbering (the AB and A sigla), the sign index, the sign variant tableau, the general concordance, page and plate references, dating and scribe notes. |
| RILA Supplement 1 | *Recueil des inscriptions en linéaire A*, Supplement 1 (2025), index. | Current document numbering, used as a concordance against the GORILA numbers. |
| SigLA | Salgarella, E., & Castellan, S. (2020-). *SigLA: The Signs of Linear A*, https://sigla.phis.me/ | Document records, per-sign occurrence records with role and reading, word divisions, bounding boxes, document type and period. CC BY-NC-SA. |
| Younger | Younger, J. G. *Linear A Texts and Inscriptions in Phonetic Transcription*. | Phonetic transcriptions and document readings. |
| lineara.xyz | lineara.xyz corpus data file. | Document ids and Unicode text for documents that SigLA does not carry. |

Credit for each source, and the licence of each source, is in
[CREDITS.md](CREDITS.md). The licence of this repository is in [LICENSE](LICENSE).
See "Licence" below for the two-licence split.

## Data files

All data is under `linear_a/data/`.

### The corpus

`corpus.json` holds 1,884 records, keyed by document id. Fields:

| Field | Where it comes from |
|---|---|
| `id` | Ours. The canonical id. See "How records are identified". |
| `sources` | Ours. Which source files carry this record: `sigla`, `lineara`, `old_corpus`, `gorila_vol5_index`, `rila_2025`. |
| `sigla_id`, `lineara_id`, `old_corpus_id` | The id of this record in that source, as that source writes it. |
| `site`, `type`, `period` | Transcribed from SigLA, or from lineara.xyz for a record that SigLA does not carry. Site spellings are normalised by us. |
| `findspot` | Transcribed from SigLA. |
| `scribe` | Transcribed from SigLA. |
| `gorila_scribe`, `gorila_dating`, `gorila_ref`, `gorila_notes` | Transcribed from GORILA. `gorila_ref` is a volume and page reference. |
| `museum_inventory` | Transcribed from GORILA. |
| `sign_count` | Transcribed from SigLA. |
| `signs` | Transcribed from SigLA. One entry per sign occurrence, with `n` (position), `type` (the sign siglum), `role`, `reading` and `certain`. |
| `unicode_text` | Transcribed from lineara.xyz, or built by us from the SigLA sign list. |
| `words` | Transcribed from SigLA, or from lineara.xyz. In a SigLA word, `re?` is a sign SigLA marks unsure, `[?]` is a sign SigLA shows but does not identify, `[unclassified]` is a sign SigLA labels unclassified, and a SigLA subscript is kept as a digit (`ra2`). See `verification/layer-check-2026-09-18.md`. |
| `word_source` | Ours. Which of those two gave the `words` value. |
| `parent_object`, `face_count` | Ours. The physical object that this face belongs to. |
| `linguistic_value`, `is_ethnographic` | Ours. See "Known limitations". |
| `aliases` | The standard siglum of a record whose key does not follow the plain GORILA pattern, where a held source gives it: RILA Supplement 1, the GORILA vol. 5 concordance, or the Anetaki publication. The key is not renamed. Present on 18 records. |
| `siglum_status`, `siglum_note` | Ours. On the 119 records whose key does not follow the plain GORILA pattern: `aliased`, `source form` (the key is exactly the siglum a held source prints) or `nonstandard, unresolved`, with the source in `siglum_note`. |
| `rila` | RILA Supplement 1 provenance: `siglum`, `period` with `period_certainty`, `support`, `repository`, `findspot`, `editio_princeps`, `joined_into`, `companion_fragment`, and the source of each. Present on 25 records. |
| `conflicts` | A list of rival readings, sites or periods. Each entry names the field, our value, their value, our source, their source, and a note. An entry from the layer check of 2026-09-18 sets the word layer (`ours`) against the glyph layer of the same record (`theirs`). Nothing in this field is resolved. Present on 16 records. |
| `join_of` | The component sigla of a join record. Present on 2 records. |
| `unpublished`, `unread` | Boolean. `unpublished` means the source states the text is not published yet, on 4 records. `unread` means no reading is entered, on 3 records. |
| `sc_note` | The previous `sign_count`, its source, and why it changed. Present on 2 records. |

The corpus holds 4,936 sign occurrences. The roles are `syllabogram` (3,287),
`logogram` (1,175), `fraction` (313), `erasure` (100) and `transaction` (61).

### Signs

`signs.json` holds 402 sign entries, keyed by siglum, plus one top-level `provenance`
object. Each entry carries the occurrence and document counts from the corpus, the
per-stream counts with their denominators, the roles and readings as they occur in the
corpus, a category, an `attested` flag, and a phonetic name and Unicode glyph where a
source gives one. The glyph column was corrected on 2026-09-06. The file was
regenerated on 2026-09-18: 21 attested types added, 5 numeral artefacts dropped, 255
codepoints filled, 22 labels resolved. See
[verification/signs-json-fix-2026-09-06.md](verification/signs-json-fix-2026-09-06.md)
and
[verification/signs-json-regeneration-2026-09-18.md](verification/signs-json-regeneration-2026-09-18.md).

### GORILA and RILA reference files

| File | What it holds |
|---|---|
| `gorila_sign_index.json`, `gorila_sign_index_rows.json`, `gorila_sign_index.xlsx` | The sign index of GORILA Volume 5, pages 135 to 326, transcribed row by row. |
| `gorila_sign_variants.json` | The sign variant tableau of GORILA Volume 5, pages XXV to LII. |
| `gorila_concordances.json`, `gorila_concordances_full.json` | The general concordance of GORILA Volume 5, pages 82 to 113. 468 entries. |
| `gorila_page_map.json` | A page classification of the five GORILA volumes, 1,516 pages. |
| `gorila_sign_plates.json` | The sign plate data of GORILA Volume 5. |
| `signs_to_gorila_index.json` | A join table from sign siglum to the GORILA index rows. |
| `rila_2025_concordances.json` | The index of RILA Supplement 1 (2025), with the sha1 of the source PDF. |

### Source snapshots and merge output

| Path | What it holds |
|---|---|
| `sources/sigla/corpus_structured.json` | The SigLA import, 772 documents, before the merge. |
| `sources/sigla/filemaker_export/` | Exports of the working FileMaker database: 773 document faces, a 731 by 62 document and sign role matrix, 5,714 image references, and site totals. `fm_ingest.py` parses them. |
| `sources/lineara/README.md` | The lineara.xyz snapshot is not redistributed here. The upstream repository carries no licence, so this project holds no grant to copy it. The README says how to fetch it. |
| `sources/intermediate/canonical_id_map.json` | Every source id against its canonical id. |
| `sources/intermediate/unified_corpus_index.json`, `unified_corpus_v2.json` | The merge output, with a flag per source for each record. |
| `sources/intermediate/physical_objects.json` | 1,665 physical objects, each with its list of faces. |
| `sources/intermediate/sign_attestation_index.json` | Per sign: total occurrences and the documents that carry it. |
| `sources/intermediate/word_attestation_index.json` | Per word form: total occurrences, documents, sites and document types. |
| `sources/intermediate/sites/*.json` | The records of one site per file, 18 files. |
| `doc`, `summary`, `role_count`, `image_decode`, `image_names` | FileMaker XML exports of the same working database. |

`linear_a/data/PROVENANCE.json` names, for every file in `linear_a/data/`, what kind of file it is, what it was built from, and the script that builds it, or `hand-maintained` where that script is not in this repository.

### Verification

`verification/` holds one file per data defect that was found. Each file names the
defect, the cause, the fix, and the count of records that changed. The audit files
`corpus_audit_matrix.json`, `corpus_enrichment_audit.json`, `word_dedup_audit.json`,
`sign_301_cross_check.json`, `sources/intermediate/cross_reference_report.json` and
`sources/intermediate/sign_reconciliation.json` hold the counts that those checks
produced.

## Data descriptions

Every line below is a count of what a file in this repository holds. Each one
carries its denominator and names the layer it measures. None of them is a
finding, and none of them carries a reading. All were recounted against this
release on 2026-09-18.

Two layers are counted separately, and they are not comparable. `corpus.json`
is the merged corpus, 1,884 records. `sources/sigla/corpus_structured.json` is
the SigLA import before the merge, 772 records. A count from one layer does not
refute a count from the other.

1. `corpus.json` holds 1,884 of 1,884 records. 762 of 1,884 carry a `signs`
   array, 670 of 1,884 carry a `words` field, of which 666 are non-empty, and
   352 of 1,884 carry `parent_object`. A record is one inscribed face, so a
   record count is not an object count.
2. `corpus.json` holds 4,936 sign occurrences, across the 762 records that
   carry a `signs` array. The roles are syllabogram 3,287, logogram 1,175,
   fraction 313, erasure 100 and transaction 61.
3. `gorila_concordances_full.json` holds 468 of 468 entries across 33 of 33
   leading site codes. `gorila_sign_variants.json` holds 181 of 181 sign
   records with 694 of 694 attestation references.
4. `sources/sigla/corpus_structured.json` holds 772 of 772 records across 18 of
   18 site labels. 432 of 772 carry a non-empty word array. Those arrays hold
   1,228 of 1,228 entries and 793 of 793 distinct strings, of which 991 of
   1,228 entries and 719 of 793 types carry a hyphen.
5. The same file holds 4,935 of 4,935 parsed sign occurrences: syllabogram
   3,286, logogram 1,175, fraction 313, erasure 100 and transaction 61. At
   least one logogram-role occurrence appears in 515 of 772 records.
6. Logogram-role document counts in that file, by sign id: `AB30` 54 of 772,
   `AB120` 43 of 772, the `AB131` family 44 of 772, the `AB21` family 15 of
   772, `AB122` 16 of 772, `AB100` 20 of 772 and `AB302` 15 of 772. Counts over
   all roles are larger, for example `AB30` at 91 of 772, because the same sign
   also occurs as a syllabogram. These are document counts per sign id, not
   commodity counts: a commodity name is a reading.
7. Sign `A301` occurs in 48 of 772 records of that file. Its roles there are
   logogram 36 of 48, syllabogram 11 of 48, erasure 1 of 48 and fraction 0 of
   48. Haghia Triada holds 36 of 48. Of the 32 of 48 records typed `nodule`,
   32 of 32 hold exactly one parsed sign.
8. The codepoint U+10655 occurs in the `unicode_text` of 272 of 1,884 records
   of `corpus.json`. 234 of those 272 are `Wa` records, and 230 of 234 hold
   exactly one Linear A codepoint. This is a different layer from item 7, and
   the two counts are not comparable.
9. `signs.json` holds 403 of 403 top-level keys: 402 sign entries and one
   `provenance` object. 334 of 402 entries carry a Unicode codepoint, and 334
   of 334 decode to a character whose Unicode name carries that entry's own
   sign series and number. 25 of 402 entries have zero occurrences in this
   corpus. `sources/intermediate/sign_attestation_index.json` holds 356 of 356
   sign keys.
10. In `sources/sigla/corpus_structured.json` the `sign_count` metadata sums to
    4,942 of 4,942 while the parsed entries total 4,935 of 4,942. The shortfall
    is 7 of 4,942. The cause is not established.

## Code

| File | What it does |
|---|---|
| `linear_a/corpus_model.py` | The data model: `Document`, `Face`, `Line`, `Word`, `SignOccurrence`, and the role, type and period enumerations. |
| `linear_a/import_sigla.py` | Builds the corpus records from a local snapshot of the SigLA site. The snapshot is not in this repository. |
| `linear_a/data/sources/sigla/filemaker_export/fm_ingest.py` | Parses the FileMaker CSV exports and merges them with `corpus.json`. |
| `linear_a/apply_private_writeback_2026-09-18.py` | Applies one documented subset of the private canonical data to `corpus.json`. It reads the private file read-only, at a path given as an argument, and asserts that nothing outside its declared list changed. It runs once. |
| `linear_a/apply_ph_wa_32_conflict_2026-09-18.py` | Adds the sixth `conflicts` entry, on `PH Wa 32`, by the same mechanism. The first write-back script runs once, so this is a second dated script. |
| `scripts/release_gates.py` | The seven release gates: no em dash and no Linear A codepoint outside the named data fields, every README link and every LICENSE path resolves, no tracked image, the corpus record count, no surviving pseudo-word, and every glyph in `signs.json` decoding to its own sign. Run it from the repository root before every release. |

## How records are identified

One record is one inscribed face.

- **Id scheme.** An id follows the GORILA convention: a site code, a document class
  where the source gives one, and a number. Examples: `HT 31`, `KH Wa 1015α`,
  `IO Za 2`, `ZA 8`.
- **Faces.** A face suffix follows the number: `HT 115a` and `HT 115b` are two faces of
  one tablet. 352 records carry a `parent_object` field, and those records group into
  137 objects. A record with no `parent_object` field is its own object.
- **Joins.** A join keeps the id that the source publication gives it. The dataset does
  not merge two ids into one record.
- **Aliases.** `sigla_id`, `lineara_id` and `old_corpus_id` hold the id of the same
  record in each source. `sources/intermediate/canonical_id_map.json` holds the same
  map in one file, including the normalised keys, such as `khwa1015α` for
  `KH Wa 1015α`.

## Known limitations

- **Pseudo-word defect, fixed 2026-09-18.** The importer read the SigLA overview page
  `index-word.html` as if it were a word page. That added one word per document, equal
  to the join of all the real words, at word index 0. A reader reported the defect on
  2026-09-17. The importer is fixed, and the data was corrected as a post-pass. The
  record is
  [verification/pseudo-word-fix-2026-09-18.md](verification/pseudo-word-fix-2026-09-18.md).
- **Private write-back, 2026-09-18.** The canonical data is in a private companion
  repository. On 2026-09-18 a documented subset of it was applied to this corpus:
  three records added, 25 changed. `PH 26` sign count 7 to 2, `HT 129` 15 to 16, six
  garbled sigla given their correct siglum, eight RILA periods recorded, two Khania
  joins and `SKO Zc 2` added, five conflicts recorded, four texts flagged unpublished.
  No reading was picked and no conflict was resolved. The script is
  `linear_a/apply_private_writeback_2026-09-18.py` and the record is
  [verification/private-writeback-2026-09-18.md](verification/private-writeback-2026-09-18.md).
- **1,884 records against 1,534 physical inscriptions.** RILA Supplement 1 counts 1,534
  physical inscriptions. This dataset holds 1,884 records for three reasons. One, a
  record is a face, not an object, and the faces in this dataset group into 1,665
  objects. Two, the merge keeps every id that any source carries, so an id that one
  source spells differently, or that RILA treats as part of another object, stays as its
  own record. 1,025 records come from lineara.xyz alone, and 99 come from SigLA alone.
  Three, no record is dropped for lack of a RILA match. A record-by-record
  reconciliation against RILA Supplement 1 is not done.
- **Damage placeholders.** 358 of the 4,936 sign occurrences have `type: null`,
  `reading: null` and `certain: false`. They mark a sign position where the source reads
  damage, not a sign. Count them as positions, not as signs.
- **Partial fields.** `words` is present on 666 records and `signs` on 762, because
  SigLA carries the per-sign data and SigLA holds 772 of the 1,884 records.
  `unicode_text` is present on 1,707 records. `period` is empty or `unknown` on 348
  records.
- **`linguistic_value` and `is_ethnographic`.** These two fields are ours. An earlier
  merge set them. They are not source data and they are not verified. Do not read them
  as a statement about any record.
- **The `old_corpus` source.** 129 records carry an `old_corpus_id`. That source was an
  earlier hand-entered transcription set. Its files are no longer in this repository,
  and its document ids do not match GORILA or SigLA numbering. See
  `verification/corpus-validation-2026-04-01.md`. Treat an `old_corpus_id` as a
  provenance label only. 60 of the 1,884 records carry `old_corpus` as their only
  source. Each of those 60 holds an id and the merge fields only, with no signs, no
  words and no text.
- **Period strings.** A period string is transcribed as the source writes it. The
  strings are not normalised to one scheme.
- **Two characters that are data, not prose.** `unicode_text` carries a Linear A glyph
  stream, so it holds codepoints in the Unicode Linear A block, U+10600 to U+1077F. It
  also holds an em dash on its own line, 38 records, which is the ruling line that the
  source draws across the object. `museum_inventory` holds an em dash on 68 records,
  where the printed apparatus gives a museum code and no number. Neither character is
  prose and neither is removed. The same applies to `unicode` in `signs.json` and to
  `reading_ours` in `corpus_audit_matrix.json`, which is a copy of the glyph stream.

## Reading the data

```python
import json

corpus = json.load(open("linear_a/data/corpus.json"))
print(len(corpus))                 # 1884

record = corpus["HT 31"]
print(record["site"], record["type"], record["sign_count"])
print(record["sources"])
```

## Licence

This repository holds material under two licences. [LICENSE](LICENSE) names every path.
[CREDITS.md](CREDITS.md) credits every source.

**Default: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).** This covers the
project's own code, text and generated data. You may use, adapt and build on it,
including commercially. Please cite the project and link back to this repository or to
lineara.eu.

**Exception: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).**
The SigLA-derived data carries the SigLA licence, because SigLA is CC BY-NC-SA 4.0. That
covers `linear_a/data/sources/sigla/**`, the FileMaker exports inside it,
`linear_a/data/signs.json`, and the records in `linear_a/data/corpus.json` whose
`sources` array contains `"sigla"`. Those paths are non-commercial, and a derivative of
them carries the same licence. Part 2 of [LICENSE](LICENSE) states the split in full and
carries the required credit line:

> Sign drawings from SigLA: The Signs of Linear A, a palaeographical database, by Ester
> Salgarella and Simon Castellan (https://sigla.phis.me/), licensed under
> CC BY-NC-SA 4.0.

The PDFs and extracted text in the private companion repository are not covered by
either licence. They stay under the copyright of their authors and publishers. GORILA
and RILA Supplement 1 are cited, not included.

## How to cite

> Navarre, M. (2026). *Linear A corpus dataset*. https://github.com/Navarre-AI/linear-a

Cite the underlying sources as well. `CREDITS.md` names each source and its licence, and
`BIBLIOGRAPHY.md` gives the full citation of every work the project reads.
