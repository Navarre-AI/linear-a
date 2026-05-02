"""
Linear A Frequency Analysis
=============================
Statistical analysis of sign/word frequencies, bigrams, trigrams,
positional patterns, entropy, and Zipf's law validation.

This module treats Linear A words as sequences of CV syllables
(using Linear B phonetic values) and analyzes their statistical
properties to constrain the language family.

Key insight: Natural languages have predictable frequency distributions.
If Linear A readings produce Zipf-compliant distributions, the phonetic
values are likely correct. Deviations point to misread signs.
"""

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from linear_a.data.corpus import get_all, get_words, get_unique_words, get_by_type


# =============================================================================
# SYLLABLE EXTRACTION
# =============================================================================

def extract_syllables(word):
    """Split a Linear A word into its constituent syllables."""
    if not word or not isinstance(word, str):
        return []
    return [s.strip() for s in word.split('-') if s.strip()]


def get_all_syllables():
    """Extract all syllable tokens from the corpus."""
    syllables = []
    for word in get_words():
        syllables.extend(extract_syllables(word))
    return syllables


def get_syllable_frequencies():
    """Count frequency of each syllable across the entire corpus."""
    return Counter(get_all_syllables())


# =============================================================================
# WORD-LEVEL FREQUENCY ANALYSIS
# =============================================================================

def word_frequency_table():
    """Generate a complete word frequency table with rank and statistics."""
    word_counts = get_unique_words()
    total = sum(word_counts.values())
    table = []
    cumulative = 0.0
    for rank, (word, count) in enumerate(word_counts.most_common(), 1):
        freq = count / total
        cumulative += freq
        table.append({
            'word': word, 'count': count, 'rank': rank,
            'frequency': freq, 'cumulative_freq': cumulative,
            'syllable_count': len(extract_syllables(word)),
        })
    return table


def word_length_distribution():
    """Distribution of word lengths (in syllables)."""
    lengths = Counter()
    for word in get_words():
        lengths[len(extract_syllables(word))] += 1
    return dict(sorted(lengths.items()))


# =============================================================================
# N-GRAM ANALYSIS
# =============================================================================

IDEOGRAMS = {
    'GRA': 'grain/wheat', 'HORD': 'barley', 'OLE': 'oil/olive oil',
    'VIN': 'wine', 'FIC': 'figs', 'OLIV': 'olives',
    'OVIS': 'sheep', 'CAP': 'goats', 'SUS': 'pigs', 'BOS': 'cattle',
    'TELA': 'textiles', 'AROM': 'aromatics', 'CYP': 'cypress?',
    'VIR': 'men', 'MUL': 'women',
}


def syllable_bigrams():
    """Extract syllable bigrams from all words."""
    bigrams = Counter()
    for word in get_words():
        syls = extract_syllables(word)
        for i in range(len(syls) - 1):
            bigrams[(syls[i], syls[i+1])] += 1
    return bigrams


def syllable_trigrams():
    """Extract syllable trigrams from all words."""
    trigrams = Counter()
    for word in get_words():
        syls = extract_syllables(word)
        for i in range(len(syls) - 2):
            trigrams[(syls[i], syls[i+1], syls[i+2])] += 1
    return trigrams


def word_bigrams():
    """Extract word-level bigrams (word pairs in same line)."""
    bigrams = Counter()
    corpus = get_all()
    for entry in corpus.values():
        for line in entry.get('lines', []):
            words_in_line = []
            for part in line.replace('|', '.').split('.'):
                w = part.strip()
                if w and not w.startswith(tuple(IDEOGRAMS.keys())) and len(w) > 1:
                    try:
                        float(w)
                    except ValueError:
                        words_in_line.append(w)
            for i in range(len(words_in_line) - 1):
                bigrams[(words_in_line[i], words_in_line[i+1])] += 1
    return bigrams


# =============================================================================
# POSITIONAL ANALYSIS
# =============================================================================

def positional_frequencies():
    """Analyze which syllables prefer word-initial, medial, or final positions."""
    initial, final, medial = Counter(), Counter(), Counter()
    for word in get_words():
        syls = extract_syllables(word)
        if not syls:
            continue
        initial[syls[0]] += 1
        if len(syls) > 1:
            final[syls[-1]] += 1
        for s in syls[1:-1]:
            medial[s] += 1
    return {'initial': initial, 'final': final, 'medial': medial}


