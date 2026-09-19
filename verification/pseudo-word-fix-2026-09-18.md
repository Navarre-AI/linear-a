# Pseudo-word fix, 2026-09-18

Reported by a reader of the repository by email on 2026-09-17; verified 2026-09-18.

## The defect

`linear_a/import_sigla.py` collected each document's word pages with the filter
`f.startswith("index-word")`. SigLA gives each word its own page, named
`index-word-N.html`. SigLA also gives each document one overview page, named
`index-word.html`, which repeats every sign of every word. The filter matched the
overview page too. The overview page became one extra word equal to the join of
all the real words of the document.

The sort key was `int(re.search(r'(\d+)', f).group(1)) if ... else 0`. The overview
page has no number, so it took the key 0, the same key as `index-word-0.html`.
Python's `sorted` is stable, so the winner of that tie was whichever name
`os.listdir` returned first. On the machine that built the data the overview page
came first, so the pseudo-word took word index 0.


## Confirmation, one document parsed both ways

The imported SigLA snapshot is not in this repository, so the pages for HT 39 were
read again from the live site (`https://sigla.phis.me/document/HT%2039/`) on
2026-09-18 and put in a local fixture. The fixture holds `index.html`, the six real
word pages `index-word-0.html` to `index-word-5.html`, and the overview page
`index-word.html`.

Overview page `index-word.html`, parsed with the importer's `sure-reading` regex:

    ta-i-*123-ku-re-ju-ku-sa-ma-ti-ku-re-ku-ro

The six real word pages:

    index-word-0.html -> ta-i-*123
    index-word-1.html -> ku-re-ju
    index-word-2.html -> ku
    index-word-3.html -> sa-ma-ti
    index-word-4.html -> ku-re
    index-word-5.html -> ku-ro

The old filter over the fixture gives 7 words, and they are the 7 words that
`corpus.json` held for HT 39, in the same order. The fixed filter gives the 6 real
words. SigLA's own document page for HT 39 reports "17 signs / 6 words".


## The fix

The importer now selects word pages with `^index-word-(\d+)\.html$` and sorts them
by the captured number. The overview page cannot match, and the tie in the sort key
is gone. This is the only place in the repository with that filter. The file
`benchmarks/word-boundary-preferences/method.md` already describes the correct
pattern `index-word-*.html`.

The importer was fixed but not re-run. The raw SigLA page snapshot is not in this
repository, so an end-to-end re-run is not possible here. The correction to the
data was applied as a deterministic post-pass with this rule:

> For each record, if `words` has more than one entry and
> `words[0] == "-".join(words[1:])`, drop `words[0]`.

That is the same set of words the fixed importer produces, because the pseudo-word
is by construction the join of the real words in order.


## Counts

- `linear_a/data/corpus.json`: 1,881 records. 385 records hold more than one word.
  318 of those 385 matched the rule and were corrected. The other 67 are the records
  whose `word_source` is `lineara`, not `sigla`. Every one of the 318 has
  `word_source: sigla`. The partition is clean: all sigla multi-word records were
  defective, no lineara record was.
- Assertion, checked in code at the time of the edit: exactly 318 records changed;
  each change is the removal of `words[0]` only; for every record, the key order is
  unchanged and every other field serialises byte for byte as before. The file is
  written with the same serialisation as before (`indent=2`, `ensure_ascii=False`,
  one trailing newline), so an unchanged record is byte identical. `git diff` on the
  file shows 318 removed lines and 0 added lines.
- Cross-check against SigLA's own `word_count` for the 318 documents (from the
  private snapshot `sigla-live-2026-08-14.json`): after the fix the count agrees for
  260 documents and is short for 58. Before the fix, 47 documents held more words
  than SigLA reports, which is not possible. The 58 short counts are a second,
  separate defect: the importer skips a word page that has no `sure-reading` span,
  so a word of unsure signs is dropped. That is not corrected here.
- `linear_a/data/sources/sigla/corpus_structured.json`: the importer's own output,
  772 documents. All 432 multi-word documents were defective and were corrected by
  the same rule. The word index `i` was renumbered from 0, which is what the fixed
  importer produces. Serialisation is unchanged (`indent=2`, `ensure_ascii=True`).


