# Errata

Corrections to `linear_a/data/corpus.json` made by hand from the printed editions, newest first.
Each entry in `linear_a/data/corrections.json` holds the edition, page, crop image, the sign-by-sign
transcription, the old and new words, and any alternative reading with who holds it. No alternative
is chosen: `words` holds one list, the alternatives stay in `corrections.json`.

Words convention: `]` before or `[` after a word marks a lacuna at that edge; a restored sign is not
written; a trailing `?` on a value marks a sign the edition dots (the convention the SigLA-sourced
words already use). Applied by `linear_a/apply_hand_corrections_2026-10-15.py`.

## 2026-10-15: nine records whose lineara.xyz raw transcription is itself wrong

Found by Andrea Catino's register of differences (2026-10-14, ORCID 0009-0005-4157-5163) and checked on the page. The raw-layer
rebuild of the same day (`verification/lineara-raw-words-2026-10-15.md`) could not fix these,
because the error is in lineara.xyz's raw glyphs.

| Record | Edition (page) | Old words | New words | Alternatives (held by) |
|---|---|---|---|---|
| PK Za 8 | GORILA IV (Godart, Olivier 1982) p. 26; GORILA V (Godart, Olivier 1985), sign index p. 150, 154, 158, 167, 170, 191, 198, 203, 205, 217, 225, 226, 228, 249 | `]nu pa3-e ja-di-ki-te-te-*307-pu2-re tu-me-i ja-sa[ ]u-na-ka-na-si[ ]i-pi[` | `]nu pa3-e? ja-na-ki-te-te-du?-pu2?-re tu-me-i ja-sa[ ]u-na-ka-na-si?[ i-pi?[` | `ja-na-ki-te-te-ku?-pu2?-re` (GORILA IV p. 26) |
| PK Za 27 | RILA Supplement 1 (Del Freo, Zurbach 2024) p. 80 | `ja-sa-sa-ra-me u-na-ka-na-si` | `ja-sa?-sa?-ra-me u?-na-ka[` | `u?-na-ka-na?[` (RILA Supplement 1 p. 80) |
| PK Za 28 | RILA Supplement 1 (Del Freo, Zurbach 2024) p. 81 | `]pu2-re *418+l2[` | `]pu2-re` | `]du?-pu2-re` (RILA Supplement 1 p. 81) |
| IO Za 2 | GORILA V (Godart, Olivier 1985) p. 19; GORILA V (Godart, Olivier 1985), sign index p. 142, 150, 151, 155, 158, 167, 170, 188, 190, 204 | `a-ta-i-*301-wa-ja ja-di-ki-tu-tu ja-sa-sa-ra[ ]me u-na-ka-na[ ]si[ ]i-pi-na-ma si-ru-te ta-na-ra-te-u-ti-nu i[` | `a-ta-i-*301-wa-ja ja-di-ki-tu ja-sa-sa-ra[ ]si i-pi-na-ma si-ru-te ta-na-ra-te-u-ti-nu i-da[` | none printed |
| IO Za 9 | GORILA V (Godart, Olivier 1985) p. 33; GORILA V (Godart, Olivier 1985), sign index p. 155, 167, 197, 228, 258 | `ja-sa-sa[ ]ra-me u-na-ka[ ]na-si` | `u?-na-ka[ ja-sa-sa[` | none printed |
| IO Za 16 | Karetsou, Godart, Olivier, Minos 37-38 (2002-2003) p. 443, 445-446 n. 26; RILA Supplement 1 (Del Freo, Zurbach 2024) p. 77 | `]arom ja-sa-sa-ra u-na-ru-ka[ ]na-si` | `]*123 ja-sa-sa-ra-me? u-na-ru-ka[` | none printed |
| SY Za 2 | GORILA V (Godart, Olivier 1985) p. 65; GORILA V (Godart, Olivier 1985), sign index p. 154, 155, 162, 209, 229, 258, 276, 284 | `a-ta-i-*301-wa-ja ja-su-ma-tu-oliv u-na-ka-na-si-ole a-ja` | `a-ta-i-*301-wa-ja ja-su-ma-tu u-na-ka-na-si a-ja` | none printed |
| SY Za 3 | RILA Supplement 1 (Del Freo, Zurbach 2024) p. 83; GORILA V (Godart, Olivier 1985) p. 67 | `a-ta-i-*301-wa[ ]ja[ ]se-ka-na-si[ ]te[ ]si-ru-te` | `a-ta?-i?-*301?-wa[ ]se?-ka-na[ ]si-ru-te` | `a-ta-i-*301-wa[ ]si-ru-te` (GORILA V p. 67 (before the joins)); `]se?-ka-na-i?[` (RILA Supplement 1 p. 83) |
| THE Zg 16 | Del Freo, Rapport 2016-2021, Ariadne Suppl. 5 (2024) p. 106 | `i-ki-ru-qe` | `]qe i-ki?-ru-qe` | none printed |

Not settled on the page (details in `corrections.json`, field `unsettled`):

- PK Za 28: the last sign is printed as unidentified; the candidates in the apparatus carry no sign numbers. No word is written for it.
- SY Za 3: GORILA V p. 67 and RILA Supplement 1 p. 83 differ (RILA adds two fragments and dots TA, I and *301). `words` follows RILA because it covers the joined object; GORILA's reading is kept as an alternative.
- SY Za 2: OLIV and OLE are indexed by GORILA as isolated logograms, so they are not in `words`. Godart and Olivier (2003, n. 26) say each could be a phonogram (AB 27, AB 09).
- Editions cited by the register and not held: Knappett, Del Freo, Zurbach 2017 (PK Za 27); Megistos Kouros (PK Za 28); Muhly, Olivier 2008 (SY Za 2, 3); Kadmos 1985 p. 127 (IO Za 9).
