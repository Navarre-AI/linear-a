# Private write-back, 2026-09-18

The private companion repository holds the canonical data. On 2026-09-18 a
write-back pass loaded RILA Supplement 1 and the SigLA refresh of 2026-08-14
into that canonical file. This note records the subset of those facts that is
now in the public corpus, and how it was applied.

Script: `linear_a/apply_private_writeback_2026-09-18.py`.
Source read: the private `docs/browser-data.json`, read only, at the path given
as the first argument.
File written: `linear_a/data/corpus.json`, and nothing else.

```
python3 linear_a/apply_private_writeback_2026-09-18.py \
    /path/to/linear-a-private/docs/browser-data.json
```

The script prints a diff summary and then asserts that no record and no field
outside its own declared list changed. It also checks the value it expects to
find before each change, so a second run stops with an error.

## Diff summary

| Measure | Value |
|---|---:|
| Records before | 1,881 |
| Records after | 1,884 |
| Records added | 3 |
| Records changed | 25 |
| Records verified and not changed | 7 |
| Records removed | 0 |

Fields touched: `aliases`, `conflicts`, `period`, `sc_note`, `sign_count`,
`signs_note` (deleted on one record), `unpublished`, and the `rila` sub-fields
`companion_fragment`, `companion_source`, `joined_into`, `period`,
`period_certainty`, `period_note`, `period_source`, `siglum`, `siglum_source`,
`unpublished_note`, `unpublished_source`.

Three field names are new to this file: `aliases`, `conflicts` and `rila`.
Two more, `sc_note` and `unpublished`, are new as well. Every one carries data
that a source states. None of them resolves anything.

## 1. PH 26: sign count 7 to 2, and the note deleted

The public file held `sign_count: 7` and a `signs_note` saying the count was
"corrected to 7 per SigLA unicode_text". That was a count of the glyph string,
not a count of signs.

The glyph layer of PH 26 decodes by codepoint as two damage placeholders
(U+1076B), one syllabogram (A314), and four fraction signs (A704, A712, A712,
A712). SigLA annotates neither the lacuna marks nor the fractions as signs. The
SigLA live scrape of 2026-08-14 states `sign_count: 2` for PH 26 and lists
exactly two signs: an uncertain syllabogram at position 1 and A314 at position
2. The private value of 2 therefore agrees with the source, and the public 7
did not.

`sign_count` is now 2. The stale `signs_note` is deleted. A new `sc_note`
records the previous value, the source and the reason, so the correction is
readable from the data.

The glyph-slot count is a different measure and is still available: it is the
length of `unicode_text`.

## 2. HT 129: sign count 15 to 16

The SigLA refresh of 2026-08-14 raised the count from 15 to 16, and SigLA lists
all 16. This is not the case of a header count that the page does not support.
SigLA inserted the fraction A707 at position 5, and every later sign moved down
one, so the document now carries two A707. `sc_note` records the previous
value, the source and the mechanism. `words` is untouched, because the change
is a fraction sign and the word stream carries no fractions.

## 3. The six garbled sigla

Six record keys are garbled spellings. The keys are unchanged, so no lookup
breaks. Each record now carries `aliases`, a list holding the correct RILA
Supplement 1 siglum, and `rila.siglum` with `rila.siglum_source`.

| Key, unchanged | `aliases` and `rila.siglum` |
|---|---|
| `POZ c1` | `PO Zg 1` |
| `MOZ f1` | `MO Zf 1` |
| `MOZ b2?` | `MO Zb 2 (?)` |
| `MOZ b3?` | `MO Zb 3 (?)` |
| `PS IZa1` | `PSI Za 1` |
| `SAM We4` | `SA We 4` |

Source: the RILA Supplement 1 Concordance museographique, through the private
`research/corpus-gap-verification-2026-08-02.md` section 5.1.

