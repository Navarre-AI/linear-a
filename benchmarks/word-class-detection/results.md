# Results: Word Class Detection

## Corpus summary
- Documents with word data: **772**
- Multi-syllable words analyzed: **951 unique, 1,660 occurrences**
- Document types: 426 tablets, 166 nodules, 146 roundels, plus libation tables, vessels, etc.

## Classification method

Words classified by distributional context:
- **Administrative terms**: appear with numerals AND commodity ideograms on tablets
- **Probable names**: appear on tablets with ideograms but rarely with numerals (recipients/agents)
- **Ritual vocabulary**: appear primarily on libation tables and stone vessels

## Administrative terms (24 words)

Words that co-occur with both commodity ideograms and numerical signs:

| Word | Total | With numbers | With ideograms |
|------|-------|-------------|----------------|
| sa-ra | 20 | 13 | 18 |
| ki-ro | 17 | 10 | 12 |
| ka-pa | 5 | 5 | 5 |
| je-di | 4 | 3 | 4 |
| sa-ro | 4 | 3 | 4 |
| da-qe-ra | 3 | 3 | 2 |
| po-to-ku-ro | 3 | 2 | 3 |
| ka-na | 3 | 2 | 3 |
| re-za | 3 | 2 | 3 |
| *56-ni-na | 3 | 3 | 2 |

Note: `sa-ra` at 20 occurrences is the second most frequent administrative word after `ku-ro`. It appears almost exclusively with commodity ideograms (18/20) and frequently with numbers (13/20), suggesting it is a transaction type or assessment category.

## Probable personal/place names (63 words)

Words appearing on tablets with ideograms but not typically with numbers — suggesting they label the recipients or sources of commodities:

| Word | Total | On tablets | With ideograms |
|------|-------|-----------|----------------|
| a-du | 12 | 12 | 11 |
| ku-*56-nu | 8 | 8 | 4 |
| ma-di | 7 | 7 | 7 |
| sa-ru | 6 | 6 | 5 |
| ku-pa | 5 | 4 | 4 |
| ku-ni-su | 4 | 4 | 4 |
| pa-ja-re | 4 | 4 | 4 |
| a-ka-ru | 3 | 3 | 3 |
| mi-nu-te | 3 | 3 | 3 |

Of these, `pa-ja-re` is already identified as Phaistos (a place name). `ku-ni-su` may be a commodity name (cf. Akkadian *kunisu* "emmer wheat"). The rest are strong candidates for personal or place names.

## Administrative vs. Name distinction

The distributional test is clear:
- **Administrative terms** (sa-ra, ki-ro, ka-pa): high co-occurrence with BOTH ideograms and numbers
- **Names** (a-du, ma-di, sa-ru): high co-occurrence with ideograms, LOW co-occurrence with numbers

This matches the expected tablet structure: NAME . COMMODITY NUMBER, where names label agents/recipients and administrative terms label transaction types.

## Interpretation

The distributional approach successfully separates three word classes:
1. **Transaction vocabulary** (24 words): functional/administrative terms
2. **Agent labels** (63 words): personal names, place names, or institutional designations
3. **Commodity terms**: encoded as logograms rather than syllabic words

This is consistent with the known administrative structure but extends it with specific word assignments based on distributional evidence across 772 documents.

## Confidence
**Provisional success.**
The distributional test is straightforward and the results are consistent with known tablet structure. However, the boundary between names and transaction terms is not always sharp, and ritual vocabulary detection was limited by document-type encoding in the imported data.
