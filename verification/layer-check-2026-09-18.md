# Layer check, 2026-09-18

This note records four checks of the corpus data. It asserts no reading. Where two layers or two sources disagree, both values are recorded and neither is chosen.

Rules applied throughout: a number belongs to one layer, one population and one unit; absence in our file is not absence from the published corpus; no reading is chosen; a disagreement is recorded as data.

## 1. The 58 records short of SigLA's word count

After the pseudo-word fix, 58 of the 318 corrected records held fewer words than SigLA's own word count (SigLA document pages of 2026-08-14). The cause was a second importer defect. `import_sigla.py` kept only the `sure-reading` spans of a SigLA word page. So:

- a word page with no `sure-reading` span gave no word, and the word was lost;
- an unsure sign inside a word was dropped;
- a subscript was cut, so `ra<sub>2</sub>` became `ra`.

No held file carried SigLA's per-word pages, so the word pages of those 58 documents were fetched from sigla.phis.me on 2026-09-18: one request per second, a User-Agent that names the project and a contact, 239 pages, all HTTP 200. The raw HTML, a manifest of URL, date and sha256, and the fetch script are kept in the private companion repository.

The importer now parses every sign of a word page. The marks in a word string are:

| Mark | Meaning |
|---|---|
| `ra2` | a sure sign; a SigLA subscript is kept as a digit |
| `re?` | a sign SigLA marks unsure |
| `[?]` | a sign SigLA shows but does not identify |
| `[unclassified]` | a sign SigLA labels unclassified |

A superscript variant letter (`qi<sup>f</sup>`) names a variant of the same sign, so the string keeps `qi`. The damage brackets at a broken word edge are not signs and are not kept. The parser checks that the number of signs it reads equals SigLA's own "(N signs)" on every page.

Result: 58 of 58 records now hold SigLA's word count. Words before: 167. Words after: 239. Words added: 72. In every record the old word list survives inside the new one once unsure marks, unidentified signs and subscripts are removed, so the restore adds and never contradicts. In 5 records (HT 3, HT 37, HT 49a, KH 94, KH 97b) a sign that the old import held as sure is now marked unsure by SigLA; the sign itself is unchanged.

Script: `linear_a/apply_word_pages_2026-09-18.py`. It writes `words` in `corpus.json` and in `sources/sigla/corpus_structured.json` for those 58 records, and asserts that no other record and no other field changes. `git diff` confirms it.

| Record | Words before | Words after | Word list after |
|---|---:|---:|---|
| HT 109 | 4 | 5 | `re [?] ta ku-ro a-ra-ju` |
| HT 110a | 3 | 4 | `si-du-*34-ku-mi ku-pa ku-ro [?]` |
| HT 110b | 1 | 2 | `[?] ro` |
| HT 112a | 1 | 2 | `[?] tu-pa` |
| HT 122b | 7 | 8 | `je-di A306-ki-ta2 [?] a-ra-ju-u-de-za qa-qa-ru da-re ku-ro po-to-ku-ro` |
| HT 131a | 1 | 2 | `[?] i-qa-*118` |
| HT 131b | 1 | 2 | `[?] po-to-ku-ro` |
| HT 137 | 1 | 3 | `[?] [?] ta2` |
| HT 144 | 1 | 3 | `[?] o [?]` |
| HT 154A | 1 | 3 | `tu-me-pa-ja [?] [?]` |
| HT 154C | 1 | 2 | `na-mi [?]` |
| HT 23b | 3 | 4 | `ni-ra mu pu [?]` |
| HT 25b | 4 | 5 | `[?] ku-ro wi-te-ro i-ti ku-ro` |
| HT 26b | 4 | 5 | `[?] pa-ro-ni ka-u-*79-ni i-A308 *188-*86` |
| HT 27b | 2 | 3 | `mi-da [?]-[?] pa-se` |
| HT 3 | 9 | 11 | `ma-di? di-na qe-ra2-ja [?] mu-ru ru si-tu-ra2-re [?] ku-*56-nu ma-di da` |
| HT 33 | 1 | 2 | `[?] sa-ra2` |
| HT 37 | 7 | 8 | `ka-ki re-su-[?] [?] ki-A310-re ki-ro ka-ki a-na? [?]-qe` |
| HT 46a | 2 | 3 | `mu-ru [?] ku-ro` |
| HT 47a | 7 | 8 | `ka ku-*56-na-tu du u pi ki-da-ro [?] mi-nu-mi` |
| HT 49a | 9 | 12 | `[?]-ra2-du ta-na-ti [?] ri su-ki? [?] ti-du-ni [?]-[?] si-ra a-ru ku-*56-nu tu-su-pu2` |
| HT 49b | 4 | 7 | `ku i ta [?] ka [?] [?]` |
| HT 5 | 3 | 4 | `A307 ma-si [?]-wi-du [?]` |
| HT 53a | 2 | 5 | `[?] sa-ne [?] [?] ra` |
| HT 53b | 1 | 2 | `[?] ku-re` |
| HT 54a | 3 | 4 | `[?]-[?] ku-mi-na-qe ki mi-ra2` |
| HT 55a | 5 | 6 | `ki-ro ma-re si-ru ne tu [?]` |
| HT 70 | 1 | 2 | `qa-*118-sa [?]` |
| HT 72 | 1 | 2 | `si-*100-[unclassified] [?]-[?]` |
| HT 74 | 1 | 2 | `ku-ro [?]` |
| HT 84 | 2 | 3 | `qi-ja-du [?] nu-ti` |
| HT 98a | 7 | 8 | `[?] [?]-de tu ta-na-ti di-re-di-na te-A301 ro-ke ka-ri-A310-i` |
| KE 1 | 1 | 2 | `ka-sa [?]` |
| KH 10 | 3 | 4 | `[?] i-pa-sa-ja qa-*118 a-ki-pi-e-te` |
| KH 2 | 1 | 2 | `tu-[?] [?]` |
| KH 24 | 1 | 2 | `[?]-su [?]` |
| KH 4 | 1 | 2 | `a-du-re [?]` |
| KH 57 | 2 | 3 | `tu zo [?]` |
| KH 60 | 1 | 2 | `ra-ki-ta-na-si [?]` |
| KH 61 | 1 | 2 | `[?] ma` |
| KH 64 | 1 | 2 | `ta-[?] [?]` |
| KH 7a | 7 | 8 | `[?] i e-na-si i-ja-pa-me ta-ta qa-ti-ki se-A305 ku-[?]-ko-e` |
| KH 8 | 2 | 3 | `re-[?] [?]-ta [?]` |
| KH 86 | 2 | 3 | `re-za pi-nu [?]` |
| KH 94 | 1 | 3 | `[?] [?] za?` |
| KH 95 | 1 | 2 | `se [?]` |
| KH 97b | 2 | 3 | `se i? [?]` |
| KN 28b | 1 | 2 | `[?]-te [?]` |
| KN 32b | 4 | 5 | `[?]-te [?]-sa-pu pa [?]-ja-su [?]` |
| PH 31b | 6 | 7 | `du-ri tu-[?] ne te-ri ri-ru-ma-ti [?] a-mi-da-o` |
| PH 3a | 1 | 3 | `[?] pa-ra [?]-[?]` |
| PH 3b | 2 | 3 | `[?] to si` |
| PS Za 2 | 4 | 5 | `ta-na-i-A301-ti [?] ja-ti ja-sa-sa-ra-me re-i-ke` |
| ZA 16 | 1 | 3 | `[?]-si [?] [?]` |
| ZA 20 | 7 | 8 | `[?] du-re-za-se mi-[?]-[?] si-te-tu si-tu te-*123 ru-ma-ta-se ku-ra` |
| ZA 21b | 4 | 6 | `i-da ki sa-ri [?] [?] me` |
| ZA 26a | 3 | 4 | `si-te di-di ja-ki [?]` |
| ZA 9 | 7 | 8 | `[?]-nu-ti za-[?] [?]-ra [?] ro-si-ra a-ta-na-[?] [?]-ma-ju wi-ra-re-mi-te` |

### Still open from the same defect

- 35 further SigLA records hold no words at all while SigLA reports at least one: every word page of those documents had no `sure-reading` span. They were outside the scope of this pass, so their pages were not fetched. Records: ARKH 7, HT 112b, HT 136a, HT 142, HT 154E, HT 154G, HT 154Jb, HT 154K, HT 154M, HT 41b, HT 50a, HT 50b, HT 82, KH 35, KH 67, KH 68, KH 69, KH 70, KH 72, KH 77, KH 80, KH 81, KH 84, KH 97, KH Wa 1003, KN Wc <24a>, PH 12b, PH 18b, PH 22b, PH 25, PH 28b, PH 29a, PH 29b, PH Wc 45, ZA 25.
- The other 374 SigLA-worded records passed the word count test, but the same sure-only parse reached them. In SigLA's pages of 2026-08-14, 47 of those 374 hold at least one subscript syllabogram (such as ra2), and 81 of 374 hold at least one unsure syllabogram. Those are upper bounds on the records whose words still lack a sign mark or cut a subscript. Section 2, class t, finds 45 records where the cut subscript shows against the glyph layer.
- The same regex fills the `reading` field of the sign array (`signs`). In corpus.json 43 sign entries of type AB76 read `ra`, 11 of type AB66 read `ta` and 7 of type AB29 read `pu`: the subscript is cut there too. Not corrected here.

## 2. Cross-layer check: the glyph string against the word list

Population: every record of corpus.json with a nonempty `unicode_text` (the glyph layer, from lineara.xyz) and a nonempty `words` list (the word layer): 610 of 1,884 records. Of these, 377 take their words from SigLA and 233 from lineara.xyz. The private file holds the same glyph strings and, after its loader drops the pseudo-word, the same word lists, so these counts hold for both repositories.

Method, in `scripts/layer_check.py`: each Linear A character is read by its Unicode 16.0 name, which gives its sign number. A glyph counts as mapped only when signs.json holds an entry of that number whose `unicode` is that same character. Numerals, separators and line breaks are dropped, because the word layer never carries them. A SigLA word token takes its sign number from the record's own SigLA sign array where that is unambiguous, else from signs.json. The two sign sequences are aligned, and each difference is put in one class.

