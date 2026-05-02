# Method

## Question
Can the corpus support `po-to-ku-ro` as a structurally related extended summation expression?

## Corpus used
The benchmark used the same current merged corpus as the `ku-ro` benchmark:
- `linear_a/data/corpus/libation_formulas.py`
- `linear_a/data/corpus/haghia_triada.py`
- `linear_a/data/corpus/zakros.py`
- `linear_a/data/corpus/khania.py`
- `linear_a/data/corpus/phaistos.py`
- `linear_a/data/corpus/other_sites.py`

Total inscriptions used: **127**.

## Approach
This benchmark follows the `ku-ro` replication benchmark and asks whether a longer form containing `ku-ro` appears in the same structural environment.

## Anti-cheating rule
The benchmark treats `po-to-ku-ro` as a follow-on replication target rather than a fully blind primary candidate. The question is not whether it dominates the corpus, but whether its distribution matches an extended summation role.

## Quantity-line heuristic
As in the `ku-ro` benchmark, quantity-bearing administrative lines were approximated as **tablet lines** containing both:
- an all-caps commodity/ideogram-like token
- and a digit

## Success condition
A successful replication would show that `po-to-ku-ro` appears:
- in quantity-bearing tablet lines
- in the same line-initial administrative slot as `ku-ro`
- in a way consistent with a larger or extended summation expression

## Limitations
- The sample is very small.
- This benchmark depends on the current corpus slice and heuristic line classification.
- The result is structural, not semantic proof.
