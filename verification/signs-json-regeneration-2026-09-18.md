# signs.json regeneration, 2026-09-18

Public file: `/Users/matt/ClaudeProjects/linear-a-public/linear_a/data/signs.json`.
Before: 386 entries, 58 with a glyph, no provenance block.
After: 402 sign entries plus one top-level `provenance` object, 334 with a glyph.

Sources, all read only:

- `/Users/matt/ClaudeProjects/linear-a-private/site/data/signs/index.json` (378 attested sign types, built 2026-09-07).
- `/Users/matt/ClaudeProjects/linear-a-private/comparative-scripts/signs-json-unicode-CORRECTED-MAP.json` (generated 2026-08-13, revision 3).
- `/Users/matt/ClaudeProjects/linear-a-private/references/inbox/sigla-tracings-2026-08-13/MANIFEST.md` (the SigLA credit line, verbatim).
- `/Users/matt/ClaudeProjects/linear-a-private/research/public-corpus-review-2026-09-18/CORPUS-DIFF.md` section 2 (the three difference lists).

## Counts

| Action | Count |
|---|---|
| Sign types added | 21 |
| Entries dropped | 5 |
| Entries kept and marked `attested: false` | 24 |
| Entries relabelled or given a `labels` object | 22 |
| Codepoints filled | 255 |
| Codepoints filled on the 21 new entries | 21 |
| Entries with `unicode: null` after the change | 68 |
| Notes reworded to remove an em dash | 2 |
| Sign entries after the change | 402 |
| Sign entries with a glyph after the change | 334 |

386 minus 5 plus 21 = 402. 58 plus 255 plus 21 = 334. 402 minus 334 = 68.

## 1. The 21 sign types added

Each one comes from the private index. `occurrences` and `documents` carry the private
`tokens` and `documents` values. The stream that supplies each count is in
`occurrences_stream` and `documents_stream`, and all six per-stream counts are in
`stream_counts`. `ws`, `gs` and `sa` below are the word stream, glyph stream and sign array
token counts.

| id | kind | occ | stream | docs | ws | gs | sa | codepoint | codepoint match |
|---|---|---|---|---|---|---|---|---|---|
| `A311` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+10661 | exact name |
| `A313a` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+10663 | exact name |
| `A313b` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+10664 | exact name |
| `A330` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+10676 | exact name |
| `A337` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+1067D | exact name |
| `A341` | unclassified | 1 | sign array | 1 | 0 | 0 | 1 | U+10681 | exact name |
| `A348` | unclassified | 1 | glyph stream | 1 | 0 | 1 | 0 | U+10688 | exact name |
| `A351` | unclassified | 1 | word stream | 1 | 1 | 1 | 1 | U+1068B | exact name |
| `A404` | unclassified | 1 | word stream | 1 | 1 | 1 | 0 | U+106A4 | unique number match |
| `A405` | unclassified | 1 | word stream | 1 | 1 | 1 | 0 | U+106A5 | unique number match |
| `A534c` | logogram | 1 | sign array | 1 | 0 | 0 | 1 | U+106CD | unique number match |
| `A663` | unclassified | 1 | glyph stream | 1 | 0 | 1 | 0 | U+10735 | exact name |
| `A664` | unclassified | 4 | glyph stream | 4 | 0 | 4 | 0 | U+10736 | exact name |
| `A712` | unclassified | 4 | glyph stream | 2 | 0 | 4 | 0 | U+1074F | unique number match |
| `A732` | unclassified | 32 | glyph stream | 25 | 0 | 32 | 0 | U+10755 | unique number match |
| `A800` | unclassified | 1 | glyph stream | 1 | 0 | 1 | 0 | U+10760 | exact name |
| `A801` | unclassified | 1 | glyph stream | 1 | 0 | 1 | 0 | U+10761 | exact name |
| `A802` | unclassified | 1 | word stream | 1 | 1 | 1 | 0 | U+10762 | exact name |
| `A805` | unclassified | 4 | glyph stream | 4 | 3 | 4 | 0 | U+10765 | exact name |
| `A806` | unclassified | 1 | glyph stream | 1 | 0 | 1 | 0 | U+10766 | exact name |
| `AB164` | unclassified | 15 | glyph stream | 16 | 3 | 15 | 0 | U+10650 | exact name |

