# Independent claims audit, and what it changed

Before the 2026-09-18 release, this project wrote a list of every claim the
repository made: 544 rows, one per claim, each with a status and a check that
an outside reader can run. An outside agent then audited all 544 rows against
the pre-release snapshot of this repository and nothing else. It held no
access to the private companion repository.

This file records what that audit found and what was accepted. It is published
because the audit changed the project's own conclusions on a quarter of the
rows, and a reader who wants to know how reliable a withdrawal notice is has a
right to see the disagreements.

## Counts

| Measure | Value |
|---|---:|
| Rows audited | 544 of 544 |
| Rows where the audit agreed with our status | 213 of 544 |
| Rows where it disagreed | 331 of 544 |
| Disagreements accepted, our status changed | 123 of 331 |
| Disagreements where we hold our status | 10 of 331 |
| Disagreements that are one verdict under two labels | 172 of 331 |
| Disagreements still open | 26 of 331 |

Of the 123 accepted rows, 119 changed their status label and 4 kept the label
and changed the evidence line only.

Our status totals before and after the reconciliation:

| Status | Before | After |
|---|---:|---:|
| BACKED | 123 | 151 |
| REFUTED | 232 | 193 |
| UNVERIFIED | 72 | 80 |
| ARTEFACT, the number is right and the input is defective | 60 | 81 |
| REFRAMED | 35 | 25 |
| SUPERSEDED | 18 | 10 |
| OVERCLAIMED | 4 | 4 |
| **Total** | **544** | **544** |

The most common reasons our rows were wrong, by count of the 123:

| Error | Rows |
|---|---:|
| We measured a different data layer from the one the claim measured | 25 |
| We judged a stated goal or a hedged wording as if it were a finding | 24 |
| We used a different population, denominator or plain count | 23 |
| We endorsed a figure and did not flag the defect in its input | 20 |
| The audit found a public counter-example our row missed | 16 |
| We dropped a filter the method documented | 11 |
| We read an absence in our own data as non-attestation | 3 |
| We mixed units: tokens, types, bigrams and records | 1 |

## The seven disputed numbers, re-run

Seven numbers were the substance of the disagreement. Each was re-measured
independently against the pre-release snapshot before any verdict was accepted.
The audit was right on all seven.

| # | The number | Who was right | What the re-run gave |
|---|---|---|---|
| 1 | The quantity-line count in the summation benchmark | The audit | The documented rule filters to tablet lines. 289 of 346 lines pass it, with `ku-ro` first in 74 of 289. Our replacement figure of 239 dropped the tablet filter, and the unfiltered rule gives 304 of 346, so our own snippet did not return our own number. |
| 2 | The site-overlap population | The audit | The published table measures multisyllable word types. Every printed row reproduces on that population, Haghia Triada with Zakros at 11 shared of a 680 union. Our replacement measured all word types, which answers a different question. |
| 3 | The `A301` document counts | The audit, and so were we, about different layers | 48 of 772 is correct in the SigLA layer. 272 of 1,881 is correct in the glyph layer. Neither refutes the other. The real defect is that the published file never named its layer. |
| 4 | The `ki-ro` counts | The audit | 17 of 1,660 word tokens in one layer, 23 of 1,948 in another, 34 of 4,408 as a within-word bigram. Three units, not three estimates of one quantity. |
| 5 | The translation-coverage proof | The audit | `HT 88` holds 31 of 31 signs and 12 words. So 5 of the 6 translated keys lack the arrays, not 6 of 6. The stronger demonstration is that the stored `HT 88` text is not the text the benchmark printed. |
| 6 | The commodity document counts | The audit, and our replacement was also wrong | The counts need a role filter. `AB30` occurs in 54 of 772 records as a logogram and in 91 of 772 across all roles. A syllabic use of `AB30` is not a commodity record. |
| 7 | The corpus validator | The audit | The legacy validator returns 77 of 127 validated and 5 of 127 mismatches, exactly as published. The figures reproduce on the authored fixture. They do not describe the corpus. Our replacement figures measured the corpus, which is a different dataset. |

