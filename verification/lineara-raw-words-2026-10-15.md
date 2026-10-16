# lineara.xyz words from the raw layer, 2026-10-15

Reported by Andrea Catino (ORCID 0009-0005-4157-5163) by email on 2026-10-15 (a
register of 63 rows, lineara.xyz against the printed editions). This note covers the importer
defect behind 15 of those rows. The rows themselves are verified separately.

## The defect

lineara.xyz (`mwenge/lineara.xyz`, `LinearAInscriptions.js`) holds two layers per
record:

- `transcription`, the raw glyph stream. It keeps the lacuna mark U+1076B.
- `parsedInscription`, `words` (glyph words) and `transliteratedWords`, a derived
  layer. `transliteratedWords` is the glyph `words` list read through
  `items_analysis/syllables.txt`, and that reading drops U+1076B: of 953 glyph
  words that hold a sign and a lacuna mark, 952 come out with no mark. 28 of them
  hold the mark between two signs, so the signs on either side are fused into one
  word.

The 234 records of `corpus.json` with `word_source: "lineara"` took their words
from `transliteratedWords`: every hyphenated item, lowercased, subscripts as
digits. 232 of 234 match that rule exactly (HT 105 and PE 1 drop one hyphenated
item each; the script that first built the file is not in this repository).
114 of the 234 have U+1076B in `unicode_text` and no damage mark on any word.

## The fix

`linear_a/apply_lineara_raw_words_2026-10-15.py`, with the rules in
`linear_a/lineara_raw_words.py`:

1. Signs and lacunae come from `transcription`.
2. A word is a run of Linear A signs. It ends at a word divider, an Aegean
   number, a fraction sign, any other character, and a lacuna mark.
3. A lacuna mark next to a word is written on that edge: `]` before the first
   sign, `[` after the last. A word is never joined across a lacuna.
4. Where the raw layer puts two signs side by side with nothing between them, the
   cut between two words comes from lineara.xyz's glyph `words` list at the
   aligned position (difflib on the codepoints, equal blocks and same-length
   replace blocks only). An unaligned position takes no cut. The same alignment
   decides whether a fraction-range glyph (U+10740 to U+1076A) is a sign of a
   word: it is when its glyph word also holds a sign of the syllabary range.
5. A raw line break ends a word unless the signs on both sides align to one
   glyph word. Tested against 1,007 SigLA words (no unsure or unidentified sign)
   on the SigLA-sourced records that also have a lineara.xyz transcription:
   cutting at every raw line break finds 690 of them, this rule finds 757,
   never cutting finds 758. The raw line breaks cut 68 words that SigLA has
   whole.
6. A run of two or more signs is a word; so is a run with a damaged edge. A lone
   undamaged sign is not (the old rule kept only hyphenated items).
7. The record gains `word_layer`, naming the layer.

Where `transcription` is empty (22 records, all sealings and roundels: HT Wa
1030, KH Wa 1014 to 1016, KH Wc 2007, 2010 to 2025, 2055) the words are kept
and `word_layer` says they come from the derived layer.

The raw layer has no doubt mark. Its characters are Linear A signs and
fraction signs, Aegean numbers, the word separator dot, the Aegean check mark
(once), line breaks, the lacuna marks U+1076B to U+1076F, spaces, the em dash,
superscript digits, U+2248, U+007C, U+002C and one Linear B sign (B043). No
combining dot below and no other doubt mark occurs. A word built here cannot say
which signs an edition dots. lineara.xyz's `items_analysis/supplement.json`
does mark signs "doubtful" (219 signs in 111 records), but its sign order
follows the derived layer, and none of the 15 register records has a mark
there.

## The result

Of 234 records: 122 words lists change, 22 are kept (raw layer empty), 90 are
unchanged. Of the 122: 58 gain damage marks only, 54 gain damage marks and
change words, 10 change words with no damage mark. Of the 114 records above,
111 change; AP Za 1 and KAM Zb 1 have their lacuna past a divider, away from
any word, and KH Wc 2025 has an empty raw layer.

Six records lose their only word, a lone vessel sign whose lineara.xyz value
carries a hyphen (`*408-vs`): KH Wc 2006, 2079, 2084, 2103, 2122, ZO 1.

`scripts/layer_check.py` now drops the edge marks before it reads a word. Its
population goes from 636 to 630 (the six records above). Class f (reading
conflict) goes from 9 to 12: HT Zd 157+156, KO (?)Zf2 and PH Zb 5, where the
raw words differ from `unicode_text`.

## Not changed

`unicode_text` equals lineara.xyz `parsedInscription` on all 1,707 records that
have both, not `transcription`. The two differ on 1,220 of them: on 883 the raw
`transcription` is empty, on 156 only the line breaks differ, and on 181 signs,
lacunae, numbers or dividers differ. Moving `unicode_text` to the raw layer is a
separate change.