Notes on the table.

- The private index holds `label: null` for every one of the 21. No source gives them a
  reading, so `label` is null in the public file too.
- `documents` is the any-stream document count, so `AB164` has 16 documents against 15 glyph
  stream tokens. The two numbers measure different things.
- `AB164` is the sign the old glyph generator collided with: the pre-2026-09-06 file stored
  U+10650 (LINEAR A SIGN AB164) against `AB81` (KU). `AB81` now holds U+10642 and `AB164`
  holds U+10650, so the collision is resolved on both sides.
- Six of the 21 reach us only through the SigLA tracings (`A311`, `A313a`, `A313b`, `A330`,
  `A337`, `A341`), and `A534c` is a seventh with a sign array only count.
- `A534c` takes the codepoint of the bare `A534`. Unicode does not encode the lettered
  variant. This follows the convention the corrected map already uses for `AB164a` to
  `AB164d` and for `A411a` to `A411c`.

## 2. The 29 unattested public-only ids

### Dropped, 5

| id | value | old description |
|---|---|---|
| `N1` | 1 | Single unit stroke |
| `N10` | 10 | Ten, horizontal bar or large dot |
| `N100` | 100 | Hundred, open circle |
| `N1000` | 1000 | Thousand, rayed circle |
| `N10000` | 10000 | Ten thousand (rare) |

Reason to drop. These five are not catalogue entries. Checks run for this change:

1. None of them is a `sign_id` in `linear_a/data/gorila_sign_index_rows.json` (207 distinct
   sign ids, 3,936 rows). No `N` prefixed id appears there at all.
2. None of them is a SigLA sign type. The SigLA sign type index holds 357 types and no `N`
   prefixed type. The SigLA occurrence index holds 5,145 rows and one `N` prefixed type,
   `N800`.
3. The Aegean numerals are encoded in the Aegean Numbers block at U+10100, not in the
   Linear A block, so they are not Linear A signs in Unicode either.
4. Their fields (`value`, `description`, `shape`) exist on no other entry in the file. They
   describe the numeral notation, not a sign in the catalogue.

So they are artefacts of the old inventory list. `N800` is a different case and stays: it is
a real SigLA sign type with 4 occurrences in 4 documents in the sign array, and it is in the
shared 357, not in the 29.

### Kept with `attested: false`, 24

`A171`, `A180`, `A188`, `A191`, `A309`, `AB12`, `AB14`, `AB15`, `AB25`, `AB32`, `AB33`,
`AB35`, `AB36`, `AB42`, `AB52`, `AB62`, `AB63`, `AB64`, `AB68`, `AB71`, `AB75`, `AB83`,
`AB84`, `AB91`.

Reason to keep. All 24 are real catalogue sign numbers.

- The 14 with a phonetic value (`AB12` so, `AB14` do, `AB15` mo, `AB25` a2, `AB32` qo,
  `AB33` ra3, `AB36` jo, `AB42` wo, `AB52` no, `AB62` pte, `AB68` ro2, `AB71` dwe, `AB75` we,
  `AB91` two) are standard AB series signs with an accepted Linear B value.
- The 5 with no value (`AB35`, `AB63`, `AB64`, `AB83`, `AB84`) are standard AB series
  numbers.
- `A171`, `A180`, `A188` and `A191` each have a row in the GORILA vol. 5 sign index in this
  repo, printed there as `AB 171`, `AB 180`, `AB 188` and `AB 191`.
- `A309` is the catalogue head number. GORILA vol. 5 catalogues the lettered variants
  `A309a`, `A309b` and `A309c` (rows 3608 to 3610 in this repo), and the private index
  attests all three. The bare number has no attestation of its own, so it keeps
  `attested: false` and a longer `attestation_note`. That note also records the open
  problem: `linear_a/data/corpus.json` spells 24 tokens in `TY 2` as `A309`, so the variant
  is unresolved in that document and the sign file and the corpus file disagree there.

Every other entry now carries `attested: true`, so the field is explicit for all 402.

## 3. The 22 label differences

Each of the 22 now carries a `labels` object (the SigLA reading under `sigla`, the previous
public label under `public_previous`), a `label_source` field naming the source that wins,
and a `label_note` giving the reason.