def initial_syllable_stats():
    """Which syllables appear word-initially and how often."""
    pos = positional_frequencies()
    total_initial = sum(pos['initial'].values())
    stats = []
    for syl, count in pos['initial'].most_common():
        total_syl = sum(pos[p].get(syl, 0) for p in ('initial', 'medial', 'final'))
        stats.append({
            'syllable': syl, 'initial_count': count, 'total_count': total_syl,
            'initial_ratio': count / total_syl if total_syl > 0 else 0,
            'initial_frequency': count / total_initial if total_initial > 0 else 0,
        })
    return stats


def final_syllable_stats():
    """Which syllables appear word-finally and how often."""
    pos = positional_frequencies()
    total_final = sum(pos['final'].values())
    stats = []
    for syl, count in pos['final'].most_common():
        total_syl = sum(pos[p].get(syl, 0) for p in ('initial', 'medial', 'final'))
        stats.append({
            'syllable': syl, 'final_count': count, 'total_count': total_syl,
            'final_ratio': count / total_syl if total_syl > 0 else 0,
            'final_frequency': count / total_final if total_final > 0 else 0,
        })
    return stats


# =============================================================================
# ENTROPY & INFORMATION THEORY
# =============================================================================

def shannon_entropy(counter):
    """Calculate Shannon entropy H = -sum(p * log2(p))."""
    total = sum(counter.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counter.values():
        if count > 0:
            p = count / total
            entropy -= p * math.log2(p)
    return entropy


def conditional_entropy(bigram_counts, unigram_counts):
    """Calculate conditional entropy H(Y|X) for bigram transitions."""
    total_bigrams = sum(bigram_counts.values())
    if total_bigrams == 0:
        return 0.0
    transitions = defaultdict(Counter)
    for (x, y), count in bigram_counts.items():
        transitions[x][y] += count
    h = 0.0
    for x, y_counts in transitions.items():
        x_total = sum(y_counts.values())
        for y, xy_count in y_counts.items():
            p_xy = xy_count / total_bigrams
            p_y_given_x = xy_count / x_total
            if p_y_given_x > 0:
                h -= p_xy * math.log2(p_y_given_x)
    return h


def mutual_information_pairs():
    """Calculate pointwise mutual information for all syllable bigrams."""
    bigrams = syllable_bigrams()
    unigrams = get_syllable_frequencies()
    total_bi = sum(bigrams.values())
    total_uni = sum(unigrams.values())
    if total_bi == 0 or total_uni == 0:
        return []
    pmi_scores = []
    for (x, y), count in bigrams.items():
        p_xy = count / total_bi
        p_x = unigrams.get(x, 0) / total_uni
        p_y = unigrams.get(y, 0) / total_uni
        if p_x > 0 and p_y > 0 and p_xy > 0:
            pmi = math.log2(p_xy / (p_x * p_y))
            pmi_scores.append({
                'bigram': (x, y), 'pmi': pmi, 'count': count,
                'display': f"{x}-{y}",
            })
    return sorted(pmi_scores, key=lambda x: x['pmi'], reverse=True)


# =============================================================================
# ZIPF'S LAW ANALYSIS
# =============================================================================

def zipf_analysis():
    """Test whether word frequencies follow Zipf's law: f(r) ~ 1/r^s"""
    word_counts = get_unique_words()
    if not word_counts:
        return {'zipf_constant': 0, 'r_squared': 0, 'exponent': 0, 'data': []}
    ranked = word_counts.most_common()
    log_ranks, log_freqs, data = [], [], []
    for rank, (word, count) in enumerate(ranked, 1):
        log_r, log_f = math.log(rank), math.log(count)
        log_ranks.append(log_r)
        log_freqs.append(log_f)
        data.append({'rank': rank, 'word': word, 'count': count,
                     'rank_x_freq': rank * count, 'log_rank': log_r, 'log_freq': log_f})
    n = len(log_ranks)
    if n < 2:
        return {'zipf_constant': 0, 'r_squared': 0, 'exponent': 0, 'data': data}
    sum_x = sum(log_ranks)
    sum_y = sum(log_freqs)
    sum_xy = sum(x * y for x, y in zip(log_ranks, log_freqs))
    sum_x2 = sum(x * x for x in log_ranks)
    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        return {'zipf_constant': 0, 'r_squared': 0, 'exponent': 0, 'data': data}
    slope = (n * sum_xy - sum_x * sum_y) / denom
    intercept = (sum_y - slope * sum_x) / n
    mean_y = sum_y / n
    ss_tot = sum((y - mean_y) ** 2 for y in log_freqs)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(log_ranks, log_freqs))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    exponent = -slope
    rf_products = [d['rank_x_freq'] for d in data]
    zipf_constant = sum(rf_products) / len(rf_products) if rf_products else 0
    return {'zipf_constant': zipf_constant, 'r_squared': r_squared,
            'exponent': exponent, 'intercept': intercept, 'n_words': n, 'data': data}


