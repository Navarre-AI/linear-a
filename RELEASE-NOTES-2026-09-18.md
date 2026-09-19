# Release notes, 2026-09-18

This release changes what this repository is. It used to hold a dataset plus a
body of claims, findings and benchmarks built on that dataset. It now holds the
dataset, the provenance of every field, the code that builds the data, and the
record of every defect that was found and fixed. Nothing else.

The reason is simple. A reader read the data, found a defect in it, and wrote in.
The defect was real. Once it was traced, a large part of the published analysis
turned out to rest on it. Rather than patch the analysis, the analysis is
withdrawn and the data is repaired.

## Thank you to the reader who reported this

An anonymous reader emailed on 2026-09-17 to report a defect in the word data.
The report was correct on every point, and it was specific enough to trace the
cause in one pass. That report is the reason for this release.

If you read this data and something in it looks wrong, please say so. A report
like that one is worth more to this project than any amount of internal review.

## What was wrong

The importer that builds the corpus read one page too many from each source
document. Every document on the source site has one page per word, and one
overview page that repeats every sign of every word. The importer's filter
matched the overview page as well, so each multi-word document gained one extra
word: a string that is every real word of the document joined together. On most
documents that fake word sorted to the front of the list.

318 records carried such a word. Every one of them is corrected. The importer is
fixed, so it cannot happen again.

The effect on the vocabulary counts was large. The number of unique
multi-syllable words in the corpus falls from 1,211 to 979. Any count of words,
any frequency table, and any word list built from the old data is wrong by that
margin.

## Withdrawn: not supported by the data

The following material is removed from this repository:

- The findings report and the success-criteria ladder.
- All 14 benchmark folders and their results.
- The analysis code that produced those results, and the decipherment pipeline
  that called it.
- The old hand-entered Python corpus and sign inventory, superseded by the
  generated data files, and whose own validation report recorded that its
  document identifiers were wrong.
- The word glossary, the morphological analysis, the scribe-attribution output
  and the sign-behaviour atlas.
- The example AI agent.
- The acquisition, citation and text-mining scripts, which read a private
  library and published nothing.

Some of that material was built on the defective word data. Some of it made
claims the data does not support, or that later reading has refuted. This
release does not restate those claims in order to correct them, because
restating them is how they spread. They are withdrawn. If you built on them,
stop.

The full path-by-path inventory, with the reason for each removal, is in
`verification/strip-inventory-2026-09-18.md`.

## What was corrected

**The word data.** 318 corpus records and 432 records in the structured source
file lost the fake word. `verification/pseudo-word-fix-2026-09-18.md`.

**The sign catalogue.** 21 sign types that occur in the corpus were missing from
`signs.json` and are added, including one with 32 occurrences across 25
documents. Five entries that described the numeral notation rather than any sign
are dropped. 24 entries that are real catalogue numbers with no attestation in
this corpus are kept and marked. 255 Unicode codepoints were missing and are
filled, each one verified by decoding the character and checking that its
Unicode name carries that entry's own sign series and number. 22 labels are
resolved against the source, and where two sources disagree both readings are
kept and neither is chosen.
`verification/signs-json-regeneration-2026-09-18.md`.

**The corpus, against the canonical private data.** Three records are added and
25 are changed. One sign count was a count of glyph slots rather than of signs
and is corrected downward. One is corrected upward, because the source added a
sign. Six records whose keys are garbled spellings now carry the correct siglum.
Eight records carry a dating from the 2024 supplement, with a note of how
certain that dating is. Two joins recorded in the supplement are added. One
document that this dataset did not hold is added, with no reading, because no
reading can be made from what we hold. Four texts are flagged as not yet
published. Five disagreements between sources are recorded as disagreements and
none of them is resolved. `verification/private-writeback-2026-09-18.md`.

The record count goes from 1,881 to 1,884.

## Licensing, corrected

The repository claimed a single licence, CC BY 4.0, over data that is not ours
to relicense. Part of the data is derived from SigLA, which is CC BY-NC-SA 4.0,
and CC BY drops both the non-commercial term and the share-alike term. The
required SigLA credit line appeared nowhere in the repository.

There are now two licences, and `LICENSE` names every path. CC BY 4.0 is the
default. The SigLA-derived paths are CC BY-NC-SA 4.0, with the credit line, and
each of those folders carries its own licence file. Inside the two mixed data
files the split is stated by field, so a machine can apply it: a record is
CC BY-NC-SA 4.0 when its `sources` array contains `"sigla"`.