| id | SigLA | previous public | source that wins | applied |
|---|---|---|---|---|
| `AB22` | CAP | PI2 | unresolved, both kept | no change to `name` |
| `AB21m` | QI | AB21/OVIS | both, complementary | no change |
| `AB23m` | MU | AB23/BOS | both, complementary | no change |
| `AB100` | VIR | ?100 | SigLA reading | `name` and `label` set to VIR |
| `AB48` | NWA | ?48 | SigLA reading | `name` and `label` set to NWA |
| `AB123` | AROM | *123 | SigLA reading | `label` set to AROM |
| `A701` | A | A701 | SigLA reading | `label` set to A |
| `A702` | B | A702 | SigLA reading | `label` set to B |
| `A703` | D | A703 | SigLA reading | `label` set to D |
| `A704` | E | A704 | SigLA reading | `label` set to E |
| `A705` | F | A705 | SigLA reading | `label` set to F |
| `A706` | H | A706 | SigLA reading | `label` set to H |
| `A707` | J | A707 | SigLA reading | `label` set to J |
| `A708` | K | A708 | SigLA reading | `label` set to K |
| `A709` | L | A709 | SigLA reading | `label` set to L |
| `A7092` | L | A709 | SigLA reading | `label` set to L |
| `A7093` | L | A709 | SigLA reading | `label` set to L |
| `A7094` | L | A709 | SigLA reading | `label` set to L |
| `A7096` | L | A709 | SigLA reading | `label` set to L |
| `A710` | W | A710 | SigLA reading | `label` set to W |
| `A713` | Ω | A713 | SigLA reading | `label` set to Ω |
| `A717` | DD | A717 | SigLA reading | `label` set to DD |

Reasons.

- `AB22` is a value conflict, not a spelling conflict. SigLA reads the logogram CAP, and the
  corpus reading in this file is `AB22/CAP` for its one occurrence. The Linear B value of
  sign 22 is pi2, which is what the old `name` and `phonetic` carry. The sources disagree, so
  both readings stay: `labels` holds `sigla: CAP` and `linear_b_value: pi2`, and
  `label_source` is `unresolved`. Nothing is chosen.
- `AB21m` and `AB23m` are not conflicts. The SigLA label gives the base syllabogram value
  (QI, MU) and the public `primary_reading` gives the ligature (`AB21/OVIS`, `AB23/BOS`).
  Both are kept and `label_source` is `both`.
- `AB100`, `AB48` and `AB123`: the old public labels `?100`, `?48` and `*123` are a
  placeholder and a catalogue number, not readings. VIR, NWA and AROM are the accepted
  values, so the SigLA reading wins. `primary_reading` is unchanged, so `*123` is still
  recorded.
- `A701` to `A717`: the public file repeated the catalogue id as the reading, which is not a
  reading. SigLA assigns a single letter to each, so the SigLA reading wins for the `label`
  field and the catalogue id stays in `primary_reading`. `A7092`, `A7093`, `A7094` and
  `A7096` all carry the SigLA label `L`, and the public file gave all four the
  `primary_reading` `A709`, so no source separates the four variants by reading. The
  `label_note` on each records that.

## 4. Codepoints filled, 255

Method. For each of the 255 ids in the `missing` list of the corrected map, the codepoint was
decoded with Python `unicodedata` 16.0.0. The entry was written only when the character name
starts with `LINEAR A SIGN` and then carries the same sign series (`A`, `B` or `AB`) and the
same sign number as the id, after leading zeros are folded. This is the rule the
2026-09-06 fix used. Result: 255 verified, 0 refused, 0 guessed. Each filled entry now
carries `unicode` (the character), `unicode_codepoint` and `unicode_name`.

Post-change check over the whole file: 334 entries hold a glyph, and all 334 decode to a
Unicode name carrying their own sign series and number. 0 mismatches.

Ten of the 255 have a sign id with a variant letter that the Unicode name does not carry, so
they take the codepoint of the base sign. This is the corrected map's own suffix-insensitive
fallback, recorded here so nobody reads the glyph as variant specific: `A411a`, `A411b` and
`A411c` (all to LINEAR A SIGN A411-VAS), `AB120b` (to AB120), `AB131c` (to AB131A),
`AB164a`, `AB164b`, `AB164c` and `AB164d` (all to AB164), `AB28b` (to AB028).

