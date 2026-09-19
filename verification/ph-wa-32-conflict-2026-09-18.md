# PH Wa 32, a reading conflict recorded

`PH Wa 32` is the sixth record in `linear_a/data/corpus.json` to carry a
`conflicts` entry. The first five came with the private write-back of
2026-09-18, and `verification/private-writeback-2026-09-18.md` records them.
This note records the sixth.

No reading is chosen. The rule is the one the earlier pass states: where two
sources disagree, both readings are recorded and neither is picked.

## How it was found

An outside agent audited the pre-release claim list against this repository
alone. One of its findings was that a local search returning zero is not a
demonstration that a form is unattested. The claim under audit said
`su-ki-ri-ta` has zero attestations. The zero was a zero in this project's own
normalised word layer. The form is attested in a published source.

## What the sources give

| Source | Reading at `PH Wa 32` |
|---|---|
| Younger, section 10c | `SU-KI-RI-TA`, listed as `SU-KI-RI-TA (PH Wa 32; KN 9 occurrences)` |
| lineara.xyz, record `PHWa32` | `SU-KI-RI-TA` |
| SigLA, through this project's import | `su-ki-ra-ta` |

Younger was read in the Internet Archive copy dated 2024-01-25, fetched
2026-09-18. lineara.xyz was fetched 2026-09-18.

## What this corpus stored

| Field of `PH Wa 32` | Value | Decodes to |
|---|---|---|
| `unicode_text` | four codepoints, listed below | `su-ki-ri-ta` |
| `signs` | AB58, AB67, **AB60**, AB59 | `su-ki-ra-ta` |
| `words` | `su-ki-ra-ta` | `su-ki-ra-ta` |
| `word_source` | `sigla` | |

The glyph string decodes sign by sign:

| Codepoint | Unicode name | Value in `signs.json` |
|---|---|---|
| U+10632 | LINEAR A SIGN AB058 | `su` |
| U+10638 | LINEAR A SIGN AB067 | `ki` |
| U+1062D | LINEAR A SIGN AB053 | `ri` |
| U+10633 | LINEAR A SIGN AB059 | `ta` |

The whole disagreement is one sign in third position: `AB53` (*ri*) in the
glyph string against `AB60` (*ra*) in the sign array. `signs.json` gives
`AB53` = `ri` and `AB60` = `ra`.

So the record contradicts itself. The glyph string agrees with Younger and with
lineara.xyz. The sign array and the word string agree with SigLA.

## How it was applied

Script: `linear_a/apply_ph_wa_32_conflict_2026-09-18.py`.
Source read: the private `docs/browser-data.json`, read only, at the path given
as the first argument.
File written: `linear_a/data/corpus.json`, and nothing else.

```
python3 linear_a/apply_ph_wa_32_conflict_2026-09-18.py \
    /path/to/linear-a-private/docs/browser-data.json
```

The first write-back script refuses to run twice, by design, so this is a
second dated script rather than an edit to the first. It uses the same
mechanism: it checks every value it expects to find before it changes anything,
it asserts afterwards that no record and no field outside its own declared list
changed, and a second run stops with an error.

`--check` reports and writes nothing.

## Diff summary

| Measure | Value |
|---|---:|
| Records before | 1,884 |
| Records after | 1,884 |
| Records added | 0 |
| Records removed | 0 |
| Records changed | 1 |
| Fields touched | `conflicts` |
| Records carrying `conflicts`, after | 6 |

The six are `ARKH Zc 8`, `KH Zc 106`, `PH Wa 32`, `PS IZa1`, `SKO Zc 2` and
`THE Zb 15`.

## What is still open

The reading. This project holds no facsimile check on `PH Wa 32`. Settling
which sign stands in third position needs the drawing, not another database.
Until then the record carries both readings and asserts neither.
