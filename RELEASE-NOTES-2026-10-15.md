# Release notes, 2026-10-15

A second reader's report, a second repair. This release changes how the
words of 234 records are built, corrects nine records from the printed
editions, and adds an errata file that every later correction will use.

## Thank you to Andrea Catino, who reported this

Andrea Catino, Independent Researcher, Italy (ORCID 0009-0005-4157-5163),
emailed on 2026-10-15 with a register of 63 differences between
lineara.xyz and the printed editions, each with the edition and the page.
We checked all 63 against our scans of those pages. 60 hold up. 15 of them
reached this repository's words; all 15 are corrected here. The two general
counts in the report (114 records with a lacuna mark in the glyph text but
no damage mark on any word; 60 of 62 Za records with no SigLA layer)
reproduced exactly. The full check is in
`verification/lineara-raw-words-2026-10-15.md` and `ERRATA.md`.

## What was wrong

For records whose words come from lineara.xyz (234 of 1,884), the importer
took the words from lineara.xyz's processed syllable list rather than from
its raw transcription. The processed list drops the lacuna marks and joins
words across gaps, so broken fragments looked like whole words. It also
cannot carry the editions' doubt marks (the dots under uncertain signs) or
their brackets for restored signs, because lineara.xyz never encoded those.

## What changed

- Words for lineara.xyz-sourced records are now built from the raw
  transcription (`linear_a/lineara_raw_words.py`). A word never crosses a
  lacuna; a lacuna at a word's edge is written `]` before or `[` after.
  122 of the 234 word lists changed. A new field, `word_layer`, names the
  layer each word list comes from.
- Nine records whose lineara.xyz raw text is itself wrong were corrected by
  hand from the edition page: PK Za 8, PK Za 27, PK Za 28, IO Za 2, IO Za 9,
  IO Za 16, SY Za 2, SY Za 3, THE Zg 16. Each correction is in
  `linear_a/data/corrections.json` with the edition, the page, a crop of the
  line, the sign-by-sign transcription, and every alternative reading with
  who holds it. No alternative is chosen. `ERRATA.md` summarises them.
- A doubtful sign (dotted in the edition) carries a trailing `?` on its
  value, the convention the SigLA-sourced words already used.

## What is still wrong, and known

- `unicode_text` (the sign-by-sign glyph text) still comes from
  lineara.xyz's processed layer on every record that has a lineara id. Sign
  and numeral differences reported for SigLA-worded records (for example
  HT 34, HT 131b, KH 21) are therefore still present in that field. That is
  the next repair.
- Outside the nine hand-corrected records, lineara.xyz-sourced words carry
  no doubt marks, because none exist in the source. Treat every sign in
  those words as "certainty not recorded", not as certain.
- Za records with no SigLA layer (60 of 62) are lineara.xyz-sourced and
  unverified against the editions except where `ERRATA.md` says otherwise.
- `gorila_ref` page numbers are wrong on a block of records (at least 167 of
  512 checked differ from the GORILA V concordance by 4 or more pages).
  Not yet corrected.

If you read this data and something in it looks wrong, please say so, with
the edition and the page. That is what makes a report checkable, and it is
what made this one worth a release.