The key repair on `PS IZa1` repairs the spelling only. Whether the object is
Pseira `PSE Zb 1` or a Psykhro document with a spurious alias is still open, and
that is recorded as a conflict on the record in section 6 below, so the repair
cannot be read as a resolution.

Eight further garbled keys are still unadjudicated and were not touched:
`ANZ b1`, `FOZ c1`, `INZ b1`, `KAZ f1`, `LAZ b1(bis)`, `NEZ a1`, `SEZ f1`,
`SIZ g1`.

## 4. Periods for eight records

Every RILA Supplement 1 period is recorded in `rila.period`, with
`rila.period_certainty` and `rila.period_source`. The flat `period` field was
written only for a period the source states, and only where `period` was empty
or `unknown`. Nothing was overwritten.

| Record | `period` before | `period` after | `rila.period` | Certainty |
|---|---|---|---|---|
| `POZ c1` | `LM IIIA` | `LM IIIA` | `LM IIIA` | stated |
| `KH Zc 106` | empty | `LM IIIA` | `LM IIIA` | stated |
| `PK Zb 24` | empty | `LM IIIA` | `LM IIIA` | stated |
| `ARKH Zc 8` | `MM IA` | `MM IA` | `Protopalatial` | stated |
| `KN 49` | empty | `Protopalatial` | `Protopalatial` | stated |
| `PH Wa 52` | `MM II` | `MM II` | `Protopalatial` | stated |
| `SAM Wa 1` | `MM II` | `MM II` | `Protopalatial` | possible |
| `SAM We4` | empty | empty | `Protopalatial` | possible |

`SAM We4` keeps an empty `period`, because a possible period is not a period to
assert. `ARKH Zc 8` keeps `MM IA`, and the disagreement with RILA Supplement 1
is recorded as a conflict rather than resolved: `MM IA` is Prepalatial, so the
two statements cannot both be right.

Three finer statements sit in `rila.period_note` instead of in `period`:
`KH Zc 106` is `LM IIIA1` in the RILA concordance row, which our own
verification marks uncertain; `PK Zb 24` is called securely LM IIIA1 in the
digest; and `KN 49` is `MM IIA` in the SigLA refresh, which sits inside
Protopalatial, so the two agree.

## 5. The two Khania joins

Two join records were added, under the sigla that RILA Supplement 1 gives them.

| New record | `join_of` |
|---|---|
| `KH Wc 2059[+]2091[+]2092` | `KH Wc 2059`, `KH Wc 2091`, `KH Wc 2092` |
| `KH Wc 2088[+]2089[+]fr.` | `KH Wc 2088`, `KH Wc 2089` |

Each carries site Khania, type roundel, `sign_count: 0`, empty `words`, no
glyph layer, `unread: true` and `sources: ["rila_s1"]`. No reading and no glyph
layer is entered: RILA Supplement 1 carries no plates and this project holds no
facsimile of either joined object.

The five component records stay, and each gained `rila.joined_into`, so the join
is readable from both ends.

Known consequence, reproduced on purpose. Each joined object now appears under
two id schemes, exactly as `HT 123a` and `HT 123b` sit beside `HT 123+124a` and
`HT 123+124b` today. Following the existing convention keeps one convention.
A later pass must fix all of these rows together, and this is not that pass.

## 6. Five conflicts, recorded and not resolved

`conflicts` is a list of objects. Each object names the field, our value, their
value, our source, their source, and a note. No conflict is decided here.

| Record | Field | Ours | Theirs |
|---|---|---|---|
| `KH Zc 106` | `words` | `sa-sa-ra-me`, final sign AB013 | `]...-sa-sa-ra-mi`, final sign AB073 |
| `THE Zb 15` | `words` | `re-sa`, then the numeral 2 | `AB09-A332`, then the numeral 2 |
| `PS IZa1` | `site` | Psykhro | Pseira |
| `ARKH Zc 8` | `period` | `MM IA` | Protopalatial |
| `SKO Zc 2` | `id` | `SKO Zc 1` carries two lines | RILA splits the text over two records |