## Before and after, HT 39

Before (7 words):

```json
[
  "ta-i-*123-ku-re-ju-ku-sa-ma-ti-ku-re-ku-ro",
  "ta-i-*123",
  "ku-re-ju",
  "ku",
  "sa-ma-ti",
  "ku-re",
  "ku-ro"
]
```

After (6 words):

```json
[
  "ta-i-*123",
  "ku-re-ju",
  "ku",
  "sa-ma-ti",
  "ku-re",
  "ku-ro"
]
```


## Effect on vocabulary counts

- `corpus.json`, multi-syllable word tokens: 1,678 before, 1,393 after. Unique
  multi-syllable words: 1,211 before, 979 after.
- `corpus_structured.json`, unique words: 1,025 before, 793 after. Unique
  multi-syllable words: 951 before, 719 after.

The numbers 1,025 and 951 are quoted as headline figures in
`benchmarks/compound-words/results.md`, `benchmarks/word-boundary-preferences/`,
`benchmarks/word-class-detection/results.md`, `benchmarks/case-system-analysis/results.md`
and in the docstring of `linear_a/data/glossary.py`. Those figures came from the
defective import. They are not corrected here.


## Consumers that changed behaviour

`scripts/test_syllabic_ordering.py` reads `words` in order and needs at least two
words and three decodable words per tablet. The pseudo-word added a word to every
affected tablet, and its initial sign is always the initial sign of the first real
word, which added a tie at position 0. Headline output before and after the fix:

| measure | before | after |
|---|---|---|
| tablets with 3+ decodable words | 215 | 144 |
| perfectly ordered (asc or desc) | 94 (43.7%) | 23 (16.0%) |
| mean tau | 0.540 | 0.523 |
| tablets with tau > 0.5 | 112 (52.1%) | 69 (47.9%) |

The script still runs and exits 0. The result is much weaker after the fix. The
published claim rested on the defect.

Everything else that reads `words` is order-agnostic and count-based, so it only
loses the pseudo-words: `linear_a/data/corpus/__init__.py` (`get_words`,
`get_unique_words`, `search_sequence`), `linear_a/analysis/frequency_analysis.py`,
`linear_a/analysis/morphology.py`, `linear_a/decipher.py`, and
`examples/ai-agent-starter/tools.py` (`lookup_tablet`, which served the pseudo-word
to the agent as the first word of the tablet). All four modules run and exit 0 after
the fix.

No code in the repository depends on `words[0]` being the whole inscription.


## The 318 corrected records

