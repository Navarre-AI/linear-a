# signs.json glyph fix, 2026-09-06

Public file: `/Users/matt/ClaudeProjects/linear-a-public/linear_a/data/signs.json` (386 signs, 60 with a glyph before the fix).

Source (verified sign table): `/Users/matt/ClaudeProjects/linear-a-private/comparative-scripts/signs-json-unicode-CORRECTED-MAP.json` (generated 2026-08-13, revision 3).

Cross-checks: `/Users/matt/ClaudeProjects/linear-a-public/SIGN-VERIFICATION-2026-06-13.md` (FAIL-wrong=45, OK=15) and an independent decode of every stored glyph with Python `unicodedata` 16.0.0 against the official Unicode names (45 wrong, 15 correct). All three agree.

Root cause: the glyph column was generated as `0x10600 + (n-1)`. That formula ignores the variant signs (AB021F, AB022F, AB022M, AB023M, A028B, and others) that sit between the base signs in the Unicode block. Every glyph after the first gap points at a higher sign.

**Result: 45 changed of 386 signs.** 43 codepoints remapped. 2 set to null: AB25 and AB75 have no codepoint in Unicode Linear A, and the stored glyphs were AB026 and A120B. The phonetic `name` field was correct in every case and is unchanged. The 15 correct glyphs (AB01 to AB11, AB24, AB29, AB30, AB31) are unchanged. The 326 signs with no glyph are unchanged. The source map lists 255 of them as encoded in Unicode but missing from the file. That is a separate task, not done here.

Rule: every stored glyph must decode to the Unicode name that carries its own sign number. Post-fix check: 58 glyphs, 0 mismatches.

| sign id | label (name) | old codepoint | old decodes to | new codepoint | new decodes to |
|---|---|---|---|---|---|
| AB13 | ME | U+1060C | LINEAR A SIGN AB016 | U+1060B | LINEAR A SIGN AB013 |
| AB16 | QA | U+1060F | LINEAR A SIGN AB021 | U+1060C | LINEAR A SIGN AB016 |
| AB17 | ZA | U+10610 | LINEAR A SIGN AB021F | U+1060D | LINEAR A SIGN AB017 |
| AB20 | ZO | U+10613 | LINEAR A SIGN AB022F | U+1060E | LINEAR A SIGN AB020 |
| AB21 | QI | U+10614 | LINEAR A SIGN AB022M | U+1060F | LINEAR A SIGN AB021 |
| AB22 | PI2 | U+10615 | LINEAR A SIGN AB023 | U+10612 | LINEAR A SIGN AB022 |
| AB23 | MU | U+10616 | LINEAR A SIGN AB023M | U+10615 | LINEAR A SIGN AB023 |
| AB26 | RU | U+10619 | LINEAR A SIGN AB027 | U+10618 | LINEAR A SIGN AB026 |
| AB27 | RE | U+1061A | LINEAR A SIGN AB028 | U+10619 | LINEAR A SIGN AB027 |
| AB28 | I | U+1061B | LINEAR A SIGN A028B | U+1061A | LINEAR A SIGN AB028 |
| AB37 | TI | U+10624 | LINEAR A SIGN AB041 | U+10620 | LINEAR A SIGN AB037 |
| AB38 | E | U+10625 | LINEAR A SIGN AB044 | U+10621 | LINEAR A SIGN AB038 |
| AB39 | PI | U+10626 | LINEAR A SIGN AB045 | U+10622 | LINEAR A SIGN AB039 |
| AB40 | WI | U+10627 | LINEAR A SIGN AB046 | U+10623 | LINEAR A SIGN AB040 |
| AB41 | SI | U+10628 | LINEAR A SIGN AB047 | U+10624 | LINEAR A SIGN AB041 |
| AB44 | KE | U+1062B | LINEAR A SIGN AB050 | U+10625 | LINEAR A SIGN AB044 |
| AB45 | DE | U+1062C | LINEAR A SIGN AB051 | U+10626 | LINEAR A SIGN AB045 |
| AB46 | JE | U+1062D | LINEAR A SIGN AB053 | U+10627 | LINEAR A SIGN AB046 |
| AB47 | ?47 | U+10630 | LINEAR A SIGN AB056 | U+10628 | LINEAR A SIGN AB047 |
| AB49 | ?49 | U+10630 | LINEAR A SIGN AB056 | U+1062A | LINEAR A SIGN AB049 |
| AB50 | PU | U+10631 | LINEAR A SIGN AB057 | U+1062B | LINEAR A SIGN AB050 |
| AB51 | DU | U+10632 | LINEAR A SIGN AB058 | U+1062C | LINEAR A SIGN AB051 |
| AB53 | RI | U+10634 | LINEAR A SIGN AB060 | U+1062D | LINEAR A SIGN AB053 |
| AB54 | WA | U+10635 | LINEAR A SIGN AB061 | U+1062E | LINEAR A SIGN AB054 |
| AB55 | NU | U+10636 | LINEAR A SIGN AB065 | U+1062F | LINEAR A SIGN AB055 |
| AB56 | PA3 | U+10637 | LINEAR A SIGN AB066 | U+10630 | LINEAR A SIGN AB056 |
| AB57 | JA | U+10638 | LINEAR A SIGN AB067 | U+10631 | LINEAR A SIGN AB057 |
| AB58 | SU | U+10639 | LINEAR A SIGN AB069 | U+10632 | LINEAR A SIGN AB058 |
| AB59 | TA | U+1063A | LINEAR A SIGN AB070 | U+10633 | LINEAR A SIGN AB059 |
| AB60 | RA | U+1063B | LINEAR A SIGN AB073 | U+10634 | LINEAR A SIGN AB060 |
| AB61 | O | U+1063C | LINEAR A SIGN AB074 | U+10635 | LINEAR A SIGN AB061 |
| AB65 | JU | U+10640 | LINEAR A SIGN AB079 | U+10636 | LINEAR A SIGN AB065 |
| AB66 | TA2 | U+10641 | LINEAR A SIGN AB080 | U+10637 | LINEAR A SIGN AB066 |
| AB67 | KI | U+10642 | LINEAR A SIGN AB081 | U+10638 | LINEAR A SIGN AB067 |
| AB69 | TU | U+10644 | LINEAR A SIGN AB085 | U+10639 | LINEAR A SIGN AB069 |
| AB70 | KO | U+10645 | LINEAR A SIGN AB086 | U+1063A | LINEAR A SIGN AB070 |
| AB73 | MI | U+10648 | LINEAR A SIGN AB118 | U+1063B | LINEAR A SIGN AB073 |
| AB74 | ZE | U+10649 | LINEAR A SIGN AB120 | U+1063C | LINEAR A SIGN AB074 |
| AB76 | RA2 | U+1064B | LINEAR A SIGN AB122 | U+1063D | LINEAR A SIGN AB076 |
| AB78 | QE | U+1064D | LINEAR A SIGN AB131A | U+1063F | LINEAR A SIGN AB078 |
| AB79 | ZU | U+1064E | LINEAR A SIGN AB131B | U+10640 | LINEAR A SIGN AB079 |
| AB80 | MA | U+1064F | LINEAR A SIGN A131C | U+10641 | LINEAR A SIGN AB080 |
| AB81 | KU | U+10650 | LINEAR A SIGN AB164 | U+10642 | LINEAR A SIGN AB081 |
| AB75 | WE | U+1064A | LINEAR A SIGN A120B | null | not encoded in Unicode Linear A |
| AB25 | A2 | U+10618 | LINEAR A SIGN AB026 | null | not encoded in Unicode Linear A |