# =============================================================================
# COMMODITY & CONTEXT ANALYSIS
# =============================================================================

def word_commodity_associations():
    """For each word, count which commodities it appears with."""
    associations = defaultdict(Counter)
    corpus = get_all()
    for entry in corpus.values():
        commodities_in_doc = set()
        for line in entry.get('lines', []):
            for ideo in IDEOGRAMS:
                if ideo in line:
                    commodities_in_doc.add(ideo)
        for line in entry.get('lines', []):
            for part in line.replace('|', '.').split('.'):
                w = part.strip()
                if w and not any(w.startswith(i) for i in IDEOGRAMS) and len(w) > 1:
                    try:
                        float(w)
                    except ValueError:
                        for c in commodities_in_doc:
                            associations[w][c] += 1
    return dict(associations)


def commodity_specialists():
    """Words appearing with only 1-2 commodities (commodity-specific terms)."""
    assoc = word_commodity_associations()
    return {w: dict(c) for w, c in assoc.items() if w != 'ku-ro' and len(c) <= 2}


def commodity_generalists():
    """Words appearing across 3+ commodity types (place names, officials)."""
    assoc = word_commodity_associations()
    return {w: dict(c) for w, c in assoc.items() if w != 'ku-ro' and len(c) >= 3}


# =============================================================================
# SITE DISTRIBUTION ANALYSIS
# =============================================================================

def word_site_distribution():
    """For each word, count which sites it appears at."""
    distribution = defaultdict(Counter)
    corpus = get_all()
    for doc_id, entry in corpus.items():
        site = entry.get('site', 'unknown')
        for line in entry.get('lines', []):
            for part in line.replace('|', '.').split('.'):
                w = part.strip()
                if w and len(w) > 1 and not any(w.startswith(i) for i in IDEOGRAMS):
                    try:
                        float(w)
                    except ValueError:
                        distribution[w][site] += 1
    return dict(distribution)


def pan_cretan_words(min_sites=3):
    """Words at 3+ sites - standard administrative/religious vocabulary."""
    dist = word_site_distribution()
    return {w: dict(s) for w, s in dist.items() if len(s) >= min_sites}


def site_unique_words():
    """Words at only one site - potential local terms or names."""
    dist = word_site_distribution()
    return {w: dict(s) for w, s in dist.items() if len(s) == 1}


# =============================================================================
# COMPARISON WITH LINEAR B
# =============================================================================

LINEAR_B_SYLLABLE_FREQ = {
    'a': 0.065, 'e': 0.045, 'i': 0.035, 'o': 0.040, 'u': 0.020,
    'ka': 0.030, 'ke': 0.015, 'ki': 0.025, 'ko': 0.030, 'ku': 0.020,
    'da': 0.025, 'de': 0.020, 'di': 0.015, 'do': 0.020, 'du': 0.010,
    'ja': 0.020, 'je': 0.005, 'jo': 0.010,
    'ma': 0.025, 'me': 0.020, 'mi': 0.015, 'mo': 0.010, 'mu': 0.005,
    'na': 0.020, 'ne': 0.015, 'ni': 0.015, 'no': 0.020, 'nu': 0.008,
    'pa': 0.025, 'pe': 0.010, 'pi': 0.010, 'po': 0.015, 'pu': 0.008,
    'ra': 0.025, 're': 0.020, 'ri': 0.020, 'ro': 0.025, 'ru': 0.015,
    'sa': 0.020, 'se': 0.012, 'si': 0.015, 'so': 0.008, 'su': 0.015,
    'ta': 0.030, 'te': 0.025, 'ti': 0.020, 'to': 0.030, 'tu': 0.010,
    'wa': 0.015, 'we': 0.008, 'wi': 0.005, 'wo': 0.010,
    'qa': 0.008, 'qe': 0.005,
    'za': 0.005, 'ze': 0.003,
}