- ARKH 1a
- ARKH 1b
- ARKH 2
- ARKH 3a
- ARKH 3b
- ARKH 4a
- ARKH 4b
- ARKH 5
- ARKH 6
- HT 1
- HT 100
- HT 101
- HT 102
- HT 103
- HT 104
- HT 108
- HT 109
- HT 10a
- HT 10b
- HT 110a
- HT 110b
- HT 112a
- HT 113
- HT 113 ter
- HT 114a
- HT 115a
- HT 115b
- HT 116a
- HT 116b
- HT 117a
- HT 117b
- HT 118
- HT 119
- HT 11a
- HT 11b
- HT 12
- HT 120
- HT 121
- HT 122a
- HT 122b
- HT 123a
- HT 123b
- HT 126a
- HT 127a
- HT 127b
- HT 128a
- HT 128b
- HT 129
- HT 13
- HT 130
- HT 131a
- HT 131b
- HT 132
- HT 133
- HT 135a
- HT 135b
- HT 137
- HT 139
- HT 14
- HT 140
- HT 141
- HT 144
- HT 146
- HT 147
- HT 15
- HT 154
- HT 154A
- HT 154C
- HT 154N
- HT 16
- HT 17
- HT 18
- HT 19
- HT 2
- HT 20
- HT 21
- HT 23a
- HT 23b
- HT 24a
- HT 25a
- HT 25b
- HT 26a
- HT 26b
- HT 27a
- HT 27b
- HT 28a
- HT 28b
- HT 29
- HT 3
- HT 30
- HT 31
- HT 32
- HT 33
- HT 34
- HT 35
- HT 36
- HT 37
- HT 38
- HT 39
- HT 4
- HT 40
- HT 41a
- HT 42+59
- HT 43
- HT 44a
- HT 44b
- HT 45a
- HT 45b
- HT 46a
- HT 47a
- HT 49a
- HT 49b
- HT 5
- HT 51a
- HT 51b
- HT 52a
- HT 52b
- HT 53a
- HT 53b
- HT 54a
- HT 55a
- HT 55b
- HT 56a
- HT 57a
- HT 58
- HT 61
- HT 62+73
- HT 63
- HT 64
- HT 66
- HT 68
- HT 69
- HT 6a
- HT 6b
- HT 70
- HT 72
- HT 74
- HT 79+83
- HT 7a
- HT 7b
- HT 81
- HT 84
- HT 85a
- HT 85b
- HT 86a
- HT 86b
- HT 87
- HT 88
- HT 89
- HT 8a
- HT 8b
- HT 90
- HT 91
- HT 92
- HT 93a
- HT 93b
- HT 94a
- HT 94b
- HT 95a
- HT 95b
- HT 96a
- HT 96b
- HT 97a
- HT 98a
- HT 98b
- HT 99a
- HT 99b
- HT 9a
- HT 9b
- HT Wa 1020α
- HT Wc 3014b
- HT Zb 158a
- HT Zb 160
- HT Zd 155
- HT Zd 156
- HT Zd 157
- KE 1
- KH 1
- KH 10
- KH 100
- KH 11
- KH 12
- KH 13
- KH 14
- KH 16
- KH 17
- KH 18
- KH 2
- KH 20
- KH 21
- KH 22
- KH 23
- KH 24
- KH 28
- KH 29
- KH 33
- KH 36
- KH 37
- KH 39
- KH 4
- KH 40
- KH 44
- KH 47
- KH 49
- KH 5
- KH 50
- KH 51
- KH 53
- KH 57
- KH 58
- KH 59
- KH 6
- KH 60
- KH 61
- KH 63
- KH 64
- KH 73
- KH 74
- KH 76
- KH 79
- KH 79+89
- KH 7a
- KH 7b
- KH 8
- KH 83
- KH 86
- KH 88
- KH 9
- KH 90
- KH 91
- KH 92
- KH 94
- KH 95
- KH 97a
- KH 97b
- KH 99
- KN 1a
- KN 1b
- KN 2
- KN 22a
- KN 22c
- KN 28b
- KN 32a
- KN 32b
- KN Wb 33b
- KN Zb 35
- KN Zb 4
- KN Zb 40
- KN Zc 6
- KN Zc 7
- MA 10a
- MA 10b
- MA 1a
- MA 1b
- MA 2b
- MA 2c
- MA 4b
- MI 2
- PH 10
- PH 12a
- PH 13a
- PH 14a
- PH 15a
- PH 15b
- PH 16a
- PH 16b
- PH 18a
- PH 1a
- PH 1b
- PH 2
- PH 26
- PH 27
- PH 28a
- PH 30
- PH 31a
- PH 31b
- PH 3a
- PH 3b
- PH 6
- PH 7a
- PH 7b
- PS Za 2
- PYR 1
- SY Za 4
- TY 2
- TY 3a
- TY 3b
- ZA 10a
- ZA 10b
- ZA 11a
- ZA 11b
- ZA 13
- ZA 14
- ZA 15a
- ZA 15b
- ZA 16
- ZA 18a
- ZA 19
- ZA 1a
- ZA 1b
- ZA 20
- ZA 21a
- ZA 21b
- ZA 22
- ZA 23
- ZA 24a
- ZA 26a
- ZA 27
- ZA 29
- ZA 4a
- ZA 5a
- ZA 5b
- ZA 6a
- ZA 6b
- ZA 7a
- ZA 8
- ZA 9
- ZA Wc 2
