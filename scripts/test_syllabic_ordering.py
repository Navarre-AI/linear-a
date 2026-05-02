#!/usr/bin/env python3
"""
test_syllabic_ordering.py — Test Duhoux 1996 syllabic-classification hypothesis

Duhoux (1996, Kadmos 35) argues that Linear B scribes sorted administrative
tablet entries by the phonetic value of the initial syllabogram — syllabic
ordering. He extends the claim to Linear A.

This script tests the hypothesis against corpus.json:
  For each multi-entry tablet whose words have LB-derivable initial signs,
  are the entries sorted by phonetic value?

Phonetic sequence used: derived from standard LB syllabic ordering
(vowels a/e/i/o/u first, then consonant+vowel pairs).

Usage:
  python3 scripts/test_syllabic_ordering.py
  python3 scripts/test_syllabic_ordering.py --verbose
  python3 scripts/test_syllabic_ordering.py --min-words 4

Reference: Duhoux, Y. 1996. "Classement syllabique chez les scribes
linéaires A et B." Kadmos 35: 111-124.
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

# ── Phonetic sequence ──────────────────────────────────────────────────────────
# Standard LB syllabic ordering from Duhoux 1996 / Linear B syllabary.
# Only signs with reliably LB-derived Linear A values are included.
# Order: pure vowels first, then consonant+vowel by vowel-group
PHONETIC_ORDER = [
    # Pure vowels
    'a', 'e', 'i', 'o', 'u',
    # da-series
    'da', 'de', 'di', 'do', 'du',
    # ja-series
    'ja', 'je',
    # ka-series
    'ka', 'ke', 'ki', 'ko', 'ku',
    # ma-series
    'ma', 'me', 'mi', 'mo', 'mu',
    # na-series
    'na', 'ne', 'ni', 'no', 'nu',
    # pa-series
    'pa', 'pe', 'pi', 'po', 'pu',
    # qa-series
    'qa', 'qi',
    # ra-series
    'ra', 're', 'ri', 'ro', 'ru',
    # sa-series
    'sa', 'se', 'si', 'so', 'su',
    # ta-series
    'ta', 'te', 'ti', 'to', 'tu',
    # wa-series
    'wa', 'we', 'wi', 'wo',
    # za-series
    'za', 'ze', 'zo',
]

PHONETIC_RANK = {s: i for i, s in enumerate(PHONETIC_ORDER)}


def get_initial_sign(word: str):
    """
    Extract the initial syllabogram from a hyphen-delimited word like
    'ja-sa-sa-ra-me' → 'ja', or 'a-ta-i-*301-wa-ja' → 'a'.
    Returns None for logograms (A301, *NNN, uppercase), numerics, or
    words whose initial sign isn't in PHONETIC_RANK.
    """
    if not word or not isinstance(word, str):
        return None
    parts = word.split('-')
    initial = parts[0].strip().lower()
    # Skip logograms (uppercase letters, A-prefixed numbers, *NNN signs)
    if initial.startswith('a') and initial[1:].isdigit():
        return None
    if initial.startswith('*'):
        return None
    if initial[0].isupper():
        return None
    # Skip pure numbers
    if initial.isdigit():
        return None
    if initial in PHONETIC_RANK:
        return initial
    return None


def is_sorted_ascending(ranks: list[int]) -> bool:
    return all(ranks[i] <= ranks[i + 1] for i in range(len(ranks) - 1))


def is_sorted_descending(ranks: list[int]) -> bool:
    return all(ranks[i] >= ranks[i + 1] for i in range(len(ranks) - 1))


def kendall_tau_score(ranks: list[int]) -> float:
    """Fraction of correctly ordered pairs (concordant / total pairs)."""
    n = len(ranks)
    if n < 2:
        return 1.0
    concordant = discordant = 0
    for i in range(n):
        for j in range(i + 1, n):
            if ranks[i] < ranks[j]:
                concordant += 1
            elif ranks[i] > ranks[j]:
                discordant += 1
            # ties contribute 0
    total = concordant + discordant
    return concordant / total if total > 0 else 0.5


def main():
    parser = argparse.ArgumentParser(description='Test Duhoux syllabic ordering hypothesis')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Print per-tablet details')
    parser.add_argument('--min-words', type=int, default=3,
                        help='Minimum decodable words required (default: 3)')
    parser.add_argument('--tablets-only', action='store_true',
                        help='Restrict to type=tablet only (default: tablets + nodules)')
    args = parser.parse_args()

    corpus_path = Path(__file__).parent.parent / 'linear_a' / 'data' / 'corpus.json'
    corpus = json.loads(corpus_path.read_text())

    # ── Collect candidates ────────────────────────────────────────────────────
    ADMIN_TYPES = {'tablet', 'Tablet', 'nodule', 'Nodule', 'roundel', 'Roundel'}
    if args.tablets_only:
        ADMIN_TYPES = {'tablet', 'Tablet'}

    results = []
    skipped_no_words = 0
    skipped_too_few_decodable = 0
    site_stats = defaultdict(lambda: {'tested': 0, 'ordered': 0, 'tau_sum': 0.0})

    for doc_id, doc in corpus.items():
        if doc.get('type') not in ADMIN_TYPES:
            continue
        words = doc.get('words', [])
        if not isinstance(words, list) or len(words) < 2:
            skipped_no_words += 1
            continue

        # Decode initial signs
        decoded = []
        for w in words:
            sign = get_initial_sign(w)
            if sign is not None:
                decoded.append((w, sign, PHONETIC_RANK[sign]))

        if len(decoded) < args.min_words:
            skipped_too_few_decodable += 1
            continue

        ranks = [r for _, _, r in decoded]
        tau = kendall_tau_score(ranks)
        ascending = is_sorted_ascending(ranks)
        descending = is_sorted_descending(ranks)
        ordered = ascending or descending

        site = doc.get('site', 'unknown')
        scribe = doc.get('scribe', '')
        site_stats[site]['tested'] += 1
        site_stats[site]['tau_sum'] += tau
        if ordered:
            site_stats[site]['ordered'] += 1

        results.append({
            'id': doc_id,
            'site': site,
            'scribe': scribe,
            'words_total': len(words),
            'words_decodable': len(decoded),
            'decoded': decoded,
            'ranks': ranks,
            'tau': tau,
            'ascending': ascending,
            'descending': descending,
            'ordered': ordered,
        })

    if not results:
        print('No tablets with sufficient decodable words found.')
        return

    # ── Summary stats ──────────────────────────────────────────────────────────
    n = len(results)
    n_ordered = sum(1 for r in results if r['ordered'])
    n_ascending = sum(1 for r in results if r['ascending'])
    n_descending = sum(1 for r in results if r['descending'])
    mean_tau = sum(r['tau'] for r in results) / n
    # Expected tau under random ordering: 0.5
    tau_above_chance = sum(1 for r in results if r['tau'] > 0.5)

    print('=' * 60)
    print('DUHOUX 1996 SYLLABIC ORDERING — HYPOTHESIS TEST')
    print('=' * 60)
    print(f'Corpus: linear_a/data/corpus.json')
    print(f'Admin-type filter: {", ".join(sorted(ADMIN_TYPES))}')
    print(f'Min decodable words: {args.min_words}')
    print()
    print(f'Tablets with ≥{args.min_words} decodable words: {n}')
    print(f'  Skipped (no words / <2 words): {skipped_no_words}')
    print(f'  Skipped (too few decodable):   {skipped_too_few_decodable}')
    print()
    print(f'ORDERING RESULTS:')
    print(f'  Perfectly ordered (asc or desc):  {n_ordered:3d} / {n}  ({100*n_ordered/n:.1f}%)')
    print(f'    Ascending only:                 {n_ascending:3d} / {n}  ({100*n_ascending/n:.1f}%)')
    print(f'    Descending only:                {n_descending:3d} / {n}  ({100*n_descending/n:.1f}%)')
    print()
    print(f'KENDALL TAU (pair concordance):')
    print(f'  Mean tau:               {mean_tau:.3f}  (random baseline: 0.500)')
    print(f'  Tablets tau > 0.5:      {tau_above_chance:3d} / {n}  ({100*tau_above_chance/n:.1f}%)')
    print()

    # ── Interpretation ─────────────────────────────────────────────────────────
    print('INTERPRETATION:')
    if mean_tau > 0.65:
        verdict = 'STRONG support for syllabic ordering'
    elif mean_tau > 0.55:
        verdict = 'WEAK / MARGINAL support for syllabic ordering'
    else:
        verdict = 'NO support for syllabic ordering'
    print(f'  {verdict}')
    print(f'  (Duhoux 1996 found clear ordering in Linear B admin tablets;')
    print(f'   random expectation ≈ 50% ascending, mean tau ≈ 0.5)')
    print()

    # ── Per-site breakdown ─────────────────────────────────────────────────────
    print('PER-SITE BREAKDOWN (sites with ≥3 tested tablets):')
    print(f'  {"Site":<25} {"Tested":>6} {"Ordered":>8} {"Mean τ":>8}')
    print(f'  {"-"*25} {"------":>6} {"-------":>8} {"------":>8}')
    for site, s in sorted(site_stats.items(), key=lambda x: -x[1]['tested']):
        if s['tested'] < 3:
            continue
        mean_t = s['tau_sum'] / s['tested']
        pct = 100 * s['ordered'] / s['tested']
        print(f'  {site:<25} {s["tested"]:>6} {s["ordered"]:>5} ({pct:4.0f}%) {mean_t:>8.3f}')
    print()

    # ── Best / worst examples ──────────────────────────────────────────────────
    sorted_by_tau = sorted(results, key=lambda x: -x['tau'])
    print('TOP 5 MOST ORDERED TABLETS:')
    for r in sorted_by_tau[:5]:
        signs = ' → '.join(f'{w}({s})' for w, s, _ in r['decoded'][:6])
        print(f'  {r["id"]:<12} τ={r["tau"]:.2f}  [{signs}{"…" if len(r["decoded"])>6 else ""}]')
    print()
    print('TOP 5 LEAST ORDERED TABLETS:')
    for r in sorted_by_tau[-5:]:
        signs = ' → '.join(f'{w}({s})' for w, s, _ in r['decoded'][:6])
        print(f'  {r["id"]:<12} τ={r["tau"]:.2f}  [{signs}{"…" if len(r["decoded"])>6 else ""}]')
    print()

    # ── Verbose: per-tablet breakdown ──────────────────────────────────────────
    if args.verbose:
        print('PER-TABLET DETAIL:')
        for r in sorted(results, key=lambda x: x['id']):
            status = ('ASC' if r['ascending'] else 'DESC' if r['descending'] else '    ')
            signs = ', '.join(f'{s}({rank})' for _, s, rank in r['decoded'])
            print(f'  {r["id"]:<14} {status} τ={r["tau"]:.2f} n={r["words_decodable"]} | {signs}')


if __name__ == '__main__':
    main()