def compare_with_linear_b():
    """Compare Linear A syllable frequencies with Linear B (Mycenaean Greek)."""
    la_freq = get_syllable_frequencies()
    la_total = sum(la_freq.values())
    if la_total == 0:
        return {'correlation': 0, 'comparisons': []}
    la_norm = {s: c / la_total for s, c in la_freq.items()}
    common = set(la_norm.keys()) & set(LINEAR_B_SYLLABLE_FREQ.keys())
    if len(common) < 3:
        return {'correlation': 0, 'comparisons': [], 'common_syllables': len(common)}
    comparisons, la_vals, lb_vals = [], [], []
    for syl in sorted(common):
        la_f = la_norm.get(syl, 0)
        lb_f = LINEAR_B_SYLLABLE_FREQ.get(syl, 0)
        comparisons.append({
            'syllable': syl, 'linear_a_freq': la_f, 'linear_b_freq': lb_f,
            'ratio': la_f / lb_f if lb_f > 0 else float('inf'),
            'difference': la_f - lb_f,
        })
        la_vals.append(la_f)
        lb_vals.append(lb_f)
    n = len(la_vals)
    mean_a = sum(la_vals) / n
    mean_b = sum(lb_vals) / n
    cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(la_vals, lb_vals))
    var_a = sum((a - mean_a) ** 2 for a in la_vals)
    var_b = sum((b - mean_b) ** 2 for b in lb_vals)
    denom = math.sqrt(var_a * var_b)
    correlation = cov / denom if denom > 0 else 0
    comparisons.sort(key=lambda x: abs(x['difference']), reverse=True)
    return {
        'correlation': correlation, 'common_syllables': len(common),
        'la_only': sorted(set(la_norm.keys()) - set(LINEAR_B_SYLLABLE_FREQ.keys())),
        'lb_only': sorted(set(LINEAR_B_SYLLABLE_FREQ.keys()) - set(la_norm.keys())),
        'comparisons': comparisons,
    }


# =============================================================================
# FULL ANALYSIS RUNNER
# =============================================================================

def run_full_analysis():
    """Run all frequency analyses and return comprehensive results."""
    results = {}

    wf = word_frequency_table()
    results['word_frequency'] = {
        'total_tokens': sum(w['count'] for w in wf),
        'unique_types': len(wf),
        'type_token_ratio': len(wf) / sum(w['count'] for w in wf) if wf else 0,
        'top_20': wf[:20],
        'hapax_legomena': [w for w in wf if w['count'] == 1],
    }
    results['word_lengths'] = word_length_distribution()

    syl_freq = get_syllable_frequencies()
    results['syllable_frequency'] = {
        'total_syllable_tokens': sum(syl_freq.values()),
        'unique_syllables': len(syl_freq),
        'top_20': syl_freq.most_common(20),
        'entropy': shannon_entropy(syl_freq),
    }

    bi = syllable_bigrams()
    results['syllable_bigrams'] = {
        'unique_bigrams': len(bi),
        'top_20': [(f"{a}-{b}", c) for (a, b), c in bi.most_common(20)],
        'conditional_entropy': conditional_entropy(bi, syl_freq),
    }

    tri = syllable_trigrams()
    results['syllable_trigrams'] = {
        'unique_trigrams': len(tri),
        'top_20': [(f"{a}-{b}-{c}", ct) for (a, b, c), ct in tri.most_common(20)],
    }

    pmi = mutual_information_pairs()
    results['pmi'] = {
        'top_20_associated': pmi[:20] if pmi else [],
        'bottom_10_avoided': pmi[-10:] if len(pmi) >= 10 else pmi,
    }

    pos = positional_frequencies()
    results['positional'] = {
        'top_10_initial': pos['initial'].most_common(10),
        'top_10_final': pos['final'].most_common(10),
        'top_10_medial': pos['medial'].most_common(10),
        'initial_entropy': shannon_entropy(pos['initial']),
        'final_entropy': shannon_entropy(pos['final']),
    }

    zipf = zipf_analysis()
    results['zipf'] = {
        'exponent': zipf['exponent'], 'r_squared': zipf['r_squared'],
        'zipf_constant': zipf['zipf_constant'],
        'is_zipfian': zipf['r_squared'] > 0.85,
        'interpretation': (
            'Strong Zipfian fit - consistent with natural language'
            if zipf['r_squared'] > 0.9
            else 'Moderate Zipfian fit - broadly natural but small corpus'
            if zipf['r_squared'] > 0.8
            else 'Weak Zipfian fit - may reflect corpus limitations'
        ),
    }

    lb_comp = compare_with_linear_b()
    results['linear_b_comparison'] = {
        'correlation': lb_comp['correlation'],
        'common_syllables': lb_comp.get('common_syllables', 0),
        'interpretation': (
            'High correlation with Linear B Greek - similar phonotactics'
            if lb_comp['correlation'] > 0.7
            else 'Moderate correlation - some shared features'
            if lb_comp['correlation'] > 0.4
            else 'Low correlation - different phonological profile from Mycenaean Greek'
        ),
        'top_divergences': lb_comp.get('comparisons', [])[:10],
        'la_unique_syllables': lb_comp.get('la_only', []),
    }

    gen = commodity_generalists()
    spec = commodity_specialists()
    results['semantic_fields'] = {
        'generalists': gen, 'specialists': spec,
        'pan_cretan': pan_cretan_words(), 'site_unique': site_unique_words(),
    }
    return results