One number went the other way. The audit dated a data file by its committer
date. The last content change to that file carries an earlier author date, and
the project's own note gave a third date, the last regeneration. Three kinds of
date were in play and none of them was labelled. No date belongs in print
without saying which kind it is.

## The ten rows we hold

Ten of the 331 disagreements are rows where our status stands. They divide
three ways.

- **Three rows rest only on evidence in the private companion repository**,
  which a public-only audit cannot open. On those the audit's verdict of
  "cannot check" is the correct verdict for the evidence it had. They are two
  claims in the old README and one evaluative claim in the bibliography.
- **Six rows hold in a corrected or weaker form, with a public reproducer.**
  One claim to cover all the published scholarship is not supported, because
  the bibliography itself carries 24 entries marked missing. One translated
  tablet holds on its public half: that record carries `old_corpus` as its only
  source, with no signs and no words. Two example-agent claims hold because the
  files and the symbols they promise are absent from the published snapshot.
  Two validation-report claims hold because their figures reproduce: 129 of
  1,881 records carry an `old_corpus_id` against 127 legacy records, and the
  sign-count shortfall of 7 of 4,942 is real.
- **One row holds with a corrected reproducer**, and the audit was right about
  our first one. The claim is that every document id follows the GORILA
  pattern. The regular expression printed in our row rejects 0 of 1,881 keys,
  so our published check did not test what it said. Corrected reproducer: 65 of
  1,881 keys carry characters outside the plain GORILA pattern, for example
  `CR (?)Zf1` and an `HT Wa 1019` key with a Greek letter suffix. The
  underlying observation stands with the corrected check.

Two of those ten also carry a caution from the audit that is accepted. The
shortfall of 7 of 4,942 between the sign-count metadata and the parsed entries
reproduces, but the cause we asserted for it is asserted and not shown. That
caution is carried into the README data description of the same shortfall.

## The 26 rows still open

26 rows are genuinely unsettled, and nothing in this release closes them. They
fall into three kinds.

- **23 rows** where our status rests on private or general evidence and the
  audit's bar asks for a public measurement. No public reproducer exists either
  way. These are mostly interpretive sentences in the withdrawn findings and
  benchmark files, and evaluative sentences in the bibliography.
- **2 rows** where the audit reads a sentence as supported and we read it as
  overstated, and no measurement settles the reading of the sentence.
- **1 row** on the word "canonical". The write-back of 2026-09-18 settled the
  eight sign counts that were in dispute, so "canonical" is now a policy word
  rather than a measurement, and neither status is testable.

Every one of the 26 sits on material this release withdrew. None of them is a
statement this repository now makes.

## Policy difference, not an error

172 of the 331 disagreements are one verdict under two labels. The largest
group is a difference of bar. The audit will not convert an absence of
validation into a linguistic disproof: a proposed gloss with no validation is
unverified, not refuted. Our list refuted the same proposals, on evidence a
public audit cannot open.

Both positions are recorded. For this repository the difference does not
matter, because the material is withdrawn either way and no gloss is published
here. The part of the audit's point that carries a measurement was accepted:
the affix figures measure the SigLA layer, not the merged corpus, and the
95 percent figure for a final `ro` uses a boundary-only denominator, 103 of 108,
rather than 103 of 165 over all positions.

## One correction to the data

The audit's fourth strongest point produced the only data change in this
branch. A search of our own word data that returns zero is not a demonstration
that a form is unattested, because the search matches our own normalisation.
The form `su-ki-ri-ta` is attested at `PH Wa 32` in a published source, while
this corpus stores `su-ki-ra-ta` there and its own glyph string decodes to the
published reading. That disagreement is now recorded as a `conflicts` entry,
and neither reading is chosen.
See [ph-wa-32-conflict-2026-09-18.md](ph-wa-32-conflict-2026-09-18.md).

## What the audit did not do

It did not validate any withdrawn claim. Accepting that a figure reproduces on
an authored fixture is not accepting the finding built on that fixture. Of the
123 accepted rows, the ones that move to BACKED are counts with a layer and a
denominator, statements of a goal, and attestations in a named published
source. None of them restores a reading, a gloss or a translation.
