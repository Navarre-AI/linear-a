# Method

## Question
Can the corpus re-discover the libation formula family from ritual corpus structure alone?

## Corpus used
The benchmark used the current merged corpus from these files:
- `linear_a/data/corpus/libation_formulas.py`
- `linear_a/data/corpus/haghia_triada.py`
- `linear_a/data/corpus/zakros.py`
- `linear_a/data/corpus/khania.py`
- `linear_a/data/corpus/phaistos.py`
- `linear_a/data/corpus/other_sites.py`

Total inscriptions used: **127**.

## Ritual selection rule
The benchmark identified ritual texts using document-level metadata only:
- `type == libation_table`
- `type == stone_vessel`
- or `notes` containing `libation`

This produced:
- **29 ritual documents**
- **98 non-ritual documents**

## Anti-cheating rule
The benchmark did **not** begin by searching directly for the published libation formula string as a target answer. It first identified ritual texts structurally and then ranked repeated tokens and n-grams within that ritual subset.

## Exclusions
During candidate generation, the benchmark did **not** use:
- direct search for a known full formula string as the primary method
- manual semantic labels for ritual tokens
- handcrafted weighting designed to force a known formula shape

## Tokenization
Each inscription line was tokenized by normalizing separators such as `.`, spaces, and `|` into token boundaries.

## Candidate ranking
The benchmark measured:
- token frequency in ritual texts
- token exclusivity in ritual vs non-ritual documents
- repeated 2-grams and 3-grams across ritual documents
- prefix families among lines beginning with the dominant ritual token

## Success condition
A successful replication would recover a repeated ritual sequence family with:
- a stable core token or token cluster
- recurrence across multiple ritual documents
- strong concentration in ritual rather than non-ritual texts
- evidence for variable extensions rather than a single frozen line only

## Limitations
- Ritual selection depends on current document metadata.
- The current corpus is still incomplete.
- The benchmark establishes structural recurrence, not semantic proof.
- The formula family may contain multiple subtypes or local variants that are not yet separated here.