An earlier crude measure found 294 of 564 records disagreeing. It had a different population and did not name its method, so it is not comparable. The measure here is stricter: any difference at all, a damage placeholder included, counts.

Records whose two layers are identical, sign for sign: 105 of 610. Records with at least one difference: 505 of 610.
Of the 505, 377 differ only by damage (a) or by logograms, fractions and similar signs (c): their identified syllabic signs agree.

| Class | Meaning | Records, primary class | Records showing the class | Differences, sign level |
|---|---|---:|---:|---:|
| f | reading conflict: a different identified sign at the same position, both layers sure | 11 of 505 | 11 of 505 | 12 |
| d | mapping gap: a glyph with no name-verified signs.json entry, or a word token with no sign number | 31 of 505 | 31 of 505 | 41 |
| t | subscript cut by the old importer: the glyph reads ra2, the SigLA word reads ra | 39 of 505 | 45 of 505 | 50 |
| b | a sign the word layer marks unsure, present there only or read differently | 0 of 505 | 0 of 505 | 0 |
| a | damage placeholder, erasure, or a sign one layer does not identify | 353 of 505 | 400 of 505 | 1830 |
| c | logogram, fraction, numeral, ligature or separator handled differently | 60 of 505 | 315 of 505 | 1359 |
| e | same signs, different order | 0 of 505 | 0 of 505 | 0 |
| u | unexplained: an identified sign present in one layer only | 11 of 505 | 58 of 505 | 104 |
| total | | 505 of 505 | | 3396 |

A record takes one primary class by the precedence f, d, t, b, a, c, e, u, and shows every class it has. The primary column sums to the disagreeing records; the other columns do not.

### Class f: the reading conflicts

Each of these is a different identified sign at the same aligned position, with no damage in the chunk, and both layers sure. Each is confirmed in SigLA's own page of 2026-08-14, which holds the word-layer reading. Every glyph was decoded by its Unicode name.

| Record | Word layer (SigLA) | Glyph layer (lineara.xyz) | Differing position |
|---|---|---|---|
| HT 115a | `*47-nu-ra-*56` | `*47-nu-ra-ja` | *56 against ja (U+10631) |
| HT 117a | `te-*56-re` | `te-ja-re` | *56 against ja (U+10631) |
| HT 122a | `pa-ri-ne` | `pa-ta-ne` | ri against ta (U+10633) |
| HT 128a | `tu-ru-*56-se-me` | `tu-ru-nu-se-me` | *56 against nu (U+1062F) |
| HT 129 | `tu-ru-ta` | `ki-re-ta2` | tu against ki (U+10638); ru against re (U+10619) |
| HT 28a | `sa-*72` | `sa-ra2` | *72 against ra2 (U+1063D) |
| HT 6b | `du-ki` | `da-ki` | du against da (U+10600) |
| HT 95b | `da-za` | `da-me` | za against me (U+1060B) |
| KN Zc 7 | `a-ka-nu-ze-ti` | `a-ka-nu-za-ti` | ze against za (U+1060D) |
| PH Wa 32 | `su-ki-ra-ta` | `su-ki-ri-ta` | ra against ri (U+1062D) |
| ZA 15a | `A364-ke-ma-se` | `*363-ke-ma-se` | A364 against *363 (U+10697) |

11 records, 12 differing signs. PH Wa 32 already carried this conflict (see `ph-wa-32-conflict-2026-09-18.md`). The other 10 now carry a `conflicts` entry in both repositories, in the write-back shape: `ours` is the word layer, `theirs` is the glyph layer, each with its source, and the note says that no reading is chosen. Script: `linear_a/apply_layer_conflicts_2026-09-18.py`. Two notes on single records: in HT 129 the third sign is not in dispute (SigLA reads ta2; the word layer shows ta because of the cut subscript); in HT 6b SigLA's page of 2026-08-14 marks du as unsure, while the word layer, imported earlier, holds it as sure.

Records carrying `conflicts` after this pass: 16 of 1,884.

Where a differing sign sits next to damage, the position is not certain, and the check does not call it a conflict. Two cases a reader will notice are HT 52a (glyph `di-ka-ki`, then damage; SigLA `di-ka-tu`) and TL Za 1 (glyph `u-na-ka-na-si`, then damage; word layer `u-na-ka-na` and `i-pi-na-ma`). Both fall in classes a and u. The drawing decides them too.

### Class d: mapping gaps

| Unmapped item | Differences |
|---|---:|
| *100 (U+10647) | 22 |
| *131 (U+1064F) | 5 |
| *629 (U+1071D) | 4 |
| *624 (U+10719) | 4 |
| ? (U+FD1EB) | 1 |
| *707 (U+10746) | 1 |
| *568 (U+106E7) | 1 |
| *601 (U+10704) | 1 |
| *600 (U+10703) | 1 |
| *708 (U+10747) | 1 |

U+10647 is LINEAR A SIGN A100-102, the VIR sign; signs.json holds no entry with that codepoint. The word tokens cyp, d and *906 have no sign number in signs.json.

### A signs.json value to check

signs.json gives AB86 the phonetic value nwa. SigLA reads AB48 as nwa (SY Za 4, sign 9 of its sign array). The check uses the record's own SigLA sign array first, so SY Za 4 agrees, but the signs.json value is doubtful and is left for review.

### Every disagreeing record

Columns: word source; primary class; all classes; then the count of sign-level differences per class.

