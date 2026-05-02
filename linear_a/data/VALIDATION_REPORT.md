# Corpus Validation Report

## Date: 2026-04-01

## Summary

The old Python corpus (129 entries in `linear_a/data/corpus/`) has been validated
against the new structured import from SigLA (772 documents in `corpus_structured.json`).

**Critical finding: the old corpus uses incorrect document IDs.**

## The Problem

The old corpus was built from Younger's simplified transcriptions, which use
renumbered/simplified identifiers. These do NOT match GORILA/SigLA's standard
numbering. Example:

- Old corpus "HT 1" contains: `ka-u-de-ta . GRA 20, di-de-ru . GRA 3, ...`
- SigLA "HT 1" contains: `qe-ra-u, ki-ro, *79-su, di-di-za-ke, ...`
- The old "HT 1" content actually matches **SigLA "HT 13"**

This means every document reference in the old corpus benchmarks and translations
should be treated as approximate, not exact.

## Number Reconciliation

| Source | Documents | Signs | Words | Unique Words |
|--------|-----------|-------|-------|-------------|
| Old Python corpus | 129 | ~376 (from line strings) | 376 | 66 |
| SigLA import | 772 | 4,935 | 1,660 | 1,025 |
| SigLA metadata | 772 | 4,942 | — | — |

### Why the sign counts differ

- **4,935**: Every sign occurrence we parsed from SigLA HTML popups
- **4,942**: What SigLA reports in its own metadata (7 signs in damaged HTML)

### Why the word counts differ

- **66**: Old corpus only parsed words from 129 hand-entered line strings
- **1,025**: Full SigLA corpus has word-view pages for all documents

## Documents in Old Corpus Missing from SigLA (40)

These fall into categories:

1. **Libation formulas** (29 entries): Hand-entered from Younger, mostly stone vessels
   from peak sanctuaries (AP, IO, AR, KO, PS, SY prefixes). SigLA may not include
   all of these because it focuses on administrative documents.

2. **Ivory scepter** (2 entries): Added manually from 2024 discovery. Not in SigLA.

3. **Name mismatches** (9): Documents like "MA 3", "KEA 1", "MI 1" that exist in SigLA
   under different identifiers.

## Recommendation

The structured SigLA import (`corpus_structured.json`) should be treated as the
**canonical corpus** for all computational analysis. The old Python corpus modules
should be retained for backward compatibility but marked as deprecated.

The libation formula entries (29) should be migrated to the new format and added
to the structured corpus, since they represent important ritual texts that SigLA
may undercount.