def print_analysis():
    """Print a human-readable analysis report."""
    results = run_full_analysis()
    print("=" * 70)
    print("LINEAR A FREQUENCY ANALYSIS")
    print("=" * 70)

    wf = results['word_frequency']
    print(f"\n--- WORD FREQUENCY ---")
    print(f"Total word tokens: {wf['total_tokens']}")
    print(f"Unique word types: {wf['unique_types']}")
    print(f"Type-token ratio: {wf['type_token_ratio']:.3f}")
    print(f"Hapax legomena: {len(wf['hapax_legomena'])}")
    print(f"\nTop 20 words:")
    for w in wf['top_20']:
        print(f"  {w['rank']:3d}. {w['word']:25s}  count={w['count']:3d}  "
              f"freq={w['frequency']:.3f}  syls={w['syllable_count']}")

    print(f"\n--- WORD LENGTH DISTRIBUTION (syllables) ---")
    for length, count in results['word_lengths'].items():
        print(f"  {length} syllables: {count:3d}  {'#' * count}")

    sf = results['syllable_frequency']
    print(f"\n--- SYLLABLE FREQUENCY ---")
    print(f"Total tokens: {sf['total_syllable_tokens']}, Unique: {sf['unique_syllables']}")
    print(f"Entropy: {sf['entropy']:.3f} bits")
    for syl, count in sf['top_20']:
        print(f"  {syl:8s}: {count}")

    bi = results['syllable_bigrams']
    print(f"\n--- SYLLABLE BIGRAMS ---")
    print(f"Unique: {bi['unique_bigrams']}, H(Y|X): {bi['conditional_entropy']:.3f} bits")
    for bg, count in bi['top_20']:
        print(f"  {bg:12s}: {count}")

    pmi = results['pmi']
    if pmi['top_20_associated']:
        print(f"\n--- MUTUAL INFORMATION ---")
        for item in pmi['top_20_associated'][:15]:
            print(f"  {item['display']:12s}  PMI={item['pmi']:+.3f}  n={item['count']}")

    pos = results['positional']
    print(f"\n--- POSITIONAL PREFERENCES ---")
    print(f"Initial entropy: {pos['initial_entropy']:.3f}, Final entropy: {pos['final_entropy']:.3f}")
    print("Initial:")
    for s, c in pos['top_10_initial']:
        print(f"  {s:8s}: {c}")
    print("Final:")
    for s, c in pos['top_10_final']:
        print(f"  {s:8s}: {c}")

    z = results['zipf']
    print(f"\n--- ZIPF'S LAW ---")
    print(f"Exponent: {z['exponent']:.3f} (ideal ~1.0), R2: {z['r_squared']:.4f}")
    print(f"{z['interpretation']}")

    lb = results['linear_b_comparison']
    print(f"\n--- LINEAR B COMPARISON ---")
    print(f"Correlation: {lb['correlation']:.4f}, Common syllables: {lb['common_syllables']}")
    print(f"{lb['interpretation']}")
    if lb.get('top_divergences'):
        for d in lb['top_divergences'][:5]:
            print(f"  {d['syllable']:6s}  LA={d['linear_a_freq']:.4f}  LB={d['linear_b_freq']:.4f}")

    sem = results['semantic_fields']
    print(f"\n--- PAN-CRETAN WORDS (3+ sites) ---")
    for w, sites in sorted(sem['pan_cretan'].items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {w:25s}  sites={len(sites):2d}")

    print(f"\n--- COMMODITY GENERALISTS (3+ commodities) ---")
    for w, c in sorted(sem['generalists'].items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {w:25s}  commodities={len(c):2d}  ({', '.join(sorted(c.keys()))})")

    print(f"\n{'=' * 70}")
    return results


if __name__ == '__main__':
    print_analysis()