| Record | Words from | Primary | Classes | a | c | d | f | t | u |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| AP Za 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| AP Za 2 | lineara | a | a c | 7 | 1 | 0 | 0 | 0 | 0 |
| AR Zf 2 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| ARG Zg 1 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| ARKH 1a | sigla | a | a c | 13 | 3 | 0 | 0 | 0 | 0 |
| ARKH 1b | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| ARKH 2 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| ARKH 3a | sigla | a | a c | 11 | 10 | 0 | 0 | 0 | 0 |
| ARKH 3b | sigla | a | a c | 9 | 5 | 0 | 0 | 0 | 0 |
| ARKH 4a | sigla | a | a c | 10 | 1 | 0 | 0 | 0 | 0 |
| ARKH 4b | sigla | a | a | 10 | 0 | 0 | 0 | 0 | 0 |
| ARKH 5 | sigla | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| ARKH 6 | sigla | a | a u | 4 | 0 | 0 | 0 | 0 | 1 |
| DRA Zg 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| GO 2r | lineara | a | a c u | 7 | 6 | 0 | 0 | 0 | 1 |
| GO 2v | lineara | a | a c | 7 | 3 | 0 | 0 | 0 | 0 |
| HT 100 | sigla | t | t a c | 3 | 18 | 0 | 0 | 1 | 0 |
| HT 101 | sigla | t | t a c | 5 | 13 | 0 | 0 | 1 | 0 |
| HT 102 | sigla | d | d t a c | 2 | 4 | 1 | 0 | 1 | 0 |
| HT 103 | sigla | t | t a c | 2 | 4 | 0 | 0 | 1 | 0 |
| HT 104 | sigla | c | c | 0 | 3 | 0 | 0 | 0 | 0 |
| HT 105 | lineara | d | d a u | 3 | 0 | 2 | 0 | 0 | 2 |
| HT 106 | lineara | a | a c u | 7 | 5 | 0 | 0 | 0 | 1 |
| HT 108 | sigla | d | d t a c | 5 | 1 | 1 | 0 | 1 | 0 |
| HT 109 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| HT 10a | sigla | a | a c | 1 | 4 | 0 | 0 | 0 | 0 |
| HT 10b | sigla | c | c | 0 | 2 | 0 | 0 | 0 | 0 |
| HT 110a | sigla | a | a c | 4 | 2 | 0 | 0 | 0 | 0 |
| HT 110b | sigla | a | a c | 7 | 9 | 0 | 0 | 0 | 0 |
| HT 111a | lineara | a | a c | 9 | 2 | 0 | 0 | 0 | 0 |
| HT 111b | lineara | a | a c u | 9 | 1 | 0 | 0 | 0 | 2 |
| HT 112a | sigla | a | a c | 5 | 1 | 0 | 0 | 0 | 0 |
| HT 113 | sigla | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| HT 114a | sigla | t | t c | 0 | 5 | 0 | 0 | 2 | 0 |
| HT 115a | sigla | f | f a c | 3 | 16 | 0 | 1 | 0 | 0 |
| HT 115b | sigla | a | a c | 3 | 6 | 0 | 0 | 0 | 0 |
| HT 116a | sigla | t | t a c | 1 | 17 | 0 | 0 | 1 | 0 |
| HT 116b | sigla | a | a c | 1 | 3 | 0 | 0 | 0 | 0 |
| HT 117a | sigla | f | f | 0 | 0 | 0 | 1 | 0 | 0 |
| HT 118 | sigla | a | a c | 1 | 6 | 0 | 0 | 0 | 0 |
| HT 119 | sigla | d | d c | 0 | 2 | 1 | 0 | 0 | 0 |
| HT 11a | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| HT 11b | sigla | t | t a c | 1 | 5 | 0 | 0 | 1 | 0 |
| HT 12 | sigla | c | c | 0 | 10 | 0 | 0 | 0 | 0 |
| HT 120 | sigla | c | c u | 0 | 8 | 0 | 0 | 0 | 1 |
| HT 121 | sigla | t | t c | 0 | 6 | 0 | 0 | 2 | 0 |
| HT 122a | sigla | f | f a | 7 | 0 | 0 | 1 | 0 | 0 |
| HT 122b | sigla | d | d a c | 4 | 2 | 1 | 0 | 0 | 0 |
| HT 123+124a | lineara | a | a c | 4 | 21 | 0 | 0 | 0 | 0 |
| HT 123+124b | lineara | a | a c u | 3 | 7 | 0 | 0 | 0 | 1 |
| HT 125a | lineara | a | a c | 9 | 8 | 0 | 0 | 0 | 0 |
| HT 125b | lineara | a | a c | 4 | 5 | 0 | 0 | 0 | 0 |
| HT 126a | sigla | a | a c | 13 | 2 | 0 | 0 | 0 | 0 |
| HT 127a | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| HT 127b | sigla | a | a c | 4 | 6 | 0 | 0 | 0 | 0 |
| HT 128a | sigla | f | f a c | 7 | 6 | 0 | 1 | 0 | 0 |
| HT 128b | sigla | a | a c | 3 | 3 | 0 | 0 | 0 | 0 |
| HT 129 | sigla | f | f t a c u | 5 | 9 | 0 | 2 | 1 | 1 |
| HT 13 | sigla | a | a c | 2 | 5 | 0 | 0 | 0 | 0 |
| HT 130 | sigla | t | t a c u | 8 | 6 | 0 | 0 | 1 | 1 |
| HT 131a | sigla | a | a c | 6 | 7 | 0 | 0 | 0 | 0 |
| HT 131b | sigla | a | a c | 7 | 4 | 0 | 0 | 0 | 0 |
| HT 132 | sigla | a | a c | 3 | 4 | 0 | 0 | 0 | 0 |
| HT 133 | sigla | c | c | 0 | 2 | 0 | 0 | 0 | 0 |
| HT 135a | sigla | a | a | 8 | 0 | 0 | 0 | 0 | 0 |
| HT 135b | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| HT 137 | sigla | a | a c | 7 | 3 | 0 | 0 | 0 | 0 |
| HT 139 | sigla | t | t a c | 7 | 3 | 0 | 0 | 1 | 0 |
| HT 14 | sigla | t | t c | 0 | 11 | 0 | 0 | 1 | 0 |
| HT 140 | sigla | a | a c u | 12 | 11 | 0 | 0 | 0 | 2 |
| HT 141 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| HT 144 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| HT 146 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| HT 147 | sigla | a | a c | 6 | 3 | 0 | 0 | 0 | 0 |
| HT 15 | sigla | a | a c | 1 | 3 | 0 | 0 | 0 | 0 |
| HT 154a | lineara | a | a c | 10 | 4 | 0 | 0 | 0 | 0 |
| HT 154ja | lineara | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| HT 16 | sigla | c | c | 0 | 8 | 0 | 0 | 0 | 0 |
| HT 17 | sigla | d | d c | 0 | 2 | 1 | 0 | 0 | 0 |
| HT 18 | sigla | t | t c | 0 | 5 | 0 | 0 | 1 | 0 |
| HT 19 | sigla | c | c | 0 | 4 | 0 | 0 | 0 | 0 |
| HT 2 | sigla | a | a c | 6 | 5 | 0 | 0 | 0 | 0 |
| HT 20 | sigla | c | c u | 0 | 9 | 0 | 0 | 0 | 1 |
| HT 21 | sigla | c | c | 0 | 9 | 0 | 0 | 0 | 0 |
| HT 23a | sigla | c | c | 0 | 19 | 0 | 0 | 0 | 0 |
| HT 23b | sigla | a | a c | 7 | 8 | 0 | 0 | 0 | 0 |
| HT 24a | sigla | a | a c u | 4 | 2 | 0 | 0 | 0 | 12 |
| HT 24b | lineara | a | a c | 1 | 6 | 0 | 0 | 0 | 0 |
| HT 25a | sigla | t | t a c | 8 | 1 | 0 | 0 | 1 | 0 |
| HT 25b | sigla | d | d a | 2 | 0 | 2 | 0 | 0 | 0 |
| HT 26a | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| HT 26b | sigla | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| HT 27a | sigla | d | d a c | 7 | 9 | 2 | 0 | 0 | 0 |
| HT 27b | sigla | a | a c | 6 | 15 | 0 | 0 | 0 | 0 |
| HT 28a | sigla | f | f c | 0 | 16 | 0 | 1 | 0 | 0 |
| HT 28b | sigla | t | t a c | 1 | 9 | 0 | 0 | 2 | 0 |
| HT 29 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| HT 3 | sigla | a | a c | 17 | 2 | 0 | 0 | 0 | 0 |
| HT 30 | sigla | a | a c u | 5 | 22 | 0 | 0 | 0 | 1 |
| HT 31 | sigla | a | a c | 7 | 7 | 0 | 0 | 0 | 0 |
| HT 32 | sigla | t | t a c | 2 | 14 | 0 | 0 | 1 | 0 |
| HT 33 | sigla | a | a c | 3 | 14 | 0 | 0 | 0 | 0 |
| HT 34 | sigla | t | t a c | 5 | 18 | 0 | 0 | 1 | 0 |
| HT 35 | sigla | a | a c | 1 | 14 | 0 | 0 | 0 | 0 |
| HT 36 | sigla | a | a c | 1 | 4 | 0 | 0 | 0 | 0 |
| HT 37 | sigla | a | a c | 8 | 2 | 0 | 0 | 0 | 0 |
| HT 38 | sigla | a | a c | 2 | 7 | 0 | 0 | 0 | 0 |
| HT 39 | sigla | a | a c | 10 | 3 | 0 | 0 | 0 | 0 |
| HT 4 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| HT 40 | sigla | a | a c | 4 | 3 | 0 | 0 | 0 | 0 |
| HT 41a | sigla | a | a c | 3 | 6 | 0 | 0 | 0 | 0 |
| HT 42+59 | sigla | a | a c | 12 | 11 | 0 | 0 | 0 | 0 |
| HT 43 | sigla | a | a c | 1 | 2 | 0 | 0 | 0 | 0 |
| HT 44a | sigla | a | a c | 6 | 7 | 0 | 0 | 0 | 0 |
| HT 44b | sigla | a | a c | 8 | 4 | 0 | 0 | 0 | 0 |
| HT 45a | sigla | a | a c | 6 | 5 | 0 | 0 | 0 | 0 |
| HT 45b | sigla | a | a c | 5 | 15 | 0 | 0 | 0 | 0 |
| HT 46a | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| HT 47a | sigla | a | a c | 11 | 1 | 0 | 0 | 0 | 0 |
| HT 47b | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| HT 49a | sigla | a | a c | 16 | 5 | 0 | 0 | 0 | 0 |
| HT 49b | sigla | a | a u | 10 | 0 | 0 | 0 | 0 | 1 |
| HT 5 | sigla | a | a | 9 | 0 | 0 | 0 | 0 | 0 |
| HT 51a | sigla | a | a c | 7 | 4 | 0 | 0 | 0 | 0 |
| HT 51b | sigla | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| HT 52a | sigla | a | a c u | 5 | 1 | 0 | 0 | 0 | 1 |
| HT 52b | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| HT 53a | sigla | a | a c | 10 | 1 | 0 | 0 | 0 | 0 |
| HT 53b | sigla | a | a | 8 | 0 | 0 | 0 | 0 | 0 |
| HT 54a | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| HT 54b | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| HT 55a | sigla | a | a c | 8 | 1 | 0 | 0 | 0 | 0 |
| HT 55b | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| HT 56a | sigla | a | a c | 4 | 2 | 0 | 0 | 0 | 0 |
| HT 57a | sigla | a | a c | 6 | 1 | 0 | 0 | 0 | 0 |
| HT 58 | sigla | d | d a c u | 6 | 4 | 1 | 0 | 0 | 1 |
| HT 61 | sigla | a | a c | 3 | 1 | 0 | 0 | 0 | 0 |
| HT 62+73 | sigla | a | a c | 30 | 7 | 0 | 0 | 0 | 0 |
| HT 63 | sigla | t | t a c | 4 | 2 | 0 | 0 | 1 | 0 |
| HT 64 | sigla | a | a c | 8 | 1 | 0 | 0 | 0 | 0 |
| HT 66 | sigla | d | d a c | 7 | 1 | 1 | 0 | 0 | 0 |
| HT 67 | lineara | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| HT 68 | sigla | d | d a | 6 | 0 | 1 | 0 | 0 | 0 |
| HT 69 | sigla | a | a c | 8 | 2 | 0 | 0 | 0 | 0 |
| HT 6a | sigla | t | t c | 0 | 7 | 0 | 0 | 1 | 0 |
| HT 6b | sigla | f | f c u | 0 | 3 | 0 | 1 | 0 | 1 |
| HT 70 | sigla | a | a c | 8 | 4 | 0 | 0 | 0 | 0 |
| HT 72 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| HT 74 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| HT 75 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| HT 78 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| HT 79+83 | sigla | a | a c | 13 | 1 | 0 | 0 | 0 | 0 |
| HT 7a | sigla | d | d | 0 | 0 | 1 | 0 | 0 | 0 |
| HT 80 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| HT 81 | sigla | a | a c | 4 | 3 | 0 | 0 | 0 | 0 |
| HT 84 | sigla | d | d a | 5 | 0 | 1 | 0 | 0 | 0 |
| HT 85a | sigla | d | d a c | 2 | 1 | 1 | 0 | 0 | 0 |
| HT 85b | sigla | t | t a c | 1 | 3 | 0 | 0 | 1 | 0 |
| HT 86a | sigla | t | t c | 0 | 2 | 0 | 0 | 1 | 0 |
| HT 86b | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| HT 87 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| HT 88 | sigla | c | c | 0 | 2 | 0 | 0 | 0 | 0 |
| HT 89 | sigla | t | t a c | 1 | 8 | 0 | 0 | 1 | 0 |
| HT 8a | sigla | c | c | 0 | 7 | 0 | 0 | 0 | 0 |
| HT 8b | sigla | t | t c | 0 | 7 | 0 | 0 | 1 | 0 |
| HT 90 | sigla | t | t c | 0 | 7 | 0 | 0 | 2 | 0 |
| HT 91 | sigla | a | a c | 2 | 21 | 0 | 0 | 0 | 0 |
| HT 92 | sigla | c | c | 0 | 3 | 0 | 0 | 0 | 0 |
| HT 93a | sigla | d | d t a c u | 5 | 13 | 1 | 0 | 1 | 3 |
| HT 93b | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| HT 94a | sigla | d | d t a c | 2 | 16 | 1 | 0 | 1 | 0 |
| HT 94b | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| HT 95a | sigla | t | t c u | 0 | 1 | 0 | 0 | 1 | 1 |
| HT 95b | sigla | f | f t a | 2 | 0 | 0 | 1 | 1 | 0 |
| HT 96a | sigla | a | a c | 3 | 8 | 0 | 0 | 0 | 0 |
| HT 96b | sigla | a | a c | 1 | 6 | 0 | 0 | 0 | 0 |
| HT 97a | sigla | a | a c | 6 | 7 | 0 | 0 | 0 | 0 |
| HT 97b | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT 98a | sigla | a | a c | 4 | 5 | 0 | 0 | 0 | 0 |
| HT 98b | sigla | a | a c | 4 | 4 | 0 | 0 | 0 | 0 |
| HT 99a | sigla | t | t a c | 3 | 5 | 0 | 0 | 1 | 0 |
| HT 99b | sigla | c | c | 0 | 2 | 0 | 0 | 0 | 0 |
| HT 9a | sigla | c | c | 0 | 7 | 0 | 0 | 0 | 0 |
| HT 9b | sigla | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| HT Wa 1006 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1007 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1008 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1009 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1010 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1011 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1012 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1013 | sigla | t | t | 0 | 0 | 0 | 0 | 1 | 0 |
| HT Wa 1020 | lineara | c | c | 0 | 4 | 0 | 0 | 0 | 0 |
| HT Wa 1021 | lineara | c | c | 0 | 7 | 0 | 0 | 0 | 0 |
| HT Wa 1021bis | lineara | d | d c | 0 | 2 | 2 | 0 | 0 | 0 |
| HT Wa 1025 | lineara | d | d | 0 | 0 | 1 | 0 | 0 | 0 |
| HT Wa 1026 | lineara | c | c u | 0 | 1 | 0 | 0 | 0 | 1 |
| HT Wc 3001 | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| HT Wc 3004 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| HT Wc 3005 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| HT Wc 3009 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| HT Wc 3014 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| HT Wc 3015 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| HT Wc 3016 | lineara | d | d c | 0 | 2 | 2 | 0 | 0 | 0 |
| HT Wc 3017 | lineara | d | d c | 0 | 2 | 2 | 0 | 0 | 0 |
| HT Wc 3024 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 2 |
| HT WeWc3020 | lineara | d | d c | 0 | 2 | 2 | 0 | 0 | 0 |
| HT Zb 158a | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| HT Zb 159 | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| HT Zb 160 | sigla | t | t a | 1 | 0 | 0 | 0 | 1 | 0 |
| HT Zb 161 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| HT Zd 157+156 | lineara | a | a c u | 1 | 8 | 0 | 0 | 0 | 1 |
| IO Za 11 | lineara | a | a c | 7 | 1 | 0 | 0 | 0 | 0 |
| IO Za 12 | lineara | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| IO Za 13 | lineara | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| IO Za 14 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Za 15 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Za 16 | lineara | a | a c | 2 | 2 | 0 | 0 | 0 | 0 |
| IO Za 2 | lineara | a | a c | 6 | 1 | 0 | 0 | 0 | 0 |
| IO Za 3 | lineara | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| IO Za 4 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Za 5 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Za 7 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| IO Za 8 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Za 9 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| IO Zb 10 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KAM Zb 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KE 1 | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| KH 1 | sigla | a | a c | 4 | 3 | 0 | 0 | 0 | 0 |
| KH 10 | sigla | a | a c | 3 | 3 | 0 | 0 | 0 | 0 |
| KH 100 | sigla | a | a c u | 6 | 2 | 0 | 0 | 0 | 1 |
| KH 102 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KH 103 | lineara | a | a c | 4 | 4 | 0 | 0 | 0 | 0 |
| KH 104 | lineara | a | a c | 1 | 3 | 0 | 0 | 0 | 0 |
| KH 11 | sigla | a | a c u | 2 | 22 | 0 | 0 | 0 | 2 |
| KH 12 | sigla | a | a c | 10 | 15 | 0 | 0 | 0 | 0 |
| KH 13 | sigla | a | a c u | 13 | 4 | 0 | 0 | 0 | 2 |
| KH 14 | sigla | a | a c | 8 | 9 | 0 | 0 | 0 | 0 |
| KH 16 | sigla | a | a c | 7 | 5 | 0 | 0 | 0 | 0 |
| KH 17 | sigla | a | a c | 8 | 4 | 0 | 0 | 0 | 0 |
| KH 18 | sigla | d | d a c | 8 | 5 | 2 | 0 | 0 | 0 |
| KH 19 | lineara | a | a c | 4 | 3 | 0 | 0 | 0 | 0 |
| KH 2 | sigla | a | a c | 8 | 2 | 0 | 0 | 0 | 0 |
| KH 20 | sigla | a | a c | 5 | 6 | 0 | 0 | 0 | 0 |
| KH 21 | sigla | a | a c | 5 | 4 | 0 | 0 | 0 | 0 |
| KH 22 | sigla | a | a c | 5 | 4 | 0 | 0 | 0 | 0 |
| KH 23 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KH 24 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KH 28 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KH 29 | sigla | t | t a c | 8 | 2 | 0 | 0 | 1 | 0 |
| KH 3 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KH 32 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 33 | sigla | a | a c | 6 | 1 | 0 | 0 | 0 | 0 |
| KH 36 | sigla | a | a c | 5 | 1 | 0 | 0 | 0 | 0 |
| KH 37 | sigla | a | a c | 2 | 2 | 0 | 0 | 0 | 0 |
| KH 39 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KH 4 | sigla | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| KH 40 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 41 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 43 | lineara | a | a c | 3 | 2 | 0 | 0 | 0 | 0 |
| KH 44 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 45 | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| KH 47 | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| KH 49 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| KH 5 | sigla | a | a c | 2 | 7 | 0 | 0 | 0 | 0 |
| KH 50 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 51 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 52 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 53 | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| KH 57 | sigla | a | a c | 10 | 1 | 0 | 0 | 0 | 0 |
| KH 58 | sigla | a | a c | 12 | 7 | 0 | 0 | 0 | 0 |
| KH 59 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 6 | sigla | a | a c | 15 | 22 | 0 | 0 | 0 | 0 |
| KH 60 | sigla | d | d a c u | 9 | 4 | 1 | 0 | 0 | 1 |
| KH 61 | sigla | a | a c | 9 | 6 | 0 | 0 | 0 | 0 |
| KH 62 | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| KH 63 | sigla | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| KH 64 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 65 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 73 | sigla | a | a c | 8 | 4 | 0 | 0 | 0 | 0 |
| KH 74 | sigla | a | a u | 4 | 0 | 0 | 0 | 0 | 2 |
| KH 76 | sigla | a | a c | 6 | 3 | 0 | 0 | 0 | 0 |
| KH 79 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 79+89 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| KH 7a | sigla | a | a c u | 12 | 16 | 0 | 0 | 0 | 1 |
| KH 7b | sigla | a | a c | 3 | 7 | 0 | 0 | 0 | 0 |
| KH 8 | sigla | d | d a c | 8 | 13 | 1 | 0 | 0 | 0 |
| KH 83 | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KH 86 | sigla | a | a c | 12 | 6 | 0 | 0 | 0 | 0 |
| KH 88 | sigla | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| KH 9 | sigla | a | a c | 11 | 17 | 0 | 0 | 0 | 0 |
| KH 90 | sigla | a | a | 8 | 0 | 0 | 0 | 0 | 0 |
| KH 91 | sigla | a | a c | 11 | 12 | 0 | 0 | 0 | 0 |
| KH 92 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 94 | sigla | a | a u | 9 | 0 | 0 | 0 | 0 | 1 |
| KH 95 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KH 97a | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH 97b | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KH 99 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KH Wc 2006 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2007 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2010 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2011 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2012 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2013 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2014 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2015 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2016 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2017 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2018 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2019 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2020 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2021 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2022 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2023 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2024 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2025 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KH Wc 2079 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2084 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2103 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2114 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KH Wc 2122 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KH Wc 2123 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN 1a | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KN 1b | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KN 2 | sigla | a | a c | 3 | 2 | 0 | 0 | 0 | 0 |
| KN 22a | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| KN 22b | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN 22c | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KN 28b | sigla | a | a c | 7 | 3 | 0 | 0 | 0 | 0 |
| KN 32a | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| KN 32b | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| KN 54 | lineara | d | d a c | 6 | 1 | 1 | 0 | 0 | 0 |
| KN Wb 33 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KN Wc 3 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KN Wc 30 | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Za 10 | lineara | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| KN Za 17 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Za 18 | lineara | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| KN Za 19 | lineara | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| KN Zb 20 | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Zb 35 | sigla | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| KN Zb 4 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| KN Zb 56 | lineara | d | d c | 0 | 1 | 1 | 0 | 0 | 0 |
| KN Zb <27> | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| KN Zc 6 | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Zc 7 | sigla | f | f a | 2 | 0 | 0 | 1 | 0 | 0 |
| KN Ze 44 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Ze 56 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| KN Zf 31 | lineara | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| LACH Za 1 | lineara | c | c u | 0 | 2 | 0 | 0 | 0 | 1 |
| MA 10a | sigla | a | a c | 2 | 3 | 0 | 0 | 0 | 0 |
| MA 10b | sigla | a | a c | 2 | 4 | 0 | 0 | 0 | 0 |
| MA 10c | lineara | a | a c | 2 | 2 | 0 | 0 | 0 | 0 |
| MA 1a | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| MA 1b | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| MA 2a | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| MA 2b | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| MA 2c | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| MA 4a | lineara | d | d c | 0 | 2 | 2 | 0 | 0 | 0 |
| MA 4b | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| MA Wc <5> | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| MA Zb 15 | lineara | d | d c | 0 | 1 | 1 | 0 | 0 | 0 |
| MA Zb 8 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| MI 2 | sigla | a | a c | 9 | 1 | 0 | 0 | 0 | 0 |
| MIL Zb 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| MIL Zb 2 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| MIL Zb 3 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| MIL Zb 4 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| MY Zf 2 | sigla | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| NEZ a1 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PE 1 | lineara | d | d a c u | 2 | 3 | 2 | 0 | 0 | 2 |
| PE 2 | lineara | a | a c | 3 | 6 | 0 | 0 | 0 | 0 |
| PE Wy5 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| PE Zb | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PE Zb 7 | lineara | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| PE Zc 4 | lineara | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| PE Zg 6 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PH (?)31a | lineara | a | a c u | 9 | 7 | 0 | 0 | 0 | 2 |
| PH (?)31b | lineara | a | a c u | 9 | 3 | 0 | 0 | 0 | 5 |
| PH 10 | sigla | c | c | 0 | 3 | 0 | 0 | 0 | 0 |
| PH 12a | sigla | a | a c u | 1 | 2 | 0 | 0 | 0 | 4 |
| PH 13a | sigla | a | a c | 2 | 3 | 0 | 0 | 0 | 0 |
| PH 13b | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PH 13c | sigla | a | a c | 2 | 2 | 0 | 0 | 0 | 0 |
| PH 14a | sigla | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| PH 14b | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PH 15a | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PH 15b | sigla | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PH 16a | sigla | a | a u | 4 | 0 | 0 | 0 | 0 | 1 |
| PH 16b | sigla | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| PH 17a | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PH 17b | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PH 18a | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| PH 19 | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PH 1a | sigla | a | a c | 3 | 5 | 0 | 0 | 0 | 0 |
| PH 1b | sigla | a | a c | 4 | 4 | 0 | 0 | 0 | 0 |
| PH 2 | sigla | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PH 26 | sigla | a | a c | 2 | 4 | 0 | 0 | 0 | 0 |
| PH 27 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| PH 28a | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| PH 30 | sigla | a | a c | 5 | 1 | 0 | 0 | 0 | 0 |
| PH 3a | sigla | a | a c | 7 | 9 | 0 | 0 | 0 | 0 |
| PH 3b | sigla | a | a c | 8 | 5 | 0 | 0 | 0 | 0 |
| PH 54 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PH 7a | sigla | a | a | 9 | 0 | 0 | 0 | 0 | 0 |
| PH 7b | sigla | d | d a c | 7 | 4 | 1 | 0 | 0 | 0 |
| PH 9a | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| PH 9b | lineara | a | a c | 1 | 3 | 0 | 0 | 0 | 0 |
| PH Wa 32 | sigla | f | f | 0 | 0 | 0 | 1 | 0 | 0 |
| PH Wc 37 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| PH Wc 39 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| PH Wc 40 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| PH Wc 46 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| PH Zb 48 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PK 1 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PK 3 | lineara | a | a c | 5 | 4 | 0 | 0 | 0 | 0 |
| PK Za 10 | lineara | a | a c | 2 | 2 | 0 | 0 | 0 | 0 |
| PK Za 11 | lineara | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| PK Za 12 | lineara | a | a u | 10 | 0 | 0 | 0 | 0 | 2 |
| PK Za 14 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PK Za 15 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PK Za 16 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PK Za 17 | lineara | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| PK Za 18 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PK Za 20 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PK Za 28 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| PK Za 4 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PK Za 8 | lineara | a | a c | 4 | 1 | 0 | 0 | 0 | 0 |
| PK Za 9 | lineara | a | a c | 5 | 1 | 0 | 0 | 0 | 0 |
| PK Zb 19 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PK Zb ? | lineara | a | a c u | 1 | 1 | 0 | 0 | 0 | 1 |
| PK Zc 13 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| PL Zf 1 | lineara | a | a c | 5 | 2 | 0 | 0 | 0 | 0 |
| PR Za 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PS IZa1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| PS Za 2 | sigla | a | a u | 3 | 0 | 0 | 0 | 0 | 6 |
| PYR 1 | sigla | c | c u | 0 | 1 | 0 | 0 | 0 | 1 |
| PYR Wc 4 | lineara | a | a c | 3 | 1 | 0 | 0 | 0 | 0 |
| PYR Zb 5 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| SAM Wa 1 | lineara | a | a c u | 2 | 1 | 0 | 0 | 0 | 1 |
| SIZ g1 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| SK Zb 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| SKO Zc 1 | lineara | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| SY Za 1 | lineara | a | a c | 2 | 1 | 0 | 0 | 0 | 0 |
| SY Za 11 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| SY Za 3 | lineara | a | a u | 4 | 0 | 0 | 0 | 0 | 1 |
| SY Za 5 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| SY Za 8 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| SY Zb 7 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| TEL Zb 1 | lineara | c | c | 0 | 2 | 0 | 0 | 0 | 0 |
| THE Zb 1 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| THE Zb 13 | lineara | a | a c | 1 | 3 | 0 | 0 | 0 | 0 |
| THE Zb 3 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| THE Zb 4 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| THE Zg 16 | lineara | u | u | 0 | 0 | 0 | 0 | 0 | 1 |
| THE tab.5 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| TI Zb 1 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| TL Za 1 | lineara | a | a u | 3 | 0 | 0 | 0 | 0 | 1 |
| TRA Zb 1 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| TRY Zb 1 | lineara | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| TY 2 | sigla | d | d a u | 10 | 0 | 1 | 0 | 0 | 4 |
| TY 3a | sigla | a | a c u | 12 | 22 | 0 | 0 | 0 | 1 |
| TY 3b | sigla | a | a c | 7 | 5 | 0 | 0 | 0 | 0 |
| TY Zg 1 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| VRY Za 1 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| ZA 10a | sigla | a | a c | 1 | 1 | 0 | 0 | 0 | 0 |
| ZA 10b | sigla | t | t a c | 1 | 4 | 0 | 0 | 1 | 0 |
| ZA 11a | sigla | t | t a c | 9 | 13 | 0 | 0 | 1 | 0 |
| ZA 11b | sigla | a | a c u | 6 | 5 | 0 | 0 | 0 | 1 |
| ZA 13 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 14 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 15a | sigla | f | f c u | 0 | 5 | 0 | 1 | 0 | 2 |
| ZA 15b | sigla | c | c | 0 | 3 | 0 | 0 | 0 | 0 |
| ZA 16 | sigla | a | a c | 9 | 2 | 0 | 0 | 0 | 0 |
| ZA 18a | sigla | a | a c | 4 | 11 | 0 | 0 | 0 | 0 |
| ZA 19 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 1a | sigla | a | a c | 1 | 4 | 0 | 0 | 0 | 0 |
| ZA 1b | sigla | a | a c | 3 | 1 | 0 | 0 | 0 | 0 |
| ZA 20 | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| ZA 21a | sigla | a | a | 17 | 0 | 0 | 0 | 0 | 0 |
| ZA 21b | sigla | a | a | 7 | 0 | 0 | 0 | 0 | 0 |
| ZA 22 | sigla | a | a c | 11 | 4 | 0 | 0 | 0 | 0 |
| ZA 23 | sigla | a | a | 5 | 0 | 0 | 0 | 0 | 0 |
| ZA 24a | sigla | a | a c | 3 | 1 | 0 | 0 | 0 | 0 |
| ZA 24b | sigla | a | a | 3 | 0 | 0 | 0 | 0 | 0 |
| ZA 26a | sigla | a | a c | 6 | 2 | 0 | 0 | 0 | 0 |
| ZA 27 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 29 | sigla | a | a | 6 | 0 | 0 | 0 | 0 | 0 |
| ZA 31 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 32 | sigla | a | a | 4 | 0 | 0 | 0 | 0 | 0 |
| ZA 4a | sigla | a | a c | 15 | 1 | 0 | 0 | 0 | 0 |
| ZA 5a | sigla | a | a c u | 5 | 1 | 0 | 0 | 0 | 1 |
| ZA 5b | sigla | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| ZA 6a | sigla | t | t a c | 17 | 6 | 0 | 0 | 2 | 0 |
| ZA 6b | sigla | t | t a c | 5 | 5 | 0 | 0 | 1 | 0 |
| ZA 7a | sigla | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| ZA 7b | sigla | a | a c | 4 | 2 | 0 | 0 | 0 | 0 |
| ZA 8 | sigla | a | a c | 1 | 12 | 0 | 0 | 0 | 0 |
| ZA 9 | sigla | a | a c u | 10 | 3 | 0 | 0 | 0 | 2 |
| ZA Wc 2 | sigla | u | u | 0 | 0 | 0 | 0 | 0 | 7 |
| ZA Zb 3 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |
| ZA Zb 34 | lineara | a | a | 2 | 0 | 0 | 0 | 0 | 0 |
| ZA Zg 35 | lineara | a | a | 1 | 0 | 0 | 0 | 0 | 0 |
| ZO 1 | lineara | c | c | 0 | 1 | 0 | 0 | 0 | 0 |