The `KH Zc 106` dispute is one sign in final position. RILA Supplement 1 itself
flags the reading uncertain and prints two variants, and its initial `ja-` is a
restoration, not an observation. The `THE Zb 15` readings agree on the numeral
and on three elements and disagree on both syllabograms.

The `ARKH Zc 8` and `SKO Zc 2` conflicts are not on the three-record list this
pass was asked for. They are included because they belong to the two items that
were: the `ARKH Zc 8` conflict is what the period item produced, and the
`SKO Zc 2` conflict came with the new record. Recording them is what stops
either change from reading as an answer.

## 7. SKO Zc 2, added

The one document of RILA Supplement 1's 107 that this dataset did not hold.

| Field | Value |
|---|---|
| `site` | `Skoteino Cave`, the spelling `SKO Zc 1` already uses |
| `type` | `clay_vessel` |
| `sign_count` | 0 |
| `words` | empty |
| `unread` | true |
| `sources` | `["rila_s1"]` |
| `rila.support` | painted inscription on a clay vessel, fragment of a chalice; the same object as `SKO Zc 1` |
| `rila.repository` | Knossos Stratigraphical Museum, inv. `Sko 187` |
| `rila.editio_princeps` | Perna, Kanta and Tyree 2005 |
| `rila.period_certainty` | uncertain |

The support is a clay vessel, not a stone vessel. The RILA facsimile lemma is
printed in the section on painted inscriptions on clay vessels, and `Zc` is the
class "painted on clay vases" in RILA's own classification table.

No reading is entered. `rila.note` records that the RILA Index des signes shows
a shape like `]...-67-37[`, that the two candidates `qa-ki-ti[` and `de-ki-ti[`
cannot be separated from the plain-text extraction, that this project does not
hold the editio princeps, and that no reading may be minted from the index
alone.

`SKO Zc 1` gained `rila.companion_fragment`, because the two are fragments of
one chalice under one inventory number. Whether the single `SKO Zc 1` record
already holds what RILA splits in two needs autopsy of plates that RILA
Supplement 1 does not contain, and that is the conflict in section 6.

## 8. Four unpublished texts

`KN Zg 57a`, `KN Zg 57b`, `KN Zg 58` and `THE Zg 16` now carry
`unpublished: true`, with `rila.unpublished_source`. RILA Supplement 1 lists all
four in its section on texts awaiting publication.

Nothing was deleted. `KN Zg 57a` and `KN Zg 57b` hold identical
placeholder-only glyph layers for one unpublished text, and that is recorded in
`rila.unpublished_note`. `THE Zg 16` carries a reading, `i-ki-ru-qe`, for a text
RILA states is unpublished. The reading is flagged, not removed, and the note
says so.

## 9. Seven sign counts verified, not changed

On these seven records the public file was already ahead of the private one, and
the private write-back brought the private file into agreement. The script
checks all seven on both sides and refuses to run if any disagrees. None was
written.

| Record | `sign_count` |
|---|---:|
| `HT 22` | 3 |
| `HT 33` | 18 |
| `HT 89` | 21 |
| `HT 94a` | 27 |
| `KH Wc 2047` | 2 |
| `KH Wc 2057` | 2 |
| `KH Wc 2065` | 2 |

In each case SigLA's header states a count one higher than the signs the SigLA
page lists, so one position is stated and never listed. That is the opposite
case to `HT 129`, where SigLA lists all 16.

## What this pass did not do

- The `HT 123` against `HT 123+124` duplicate-row problem. Untouched. The two
  new join records reproduce it.
- The 19 unloaded SigLA documents, including the eight face-level records. Sign
  type `A534c` still has no attestation in any corpus record, because its only
  attestation is `THE 8`, one of those eight.
- The `PS IZa1` site question, Pseira against Psykhro. Recorded, not resolved.
- The `SA We 3` to `SAM Wa 1` key alias. Not in this pass.
- Reading conflicts beyond the five recorded here.
