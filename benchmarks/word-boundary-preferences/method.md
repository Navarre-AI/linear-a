# Method

## Goal
Determine whether Linear A signs show statistically significant preferences
for word-initial vs. word-final position, revealing phonotactic constraints
of the underlying language.

## Data source
Full imported SigLA website corpus: 772 documents, 951 multi-syllable words
extracted from word-view pages. Each word's sign readings were split on
hyphens to isolate initial and final syllabograms.

## Approach
1. Parse all `index-word-*.html` pages from the imported SigLA snapshot
2. Extract sign readings via `sure-reading` spans
3. Join into hyphenated words (e.g., `ku-ro`, `ja-sa-sa-ra-me`)
4. Filter to multi-syllable words only (single signs excluded)
5. Count each sign's frequency in word-initial vs. word-final position
6. Identify signs with strong positional preference (>75% in one position,
   minimum 10 total occurrences)

## Controls
- Only signs with 10+ total occurrences considered (avoids small-sample noise)
- Threshold set at 75% preference (3:1 ratio) for "strong" preference
- Analysis covers the full attested corpus, not a hand-selected subset
