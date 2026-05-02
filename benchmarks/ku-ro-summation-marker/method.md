# Method

## Question
Can the corpus re-discover `ku-ro` as a summation marker from structural behavior alone?

## Corpus used
The benchmark used the current merged corpus from these files:
- `linear_a/data/corpus/libation_formulas.py`
- `linear_a/data/corpus/haghia_triada.py`
- `linear_a/data/corpus/zakros.py`
- `linear_a/data/corpus/khania.py`
- `linear_a/data/corpus/phaistos.py`
- `linear_a/data/corpus/other_sites.py`

Total inscriptions used: **127**.

## Anti-cheating rule
The benchmark did not begin by searching specifically for `ku-ro` as a target token. It first identified quantity-bearing administrative lines and then ranked recurrent tokens by structural prominence.

## Exclusions
During candidate generation, the benchmark did **not** use:
- direct searching for `ku-ro`
- manual semantic labels for candidate tokens
- handcrafted weighting designed to favor the known answer

## Tokenization
Each inscription line was tokenized by normalizing separators such as `.`, spaces, and `|` into token boundaries.

## Quantity-line heuristic
The first-pass benchmark defined a quantity-bearing administrative line as a **tablet line** containing both:
- an all-caps commodity/ideogram-like token (e.g. `GRA`, `VIN`, `OLE`, `OVIS`)
- and a digit

This produced **289** candidate quantity lines.

## Candidate ranking
For the first pass, the benchmark measured:
- token frequency in quantity-bearing tablet lines
- line-initial prominence
- recurrence in administrative contexts

The key question was: which token most strongly dominates the initial slot in quantity-bearing lines?

## Success condition
A successful replication would recover a small number of candidate administrative markers, with one of them strongly dominating quantity-bearing line openings in a way consistent with a summation function.

## Limitations
- The quantity-line detector is heuristic, not a full parser.
- Numeric information is often embedded in line strings rather than normalized metadata.
- The current corpus is substantial but incomplete.
- This benchmark establishes structural behavior, not full semantic proof.