Five codepoints are therefore shared by more than one id: U+1065D (`A309a`, `A309`),
U+106AB (`A411`, `A411a`, `A411b`, `A411c`), U+10649 (`AB120`, `AB120b`), U+1064D (`AB131`,
`AB131a`, `AB131c`), U+10650 (`AB164a`, `AB164b`, `AB164c`, `AB164d`). The new `AB164` entry
takes U+10650 as well, on the exact name match.

### The 68 entries with `unicode: null` after the change

The corrected map lists 73 ids as genuinely not encoded in Unicode. Five of those 73 are the
dropped numerals, which leaves 68. The map has no codepoint for any of them, so all 68 stay
null. No value was guessed.

`A1000`, `A1001`, `A171`, `A180`, `A188`, `A191`, `A507`, `A514`, `A517`, `A518`, `A519`,
`A522`, `A533`, `A543`, `A546`, `A558`, `A560`, `A561`, `A562`, `A567`, `A590`, `A593`,
`A597`, `A599`, `A605`, `A607`, `A625`, `A630`, `A631`, `A632`, `A633`, `A635`, `A636`,
`A639`, `A641`, `A647`, `A650`, `A684`, `A7092`, `A7093`, `A7094`, `A7096`, `A718`, `AB100`,
`AB12`, `AB130`, `AB14`, `AB15`, `AB25`, `AB302`, `AB32`, `AB33`, `AB35`, `AB36`, `AB42`,
`AB43`, `AB52`, `AB62`, `AB63`, `AB64`, `AB68`, `AB71`, `AB72`, `AB75`, `AB83`, `AB84`,
`AB91`, `N800`.

`AB25` and `AB75` are in this list. The 2026-09-06 fix set both to null because Unicode
Linear A has no codepoint for them. That decision stands.

## 5. Em dashes removed, 2

Both were in a `gorila_index_hand_resolution_note`. The old text is shown with `[U+2014]` in place of the character.

| id | old text, shortened | new text, shortened |
|---|---|---|
| `A506` | `ref HT 101.3¹ [U+2014] exact corpus attestation match` | `ref HT 101.3¹. That is an exact corpus attestation match` |
| `A684` | `(3,936 rows) [U+2014] string "684" does not appear` | `(3,936 rows). The string "684" does not appear` |

A grep for the em dash character over the whole file now returns 0 lines.

## 6. The provenance object

`provenance` is the first top-level key. It holds:

- `sources`: SigLA (CC BY-NC-SA 4.0, with the credit line copied verbatim from the tracings
  manifest), GORILA vol. 5 sign index (Godart and Olivier 1985), Younger 2024, and the
  Unicode 16.0 Linear A block with the decode rule.
- `private_index_built`: 2026-09-07, and `private_index_sign_types`: 378.
- `streams`: what the word stream, the glyph stream and the sign array each are.
- `denominators`: the per-stream totals, including `documents_with_any_sign` 1,817,
  `word_stream_documents` 666, `glyph_stream_documents` 1,707, `sign_array_documents` 788 and
  `corpus_documents` 1,880.

Every other top-level key is a sign id, and no sign id can be the string `provenance`, so
lookups by id are unaffected.

## 7. Validation

- `json.load` on the file: passes. 403 top-level keys, 402 sign entries plus `provenance`.
- Glyph decode check: 334 glyphs, 0 mismatches.
- `attested: false` count: 24. Every other entry carries `attested: true`.
- Em dash count: 0.
- Consumers. A grep for `signs.json` over the repo finds one script that reads it,
  `scripts/build_sign_behavior_atlas.py`. It loads the file with `json.load` and reads it only
  by `signs_data.get(id)`, so the new `provenance` key cannot reach its output. The script
  runs to completion after the change. `linear_a/data/sign_behavior_atlas.json` names
  signs.json in its own metadata but is a derived file, not a reader. The other hits are
  prose in `README.md` and in the 2026-09-06 verification note.
- The atlas file is not rebuilt in this commit. A rebuild sets `category` to
  `unclassified` on 9 atlas rows that now match a sign entry, and it also reorders equal
  counts inside `site_distribution` on rows this change does not touch. That reordering comes
  from the committed file, not from this change, so the rebuild belongs in its own commit.