## 3. Nonstandard record keys

The claims reconciliation quoted 65 of 1,881 keys with characters outside the plain GORILA pattern. The pattern behind that number was not recorded and could not be reproduced exactly. This pass uses a stated pattern: a site code of 2 to 4 capitals, an optional series (Wa, Zb ...), a space, a number, and optional lower-case face letters.

- Keys that fail the pattern: 119 of 1,884.
- Of those, keys with a character outside letters, digits and space: 77 of 1,884. (On the 1,881-key file the same test gives 75, or 66 when `+` is allowed. 66 is the closest to the quoted 65.)

Each failing key has one of three outcomes, from sources held here. No key is renamed.

| Outcome | Keys | Rule |
|---|---:|---|
| aliased | 18 of 119 | A held source gives a standard siglum for the same object: the GORILA vol. 5 concordance (the key without spaces equals a GORILA id without spaces, and the record's gorila_ref names the same volume and page), RILA-S1 (the six aliases of the write-back), or Kanta, Nakassis, Palaima and Perna 2024 (KN Zg 57 and KN Zg 58). 12 of these are new in this pass. |
| source form | 56 of 119 | The key is exactly the siglum a held source prints: a GORILA concordance id, a SigLA document id, or a RILA-S1 siglum. |
| nonstandard, unresolved | 45 of 119 | No held source establishes a standard siglum. |

Public corpus.json: each failing key carries `siglum_status` and `siglum_note`, and each aliased key carries the standard siglum in `aliases`. Private: the same two fields in docs/browser-data.json, and 4 new ID_ALIASES entries (see the private note for why the other new aliases stay out of the loader).

| Key | Outcome | Alias | Outside characters |
|---|---|---|---|
| `ANZ b1` | nonstandard, unresolved |  | no |
| `AP Za <3>` | source form |  | yes |
| `CR (?)Zf1` | aliased | `CR (?) Zf 1` | yes |
| `FOZ c1` | nonstandard, unresolved |  | no |
| `HT 113 ter` | source form |  | no |
| `HT 123+124a` | nonstandard, unresolved |  | yes |
| `HT 123+124b` | nonstandard, unresolved |  | yes |
| `HT 154.` | nonstandard, unresolved |  | yes |
| `HT 154A` | aliased | `HT 154 A` | no |
| `HT 154B` | aliased | `HT 154 B` | no |
| `HT 154C` | aliased | `HT 154 C` | no |
| `HT 154E` | aliased | `HT 154 E` | no |
| `HT 154G` | aliased | `HT 154 G` | no |
| `HT 154Ja` | source form |  | no |
| `HT 154Jb` | source form |  | no |
| `HT 154K` | source form |  | no |
| `HT 154L` | source form |  | no |
| `HT 154M` | source form |  | no |
| `HT 154N` | source form |  | no |
| `HT 42+59` | source form |  | yes |
| `HT 62+73` | source form |  | yes |
| `HT 79+83` | source form |  | yes |
| `HT W231a` | nonstandard, unresolved |  | no |
| `HT W231b` | nonstandard, unresolved |  | no |
| `HT W231c` | nonstandard, unresolved |  | no |
| `HT W231d` | nonstandard, unresolved |  | no |
| `HT W231e` | nonstandard, unresolved |  | no |
| `HT W231f` | nonstandard, unresolved |  | no |
| `HT Wa 1019α` | source form |  | yes |
| `HT Wa 1019γ` | source form |  | yes |
| `HT Wa 1020α` | source form |  | yes |
| `HT Wa 1020β` | source form |  | yes |
| `HT Wa 1020γ` | source form |  | yes |
| `HT Wa 1021α` | source form |  | yes |
| `HT Wa 1021β` | source form |  | yes |
| `HT Wa 1021γ` | source form |  | yes |
| `HT Wa 1025α` | source form |  | yes |
| `HT Wa 1025γ` | source form |  | yes |
| `HT Wa 1028α` | source form |  | yes |
| `HT Wa 1028γ` | source form |  | yes |
| `HT Wa 1029α` | source form |  | yes |
| `HT Wa 1029γ` | source form |  | yes |
| `HT Wa 1845+1733` | nonstandard, unresolved |  | yes |
| `HT Wa <1021bis>` | source form |  | yes |
| `HT Wc 3001-latus` | source form |  | yes |
| `HT Wc 3019-latus` | source form |  | yes |
| `HT Wc 3022(?)` | nonstandard, unresolved |  | yes |
| `HT Wc <3018>` | nonstandard, unresolved |  | yes |
| `HT Wd1617` | nonstandard, unresolved |  | no |
| `HT Wd1663` | nonstandard, unresolved |  | no |
| `HT WeWc3020` | nonstandard, unresolved |  | no |
| `HT Zd 157+156` | nonstandard, unresolved |  | yes |
| `HT Zf (HM767)` | nonstandard, unresolved |  | yes |
| `INZ b1` | nonstandard, unresolved |  | no |
| `IO Za <1>` | nonstandard, unresolved |  | yes |
| `KA NZa1` | nonstandard, unresolved |  | no |
| `KAZ f1` | aliased | `KA Zf 1` | no |
| `KH 68+71` | nonstandard, unresolved |  | yes |
| `KH 79+89` | source form |  | yes |
| `KH Wa 1001α` | source form |  | yes |
| `KH Wa 1001γ` | source form |  | yes |
| `KH Wa 1002α` | source form |  | yes |
| `KH Wa 1002γ` | source form |  | yes |
| `KH Wa 1013α` | source form |  | yes |
| `KH Wa 1013γ` | source form |  | yes |
| `KH Wa 1014α` | source form |  | yes |
| `KH Wa 1014γ` | source form |  | yes |
| `KH Wa 1015α` | source form |  | yes |
| `KH Wa 1015γ` | source form |  | yes |
| `KH Wa 1016α` | source form |  | yes |
| `KH Wa 1016γ` | source form |  | yes |
| `KH Wc 2059[+]2091[+]2092` | source form |  | yes |
| `KH Wc 2088[+]2089[+]fr.` | source form |  | yes |
| `KN Anetaki Scepter (Handle)` | aliased | `KN Zg 58` | yes |
| `KN Anetaki Scepter (Ring)` | aliased | `KN Zg 57` | yes |
| `KN Wc <24a>` | source form |  | yes |
| `KN Wc <24b>` | source form |  | yes |
| `KN Wc <25>` | source form |  | yes |
| `KN Zb <27>` | source form |  | yes |
| `KN Zb <36>` | source form |  | yes |
| `KN Zb <37>` | source form |  | yes |
| `KN Zb <38>` | source form |  | yes |
| `KN Zb <39>` | source form |  | yes |
| `KN Zg <21>` | source form |  | yes |
| `KN sceau` | nonstandard, unresolved |  | no |
| `KO (?)Zf2` | aliased | `KO (?) Zf 2` | yes |
| `KOZ a1` | aliased | `KO Za 1` | no |
| `LAZ b1(bis)` | nonstandard, unresolved |  | yes |
| `MA Wc <5>` | source form |  | yes |
| `MA Wc <5a>` | source form |  | yes |
| `MA Wc <5b>` | source form |  | yes |
| `MARG Wa 1-26` | nonstandard, unresolved |  | yes |
| `MOZ b2?` | aliased | `MO Zb 2 (?)` | yes |
| `MOZ b3?` | aliased | `MO Zb 3 (?)` | yes |
| `MOZ f1` | aliased | `MO Zf 1` | no |
| `NEZ a1` | nonstandard, unresolved |  | no |
| `PE Ws` | nonstandard, unresolved |  | no |
| `PE Wy5` | nonstandard, unresolved |  | no |
| `PE Zb` | nonstandard, unresolved |  | no |
| `PETS Wc` | nonstandard, unresolved |  | no |
| `PH (?)31a` | nonstandard, unresolved |  | yes |
| `PH (?)31b` | nonstandard, unresolved |  | yes |
| `PH Wc <47>` | source form |  | yes |
| `PH Wg45` | nonstandard, unresolved |  | no |
| `PH Wy42` | nonstandard, unresolved |  | no |
| `PH Zb <47>` | nonstandard, unresolved |  | yes |
| `PK Zb ?` | nonstandard, unresolved |  | yes |
| `POZ c1` | aliased | `PO Zg 1` | no |
| `PS IZa1` | aliased | `PSI Za 1` | no |
| `PS IZa2` | nonstandard, unresolved |  | no |
| `SAM We4` | aliased | `SA We 4` | no |
| `SEZ f1` | nonstandard, unresolved |  | no |
| `SIZ g1` | aliased | `SI Zg 1` | no |
| `THE fr.1` | nonstandard, unresolved |  | yes |
| `THE fr.2` | nonstandard, unresolved |  | yes |
| `THE fr.3` | nonstandard, unresolved |  | yes |
| `THE tab.4` | nonstandard, unresolved |  | yes |
| `THE tab.5` | nonstandard, unresolved |  | yes |
| `THE tab.6` | nonstandard, unresolved |  | yes |

## 4. Provenance of the data files

`linear_a/data/PROVENANCE.json` now holds one entry for each of the 62 tracked files under linear_a/data: 36 derived, 9 source transcriptions, 9 FileMaker exports, 5 documentation files, 2 code files and 1 placeholder. Each of the 54 data entries names its inputs and a generator. Only 1 of 54 has a generator script in this repository (`sources/sigla/corpus_structured.json`, from `linear_a/import_sigla.py`, whose input mirror is not held). The other 53 say hand-maintained: the script that first built them is not in this repository. Dated post-pass scripts that changed corpus.json and corpus_structured.json are listed in order.

`scripts/release_gates.py` gate 8 fails when a tracked file under linear_a/data has no entry, when a data entry names no inputs or no generator, or when a named script is missing.

Two provenance defects found on the way: `import_sigla.py` wrote to linear_a/data/corpus_structured.json, not to the path where the file lives (fixed); and `sources/sigla/PROVENANCE.md` says the FileMaker CSV files were flattened from corpus_structured.json, but fm_doc.csv holds 773 rows against 772 documents and matches the 773-record FileMaker XML export, so that statement is recorded as not confirmed.


## 5. Addendum, 2026-09-18, second pass: the rest of the sure-only parse defect

Section 1 fixed 58 records. The same sure-only parse built every other SigLA word list and the sign-array readings. This pass fixes those. It asserts no reading, and it chooses none.

### 5.1 Word pages fetched

The word pages of 409 more SigLA documents were fetched from sigla.phis.me on 2026-09-18, with the same script and the same courtesy as the first 58: one request per second, a User-Agent that names the project and a contact. 1,101 pages, 1,101 of 1,101 HTTP 200. The raw HTML is cached, and the URL, date and sha256 of each page are appended to the same manifest, in the private companion repository (1,340 pages in all, for 467 documents). The 409 documents are the 374 other worded SigLA records and the 35 SigLA records without words (section 1, "Still open").

One parser change was needed. On the word pages of HT 129 and HT 130, SigLA titles the word link "View attestations of this sequence". On every other page the title is "View othe rattestations of this sequence". `parse_word_page` now accepts both. The 58 lists of section 1 parse the same as before (checked: 0 of 58 differ).

### 5.2 The 374 other worded records

Script: `linear_a/apply_word_pages_rest_2026-09-18.py`. It writes `words` in corpus.json, and `words` in corpus_structured.json (with `word_count` where it moves). It asserts that no other field and no other record changes. For each record it asserts that the old list survives inside the new one: the new list, read with unidentified signs removed, unsure signs removed (or kept as sure) and subscripts cut, must equal the old list. A record that fails the test is class "other" and is not changed.

| Class | Meaning | Records |
|---|---|---:|
| subscript restored | a sure sign reads ra2 (ta2, pu2) where the old list read ra | 45 of 374 |
| unsure sign restored | an unsure sign (re?) or a sign SigLA does not identify ([?], [unclassified]) now stands inside a word the old list held without it | 75 of 374 |
| word added | a word the old list did not hold | 0 of 374 |
| sure now unsure | the old list held a sign as sure that SigLA now marks unsure; the sign is the same | 13 of 374 |
| other | the old list does not survive inside the new one; not applied | 2 of 374 |
| no change | the new list equals the old list | 252 of 374 |

A record can show more than one class. Records changed: 120 of 374. No word was added: every changed record holds as many words as before, and only signs inside words change. The upper bounds in section 1 were 47 of 374 (subscript) and 81 of 374 (unsure). The counts found are 45 and 75, and the 2 records in "other" also hold a subscript.

#### Class "other": not applied

| Record | Old list | SigLA word pages, 2026-09-18 | Why it fails the test |
|---|---|---|---|
| HT 129 | `tu-ru-ta qi-ri-na-AB120/GRA` | `tu-ru-ta2 A707-A702 tu-qif-ri-na A707` | SigLA now divides the document into 4 words. Its document page of 2026-08-14 counted 2, and the SigLA refresh of 2026-08-14 recorded HT 129 as the one document whose sign readings changed. The old word 2 has no counterpart. The page prints `qif` without the superscript markup that other pages use for this variant. |
| HT 130 | `sa-ra ro AB41` | `sa-ra2 ra2 ro` | The word count is the same (3), but the word AB41 is gone and a word ra2 stands second. |

Both keep their old lists until the change of word division is explained. The HT 129 conflict entry of section 2 stays as recorded.

#### Records changed

| Record | Classes | Word list after |
|---|---|---|
| ARKH 1a | unsure sign restored | `ta-pi ki a-ra a-su-mi-*118 a-pa-[?] mi-ki-sa-ne` |
| ARKH 3b | unsure sign restored | `[?]-ja-pi pi-A314` |
| ARKH 4a | unsure sign restored | `[?]-ni-ta ta a-[?]-[?]-ju de-su-[?]-*47-te pi-ti-ne-a-[?]` |
| ARKH 4b | unsure sign restored, sure now unsure | `[?]-re u de-mi i-*47 a-ki-ro za?-si-*79` |
| ARKH 6 | unsure sign restored | `da-na-tu ku [?]-ri` |
| HT 1 | subscript restored | `qe-ra2-u ki-ro *79-su di-di-za-ke ku-*56-nu a-ra-na-re` |
| HT 100 | subscript restored | `ku-ro sa-ra2` |
| HT 101 | subscript restored | `*79-*22-di sa-ra2 ku *56` |
| HT 102 | subscript restored | `ka-pa sa-ra2 *56-ni di-ri-na ma-*79 i-ka ku-ro` |
| HT 103 | subscript restored | `u-ta2 *56-da-ku-se-ne da-ku-na da-ku-se-ne ki-ra` |
| HT 108 | subscript restored, unsure sign restored | `ki-re-ta-na di-na-ro du-su-ni [?]-ra2-ti-ju` |
| HT 113 ter | unsure sign restored | `mi-[?]` |
| HT 114a | subscript restored | `ki-ri-ta2 sa-ra2` |
| HT 115b | unsure sign restored | `ru pa-ra-ne ti-nu-ja nu-wi du-*56-na ku-ru-ma A306-tu-ja a-i-[?]-[?] ku-ta` |
| HT 116a | subscript restored | `u-ta-ro ku-pa-ja pu-ra2 pi-*34-te si-ki-ne qa-nu-ma` |
| HT 11a | unsure sign restored | `a-ru-ra-[?] ka-ro-na A322-ri ku-ro a-su-ja *100-i` |
| HT 11b | subscript restored | `de-nu ru-ra2 *86 ru-*79-na sa-qe-ri ku-ro` |
| HT 121 | subscript restored | `ki-ri-ta2 sa-ra2` |
| HT 126a | unsure sign restored | `da-na-si a-na-[?] u si-di-ja u-*49 pi` |
| HT 128b | unsure sign restored | `*100-A329 ru-[?]` |
| HT 135b | unsure sign restored, sure now unsure | `[?]-*34?-ta-ne` |
| HT 139 | subscript restored, unsure sign restored | `[?]-pu-ma-ku ka-ra2` |
| HT 14 | subscript restored | `pu-*131 a-pu2-na-du` |
| HT 140 | unsure sign restored | `u-*34-si *86-si-ni je-di u-*34-si [?]-*118-ka ka-ma ka-pa` |
| HT 141 | unsure sign restored | `[?]-a-ri ru-di` |
| HT 18 | subscript restored | `pa-se sa-ra2` |
| HT 25a | subscript restored | `di-na-u ru-ni u-re-wi di-na-u a-ri-ni-ta tu-qe-nu *79-ju-pu2 du-ru-wi i-ki-ra` |
| HT 28b | subscript restored | `a-si-ja-ka u-mi-na-si sa-ra2 pu-ra2 ja-qi wi-di-na` |
| HT 30 | subscript restored | `sa-ra2 sa-ra-ra ki-ro` |
| HT 31 | unsure sign restored | `[?]-ti-sa pu-ko qa-*56 su-pu ka-ro-*56 sa-ja-ma ki-de-ma-A323-na su-*56-ra pa-ta-qe` |
| HT 32 | subscript restored | `sa-ra2 su-re` |
| HT 34 | subscript restored | `da-ju-te si-A516 sa-ra2 ki-ro` |
| HT 39 | sure now unsure | `ta-i-*123 ku-re-ju ku sa-ma-ti ku-re? ku-ro` |
| HT 4 | unsure sign restored, sure now unsure | `[?]-A306-ti-ka-a-re? [?]-du-ri-te pa-re ta-pi-si-di` |
| HT 44b | sure now unsure | `ja?` |
| HT 45b | unsure sign restored | `ku ro-[?]-a` |
| HT 51a | unsure sign restored | `ti-ni [?]-re` |
| HT 62+73 | unsure sign restored | `[?]-sa-ra [?]-na ka-ku i-ti-[?] *100-[?] ko nu ku pa-i-ki sa-ro-qe` |
| HT 63 | subscript restored | `ka-ti su-pu2 *79` |
| HT 6a | subscript restored | `ka-pa da-ta-ra pi-ta-ja A717 ma-A321 o-ra2-di-ne ka-pa-qe da-qe-ra qe-pi-ta` |
| HT 6b | unsure sign restored, sure now unsure | `wa-du-ni-mi ra-ti-se ma-ri-[unclassified]-i du-da-ma du?-ki sa-ma *56-ni-na` |
| HT 79+83 | unsure sign restored, sure now unsure | `i? ka da-*56 tu-pa-ri tu-[unclassified] ku-ni *79` |
| HT 85b | subscript restored, unsure sign restored | `ki-ki-ra-ja ki-re-ta2 qe-ka te-tu-[?] me-za re-di-se wa-du-ni-mi ma-di qa-A310-i` |
| HT 86a | subscript restored | `a-ka-ru ku-ni-su sa-ru di-de-ru qa-ra2-wa a-du da-me mi-nu-te` |
| HT 87 | unsure sign restored | `qi-tu-ne ma-ka-ri-te pi-ta-ke-si ja-re-mi di-ki-se qe-su-pu ku-ru-ku a-ra-[?]-a-tu` |
| HT 89 | subscript restored | `a-sa-ra2 ma-i-mi ta-ra ku-ro *131` |
| HT 8b | subscript restored | `su-pu2-*188 *56-*188 qa-A310-i ka-pa pa-ja-re` |
| HT 90 | subscript restored | `i-ku-ri-na sa-ra2 si-ru-ma-ri-ta2` |
| HT 93a | subscript restored, unsure sign restored | `*56-ni-na di-ri-na ki-di-ni a-se sa-ra2 qa-qa-ru *100-i de-ju-ku o-ti-[?] da-ri-da *56-ni-na pa-se-ja [?]-ka` |
| HT 94a | subscript restored | `ka-pa ku-ro sa-ra2 A318-A306` |
| HT 94b | unsure sign restored | `ki-ro tu-ma pa-ta-ne de-di ke-ki-ru sa-ru ku-ro ra-[?]-de-me-te qi-tu` |
| HT 95a | subscript restored, unsure sign restored | `da-du-ma-ta da-me mi-nu-te sa-ru ku-ni-[?] di-de-ru-qe-ra2-u` |
| HT 95b | subscript restored | `a-du sa-ru da-za mi-nu-te ku-ni-su di-de-ru qe-ra2-u` |
| HT 97a | unsure sign restored | `ka-ru ka-nu-ti pa-i-to na-ti-ma-di ta-ti de-[?] a` |
| HT 97b | subscript restored | `sa-ra2` |
| HT 99a | subscript restored | `a-du sa-ra2` |
| HT 9b | unsure sign restored | `wa-ja-pi-[?] ka-A305 pa-de a-si A306-tu A324-di-ra qe-pu ta-i-*123 di-na-u ku-ro` |
| HT Wa 1006 | subscript restored | `i-ra2` |
| HT Wa 1007 | subscript restored | `i-ra2` |
| HT Wa 1008 | subscript restored | `i-ra2` |
| HT Wa 1009 | subscript restored | `i-ra2` |
| HT Wa 1010 | subscript restored | `i-ra2` |
| HT Wa 1011 | subscript restored | `i-ra2` |
| HT Wa 1012 | subscript restored | `i-ra2` |
| HT Wa 1013 | subscript restored | `i-ra2` |
| HT Zb 158a | unsure sign restored | `[?]-tu-se-su-ki` |
| HT Zb 160 | subscript restored | `pa-ta-da du-pu2-re` |
| KH 11 | unsure sign restored | `a-du-[?]-za a-to-A349-to-i a-ta-A350` |
| KH 13 | unsure sign restored | `a-se-re-za [?]-da-i` |
| KH 16 | unsure sign restored | `u-ta-i-si ta-[?]` |
| KH 22 | unsure sign restored | `[?]-za` |
| KH 29 | subscript restored, unsure sign restored | `[?]-ra ta2-[?] ku-pa` |
| KH 3 | sure now unsure | `nu?` |
| KH 33 | unsure sign restored | `[?]-a` |
| KH 39 | unsure sign restored | `a-ta-[?]` |
| KH 40 | unsure sign restored | `si-na-[?]` |
| KH 44 | sure now unsure | `N800? A335` |
| KH 49 | unsure sign restored | `[?]-ru ku` |
| KH 50 | unsure sign restored | `[?]-ta je qe` |
| KH 73 | unsure sign restored | `[?]-[?]-a a-[?]` |
| KH 74 | unsure sign restored | `[?]-si ja-da-su si` |
| KH 79 | unsure sign restored | `[?]-pa-da` |
| KH 79+89 | unsure sign restored | `mi-na pa-ta a-ra [?]-pa-da-ni` |
| KH 90 | unsure sign restored | `[?]-ja-[?] ma-ta-ri-ta` |
| KH 92 | unsure sign restored, sure now unsure | `a-da-qi-ri ku-ni-te na-ki a?-[?]` |
| KH 99 | unsure sign restored | `pa-ri-de a-si-*118 ku-ka-[?]` |
| KN 22a | unsure sign restored | `su-ju-ta ka-je-[?]` |
| KN 22c | unsure sign restored | `ma-su-mi-[?]-na-[?]` |
| KN 32a | unsure sign restored | `a-pa-[?] a-ka-ta-[?]` |
| KN Wb 33b | unsure sign restored | `nu-se-[?]` |
| KN Zb 4 | unsure sign restored | `[?]-ju ja-si si` |
| KN Zc 6 | unsure sign restored | `*34-ti-ri a-di-da-ki-ti-pa-ku ni-ja-nu ju-ku-na-pa-ku-nu-u-[?]-i-*79` |
| KN Zc 7 | unsure sign restored | `a-ka-nu-ze-ti du-ra-re a-*79-ra ja-sa-ra-a-na-ne-wi-pi-[?]` |
| MA 2b | unsure sign restored | `[?]-re-ti ti ja-ku ti` |
| MA 4b | unsure sign restored | `a-[?]-ja` |
| PH 12a | unsure sign restored | `[unclassified]-*180-A339-*100` |
| PH 15b | unsure sign restored | `[?]-A357` |
| PH 16a | unsure sign restored | `A320-na-[?] [?]-A358-ni-[?]` |
| PH 16b | unsure sign restored | `[?]-ja-sa [?]-A320-[?]` |
| PH 18a | unsure sign restored | `[?]-wi-ja` |
| PH 1b | unsure sign restored | `[?]-na` |
| PH 26 | unsure sign restored | `[?]-A314` |
| PH 27 | unsure sign restored | `te-[?] a` |
| PH 28a | unsure sign restored | `a-*56-[?] ja-ki-*56-[?] a-ri-ja` |
| PH 30 | unsure sign restored | `[?]-ti-ri ma-re-ri-mi-de` |
| PH 31a | unsure sign restored | `[?]-a-[?] ru ma-di ku-*56-nu pa-ta-da ku-ro` |
| TY 2 | unsure sign restored, sure now unsure | `A309-[?]-*34?-pu-pi A309-[?] A309-[?]-ki-pu A309?-[?]-da-pu pa-da-ru A309-ju?-ki A309?-ri-ju? A309?-[?] A309-ri?-da-[?]-ju? A309-ri?-ka-ru A309-ri?-[?]-wa-ju? A309-ri?-ju?-[?] A309` |
| TY 3a | unsure sign restored | `za-A321 a-du-[?]-[?] a-da ko-a-du-wa a-ku-tu-A361` |
| ZA 10b | subscript restored | `wa-A362 du-re-za-se u-*49 ma-za ma-ki-de-te sa-ma a-de a-mi-ta ra2-ro-re pa-ja-re ka-ku-ne-te` |
| ZA 11a | subscript restored | `di-di-ko-ra-me-ta2 ra-ma-si e-ku-ru ku-pa pi-A310-a` |
| ZA 13 | unsure sign restored | `[?]-su-pa` |
| ZA 15a | unsure sign restored | `*47-ku-na qe-si-*79-e i-ti-ni-sa mi-za-se i-nu-ma-re si-[?]-ki ja-sa-mu mi-da-e A364-ke-ma-se` |
| ZA 19 | unsure sign restored | `ra-te-[?]` |
| ZA 1b | unsure sign restored | `e-mi-[?] ro` |
| ZA 21a | unsure sign restored | `[?]-me pi-mu ma te ta-ke pa ta-ma-pi a *118-mi` |
| ZA 31 | sure now unsure | `du?` |
| ZA 32 | sure now unsure | `ja?` |
| ZA 4a | unsure sign restored | `pi-[?]-se ja-to-ja a-ti-ru ja-pa tu-me-se qe-si-*79-e i-nu-ma-re si-pi-ki e-*82 ka-di` |
| ZA 6a | subscript restored | `A305-wa-na *34-ju-te-mi i-se i pu2-ra2 i-se` |
| ZA 6b | subscript restored | `i-ku-ju-ti-i A312-ta2 pa-za i-ma` |

### 5.3 The 35 records without words

All 35 have word pages on SigLA, so none needed `words_status: none on source (SigLA, 2026-09-18)`. Each now carries `words` and `word_source: sigla`, placed after `signs` as in every other worded record. Every sign of these words is one that SigLA does not identify or labels unclassified, which is why the sure-only parse gave nothing. Words added: 38. The word count equals SigLA's on 35 of 35.

| Record | Words |
|---|---|
| ARKH 7 | `[?]` |
| HT 112b | `[?]` |
| HT 136a | `[?]-[?]` |
| HT 142 | `[?]` |
| HT 154E | `[?]-[?]` |
| HT 154G | `[?]` |
| HT 154Jb | `[?]` |
| HT 154K | `[?] [?]` |
| HT 154M | `[?] [?]` |
| HT 41b | `[?]` |
| HT 50a | `[?]` |
| HT 50b | `[?]` |
| HT 82 | `[?]` |
| KH 35 | `[?]` |
| KH 67 | `[?]` |
| KH 68 | `[?]-[?]` |
| KH 69 | `[?]` |
| KH 70 | `[?]-[?]` |
| KH 72 | `[?]` |
| KH 77 | `[?]` |
| KH 80 | `[?]` |
| KH 81 | `[?] [?]` |
| KH 84 | `[?]` |
| KH 97 | `[?]` |
| KH Wa 1003 | `[?]` |
| KN Wc <24a> | `[unclassified]-[unclassified]` |
| PH 12b | `[?]` |
| PH 18b | `[?]` |
| PH 22b | `[?]` |
| PH 25 | `[?]` |
| PH 28b | `[unclassified]` |
| PH 29a | `[unclassified]` |
| PH 29b | `[unclassified]` |
| PH Wc 45 | `[?]-[?]-[?]` |
| ZA 25 | `[?]` |

### 5.4 Sign-array readings

Script: `linear_a/apply_sign_subscripts_2026-09-18.py`. In corpus.json and corpus_structured.json, 61 sign entries in 53 records held a reading with the subscript cut: 43 of type AB76 (`ra`), 11 of type AB66 (`ta`), 7 of type AB29 (`pu`). For each, the script reads the same occurrence (`occ-N`) on SigLA's own document page of 2026-08-14, cached as raw HTML in the private repository. It asserts that SigLA gives the same sign type and the reading `ra<sub>2</sub>` (`ta<sub>2</sub>`, `pu<sub>2</sub>`). 61 of 61 did. They now read ra2, ta2 and pu2. Only `signs[].reading` of those 61 entries changes. The one AB66 entry that reads `AB66` is not a cut subscript and does not change. The sign array also cuts SigLA's superscript variant letters (qi<sup>f</sup>, AB131/VIN<sup>a</sup> and others). A variant letter names a variant of the same sign, and this pass leaves them as they are.

### 5.5 Cross-layer check, before and after

Population after: 636 of 1,884 records (before: 610). The 26 new records are the records of 5.3 that hold a glyph string. Records whose two layers are identical: 114 of 636 (before: 105 of 610). Records with at least one difference: 522 of 636 (before: 505 of 610).

| Class | Primary, before | Primary, after | Showing, before | Showing, after | Differences, before | Differences, after |
|---|---:|---:|---:|---:|---:|---:|
| f | 11 of 505 | 9 of 522 | 11 of 505 | 9 of 522 | 12 | 9 |
| d | 31 of 505 | 31 of 522 | 31 of 505 | 31 of 522 | 41 | 41 |
| t | 39 of 505 | 0 of 522 | 45 of 505 | 0 of 522 | 50 | 0 |
| b | 0 of 505 | 1 of 522 | 0 of 505 | 2 of 522 | 0 | 4 |
| a | 353 of 505 | 402 of 522 | 400 of 505 | 429 of 522 | 1830 | 1943 |
| c | 60 of 505 | 68 of 522 | 315 of 505 | 329 of 522 | 1359 | 1395 |
| e | 0 of 505 | 0 of 522 | 0 of 505 | 0 of 522 | 0 | 0 |
| u | 11 of 505 | 11 of 522 | 58 of 505 | 54 of 522 | 104 | 111 |
| total | 505 of 505 | 522 of 522 | | | 3396 | 3503 |

Class t falls from 45 of 505 records to 0. Of the 45: 9 now agree sign for sign, 8 take primary class c, 4 take d, 1 (HT 95b) keeps its class f conflict, and 23 take class a. HT 129 and HT 130 are 2 of those 23, and they are not fixed: their word lists stay cut (class "other", 5.2). The check stopped calling them t only because the sign array now reads ra2 and ta2, so the record's own sign array no longer maps the cut word reading to AB76 or AB66. Read their classes with that in mind.

Class f falls from 11 records to 9. No new class-f conflict appears, so no `conflicts` entry is added. HT 129 leaves class f for the reason above; its conflict entry stays. HT 6b moves to class b: SigLA's word page now marks du unsure (`du?-ki`), as the note of its conflict entry already said. The entry keeps `ours: du-ki`, the word layer as it stood when the conflict was recorded. Class b appears now because unsure marks reach the word layer: HT 6b and TY 2 show it (4 differences).

Records carrying `conflicts` after this pass: 16 of 1,884 (unchanged).

### 5.6 Gates

`scripts/release_gates.py`: all 8 gates pass. Gate 6 now finds 4 records that match the pseudo-word test by coincidence, all one repeated word: HT 154K, HT 154M, HT 154N and KH 81 (before: HT 154N and KH 73; KH 73 now reads `[?]-[?]-a a-[?]`). The gate comment is updated. `linear_a/data/PROVENANCE.json` lists both new scripts as post-passes of corpus.json and corpus_structured.json.