Two files that were verbatim copies of an upstream dataset with no licence are
removed. One of them also carried third-party image-rights strings on 1,328
records. `CREDITS.md` now credits every source, with what it gave and the terms
that apply. `verification/licensing-2026-09-18.md`.

## Where the record is

Every change in this release has a file in `verification/` that names the
defect, the cause, the fix, and the count of records that changed. Read those
rather than this summary if you need to check something.

| File | What it records |
|---|---|
| `strip-inventory-2026-09-18.md` | Every tracked path, its class, and the verdict. |
| `pseudo-word-fix-2026-09-18.md` | The word defect, its cause, and the correction. |
| `signs-json-regeneration-2026-09-18.md` | The sign catalogue, entry by entry. |
| `private-writeback-2026-09-18.md` | The facts carried from the canonical data. |
| `licensing-2026-09-18.md` | The licence split, and two decisions still open. |
| `signs-json-fix-2026-09-06.md` | An earlier glyph defect. |
| `corpus-validation-2026-04-01.md` | The identifier defect in the retired corpus. |
| `claims-reconciliation-summary-2026-09-18.md` | The independent audit of the withdrawn claims, and what it changed. |
| `ph-wa-32-conflict-2026-09-18.md` | A reading conflict on one record, recorded and not resolved. |

`scripts/release_gates.py` runs the seven checks this release had to pass. Run
it from the repository root.

## Independent audit

Before this release, the project listed every claim the repository made: 544
rows, each with a status and a check an outside reader can run. An outside
agent then audited all 544 of those rows against the pre-release snapshot of
this repository and nothing else. It disagreed with our status on 331 rows. We
re-measured every disputed number and accepted 123 of the 331 disagreements,
including all seven of the numbers that were the substance of the dispute. On
those seven the audit was right and we were wrong. Ten rows we hold, 172 are
one verdict under two labels, and 26 are still open. The audit validated no
withdrawn claim, and nothing it found restores a reading, a gloss or a
translation. The full reconciliation, with the counts, the seven re-runs and
the open rows, is in
`verification/claims-reconciliation-summary-2026-09-18.md`. One data change
came out of it: `PH Wa 32` now carries a `conflicts` entry, because a published
source reads that record differently from this corpus and neither reading is
chosen. `verification/ph-wa-32-conflict-2026-09-18.md`.

## What this repository does now

It publishes one machine-readable table per inscription, with every source keyed
to it, and the concordance tables that tie the sources together. It makes no
claim about the Linear A language. It proposes no reading and no translation.
Where a reading appears in a data file, it is transcribed from a named source,
and the field list in `README.md` says which source. Where two sources disagree,
both readings are recorded and neither is chosen.

Counts are published with their denominators, because a count without one is not
a fact about the corpus.

## Addendum, 2026-09-18: the layer check

A second pass checked the data layer by layer. The full record is
`verification/layer-check-2026-09-18.md`. In plain words:

**Words that were lost.** The importer had a second defect. It kept only the
signs that the source marks as sure, so a word made only of unsure or
unidentified signs was dropped, unsure signs vanished from inside words, and a
subscript such as ra2 was cut to ra. After the first fix, 58 of the 318
corrected records still held fewer words than the source counts. For those 58
the source's own word pages were read again, and each record now holds the
source's full word list: 72 words added, 239 in all. Unsure signs are marked
with `?`, and a sign the source does not identify is written `[?]`. The
importer is fixed. Still open: 35 other records from the same source hold no
words at all, and other word lists and sign readings can still lack an unsure
mark or a subscript.

**Two layers of one record.** Most records carry both a glyph string and a word
list, and they come from different sources. For 610 of 1,884 records both are
present. They agree sign for sign in 105 of 610. In 377 of the 505 that differ,
the only differences are damage marks or signs such as numerals, fractions and
commodity signs that the two layers handle differently. In 11 of 610 records
the two layers read a different sign at the same place. Those 11 now carry a
recorded conflict, with both readings and both sources. No reading is chosen.
The drawing decides.

**Record keys.** 119 of 1,884 record keys do not follow the plain pattern of
the standard catalogue. 18 of 119 now carry the standard form as an alias,
from a source held here. 56 of 119 are exactly the form a source prints. 45 of
119 are marked unresolved. No key is renamed.

**Where each file comes from.** Every file in `linear_a/data/` now has an entry
in `linear_a/data/PROVENANCE.json` that names its inputs and the script that
builds it. For 53 of the 54 data files that script is not in this repository,
and the entry says hand-maintained. A new release gate fails if a data file
has no entry.
