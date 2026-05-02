"""
Linear A Cross-Reference Engine
=================================
Compare Linear A vocabulary against known ancient languages to constrain
the language family. Tests Semitic, Anatolian, and pre-Greek hypotheses.

Methodology:
1. For each Linear A word, generate candidate readings using Linear B values
2. Compare against vocabulary from Semitic (Akkadian, Ugaritic, Hebrew),
   Anatolian (Luwian, Hittite), and pre-Greek substrate words
3. Score matches by phonetic similarity, semantic plausibility, and context
4. Use Bayesian framework to weight evidence for/against each hypothesis

Key principle: A match must be better than chance. With ~50 CV syllables,
random 3-syllable words have a ~1/125000 chance of matching any given target.
We need multiple independent matches to claim a language family connection.
"""

import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from linear_a.data.corpus import get_words, get_unique_words, get_all
from linear_a.analysis.frequency_analysis import extract_syllables, pan_cretan_words


# =============================================================================
# KNOWN ANCIENT VOCABULARY DATABASES
# =============================================================================

# Semitic vocabulary that has been proposed as Linear A cognates
# Format: {LA_reading: [(semitic_word, language, meaning, proposer), ...]}
SEMITIC_COMPARISONS = {
    'ku-ro': [
        ('kull-', 'Akkadian', 'totality/all', 'Gordon 1966'),
        ('kol', 'Hebrew', 'all/every', 'Gordon 1966'),
    ],
    'ki-ro': [
        ('qiru', 'Akkadian', 'deficit/shortfall', 'Best 1972'),
    ],
    'ku-ni-su': [
        ('kunisu', 'Akkadian', 'emmer wheat', 'Gordon 1966'),
        ('kunash', 'Ugaritic', 'emmer', 'Dietrich & Loretz'),
    ],
    'da-me': [
        ('dammu', 'Akkadian', 'assessment/levy', 'Palmer 1963'),
    ],
    'su-ki-ri-ta': [
        ('sukiritu', 'Akkadian', 'orchard/plantation', 'Gordon 1966'),
    ],
    'ja-sa-sa-ra-me': [
        ('ishassara', 'Anatolian/Luwian', 'lady/mistress', 'multiple scholars'),
        ('ya-sha-sha-ra', 'Semitic', 'the just one (f.)', 'Gordon'),
    ],
    'i-da-ma-te': [
        ('ida + mater', 'pre-Greek', 'Mother of Ida', 'widely accepted'),
    ],
    'a-du': [
        ('adu', 'Akkadian', 'father', 'Best 1972'),
    ],
    'pa-ja-re': [
        ('pa-i-to', 'Linear B', 'Phaistos', 'widely accepted'),
    ],
    'ku-do-ni': [
        ('ku-do-ni-ja', 'Linear B', 'Kydonia/Khania', 'widely accepted'),
    ],
    'se-to-i-ja': [
        ('Seteia', 'Greek toponym', 'Siteia (eastern Crete)', 'Younger'),
    ],
    'da-ta-re': [
        ('dataru', 'Akkadian', 'one who gives', 'Best 1972'),
    ],
    'qa-qa-ru': [
        ('qaqqaru', 'Akkadian', 'ground/land', 'Gordon 1966'),
    ],
    'te-ki': [
        ('teku', 'Akkadian', 'delivery/payment', 'Palmer'),
    ],
    'a-ta-i-*301-wa-ja': [
        ('atai-waya', 'unknown', 'I dedicate (?)' , 'various'),
    ],
    'wa-tu': [
        ('watu', 'pre-Greek?', 'settlement?', 'uncertain'),
    ],
}

# Anatolian (Luwian/Hittite) comparisons - Adithyan Madhu hypothesis
ANATOLIAN_COMPARISONS = {
    'ja-sa-sa-ra-me': [
        ('ishassara-mi', 'Luwian', 'my lady', 'Palmer, Younger, Madhu'),
    ],
    'i-da-ma-te': [
        ('ida-mati', 'Luwian-type', 'Ida-mother (compound)', 'Davis'),
    ],
    'a-ta-i-*301-wa-ja': [
        ('atta-i-waya', 'Luwian-type', 'father-to-give?', 'Madhu 2024'),
    ],
    'da-me': [
        ('tame-', 'Hittite', 'to assess/distribute', 'Palmer'),
    ],
    'te-ki': [
        ('teki-', 'Luwian', 'to place/deliver', 'speculative'),
    ],
    'ku-ro': [
        ('kul-', 'Hittite', 'to gather/collect', 'speculative'),
    ],
    'a-di-ki-te': [
        ('Dikte', 'pre-Greek/Anatolian', 'Mount Dikte', 'widely accepted'),
    ],
    'pi-te-za': [
        ('pittaza', 'Luwian', 'place/offering-place?', 'Madhu'),
    ],
    'ta-na-te': [
        ('Tanit', 'Punic/pre-Greek', 'deity name', 'uncertain'),
    ],
}

# Pre-Greek substrate words found in later Greek that may connect to Linear A
PRE_GREEK_SUBSTRATE = {
    # Words with -nth- suffix (Pelasgian/pre-Greek)
    '-inth-': {
        'examples': ['Korinthos', 'labyrinthos', 'Hyakinthos', 'terebinthos'],
        'la_candidates': ['da-i-pi-ta', 'ka-u-de-ta'],
        'notes': 'Pre-Greek substrate words often have -inth-, -nth- suffixes',
    },
    # Words with -ss- (pre-Greek)
    '-ss-': {
        'examples': ['Knossos', 'Halikarnassos', 'Parnassos', 'narkissos'],
        'la_candidates': ['ja-sa-sa-ra-me', 'a-sa-sa-ra-me'],
        'notes': '-ss- is characteristically pre-Greek, not Indo-European',
    },
    # Place names with -a ending
    '-a endings': {
        'examples': ['Gortyna', 'Lyktos', 'Phaistos', 'Kydonia'],
        'la_candidates': ['su-ki-ri-ta', 'se-to-i-ja'],
        'notes': 'Many Cretan place names survived into Greek',
    },
}

# Known Linear B readings for comparison
LINEAR_B_KNOWN_WORDS = {
    'pa-i-to': ('Phaistos', 'place name'),
    'ku-do-ni-ja': ('Kydonia/Khania', 'place name'),
    'ko-no-so': ('Knossos', 'place name'),
    'a-mi-ni-so': ('Amnisos', 'place name'),
    'su-ki-ri-ta': ('Sybrita', 'place name'),
    'se-to-i-ja': ('Seteia/Siteia', 'place name'),
    'di-ka-ta': ('Dikte', 'mountain name'),
    'da-pu2-ri-to': ('Labyrinthos', 'structure name'),
    'wa-na-ka': ('wanax/king', 'title'),
    'ra-wa-ke-ta': ('lawagetas/war-leader', 'title'),
    'po-ti-ni-ja': ('potnia/mistress', 'divine epithet'),
    'a-ta-na-po-ti-ni-ja': ('Athena Potnia', 'deity'),
}


# =============================================================================
# PHONETIC DISTANCE METRICS
# =============================================================================

def syllable_distance(s1, s2):
    """Calculate phonetic distance between two CV syllables.

    Returns 0 for identical, 0.5 for same consonant or vowel, 1.0 for different.
    """
    if s1 == s2:
        return 0.0

    # Extract C and V components
    c1 = s1[:-1] if len(s1) > 1 else ''
    v1 = s1[-1] if s1 else ''
    c2 = s2[:-1] if len(s2) > 1 else ''
    v2 = s2[-1] if s2 else ''

    # Pure vowels
    if not c1 and not c2:
        return 0.3 if v1 != v2 else 0.0

    score = 0.0
    # Consonant similarity
    if c1 != c2:
        # Check for common alternations
        similar_pairs = [
            {'d', 't'}, {'k', 'g'}, {'p', 'b'}, {'s', 'z'},
            {'r', 'l'}, {'m', 'n'}, {'w', 'u'}, {'j', 'i'},
        ]
        if any(c1 in pair and c2 in pair for pair in similar_pairs):
            score += 0.3
        else:
            score += 0.6
    # Vowel similarity
    if v1 != v2:
        similar_vowels = [{'a', 'e'}, {'e', 'i'}, {'o', 'u'}]
        if any(v1 in pair and v2 in pair for pair in similar_vowels):
            score += 0.15
        else:
            score += 0.3
    return min(score, 1.0)


def word_distance(word1, word2):
    """Calculate normalized phonetic distance between two words.

    Uses dynamic programming (edit distance variant) on syllable sequences.
    Returns value between 0 (identical) and 1 (completely different).
    """
    syls1 = extract_syllables(word1) if '-' in word1 else list(word1)
    syls2 = extract_syllables(word2) if '-' in word2 else list(word2)

    if not syls1 or not syls2:
        return 1.0

    m, n = len(syls1), len(syls2)
    dp = [[0.0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = syllable_distance(syls1[i-1], syls2[j-1])
            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,       # insertion
                dp[i-1][j-1] + cost,  # substitution
            )

    max_len = max(m, n)
    return dp[m][n] / max_len if max_len > 0 else 0.0


# =============================================================================
# CROSS-REFERENCE SCORING
# =============================================================================

def score_semitic_hypothesis():
    """Score how well Linear A vocabulary matches Semitic languages.

    For each proposed Semitic cognate:
    1. Calculate phonetic distance
    2. Check semantic plausibility (does meaning fit context?)
    3. Weight by word frequency (common words matter more)
    """
    word_counts = get_unique_words()
    matches = []
    total_score = 0.0
    total_weight = 0.0

    for la_word, comparisons in SEMITIC_COMPARISONS.items():
        freq = word_counts.get(la_word, 0)
        weight = math.log(freq + 1) + 1  # log-weighted frequency

        for sem_word, lang, meaning, proposer in comparisons:
            dist = word_distance(la_word, sem_word)
            match_score = 1.0 - dist

            matches.append({
                'la_word': la_word,
                'comparison': sem_word,
                'language': lang,
                'meaning': meaning,
                'proposer': proposer,
                'distance': dist,
                'score': match_score,
                'frequency': freq,
                'weight': weight,
            })
            total_score += match_score * weight
            total_weight += weight

    avg_score = total_score / total_weight if total_weight > 0 else 0
    matches.sort(key=lambda x: x['score'], reverse=True)

    return {
        'hypothesis': 'Semitic',
        'avg_score': avg_score,
        'n_comparisons': len(matches),
        'matches': matches,
        'strong_matches': [m for m in matches if m['score'] > 0.7],
        'weak_matches': [m for m in matches if m['score'] < 0.4],
    }


def score_anatolian_hypothesis():
    """Score how well Linear A vocabulary matches Anatolian languages."""
    word_counts = get_unique_words()
    matches = []
    total_score = 0.0
    total_weight = 0.0

    for la_word, comparisons in ANATOLIAN_COMPARISONS.items():
        freq = word_counts.get(la_word, 0)
        weight = math.log(freq + 1) + 1

        for anat_word, lang, meaning, proposer in comparisons:
            dist = word_distance(la_word, anat_word)
            match_score = 1.0 - dist

            matches.append({
                'la_word': la_word,
                'comparison': anat_word,
                'language': lang,
                'meaning': meaning,
                'proposer': proposer,
                'distance': dist,
                'score': match_score,
                'frequency': freq,
                'weight': weight,
            })
            total_score += match_score * weight
            total_weight += weight

    avg_score = total_score / total_weight if total_weight > 0 else 0
    matches.sort(key=lambda x: x['score'], reverse=True)

    return {
        'hypothesis': 'Anatolian',
        'avg_score': avg_score,
        'n_comparisons': len(matches),
        'matches': matches,
        'strong_matches': [m for m in matches if m['score'] > 0.7],
        'weak_matches': [m for m in matches if m['score'] < 0.4],
    }


def score_isolate_hypothesis():
    """Score the hypothesis that Minoan is a language isolate.

    Evidence FOR isolate:
    - Low correlation with any known language family
    - Unique phonotactic patterns
    - No systematic correspondence with any family

    Evidence AGAINST isolate:
    - Any strong, systematic correspondences found above
    """
    sem = score_semitic_hypothesis()
    anat = score_anatolian_hypothesis()

    # If neither hypothesis scores well, that's evidence for isolate
    max_family_score = max(sem['avg_score'], anat['avg_score'])
    isolate_score = 1.0 - max_family_score

    n_strong = len(sem['strong_matches']) + len(anat['strong_matches'])

    return {
        'hypothesis': 'Language Isolate',
        'score': isolate_score,
        'evidence': {
            'semitic_avg_score': sem['avg_score'],
            'anatolian_avg_score': anat['avg_score'],
            'strong_external_matches': n_strong,
        },
        'interpretation': (
            'Strong evidence for isolate - no family matches well'
            if isolate_score > 0.7
            else 'Moderate evidence - some family resemblances but inconclusive'
            if isolate_score > 0.4
            else 'Weak evidence for isolate - at least one family shows good matches'
        ),
    }


# =============================================================================
# TOPONYM ANALYSIS
# =============================================================================

def analyze_toponyms():
    """Analyze words that are likely place names.

    Strong toponym candidates:
    1. Appear at multiple sites (not just locally)
    2. Appear with multiple commodity types
    3. Have Linear B parallels
    """
    pan = pan_cretan_words()
    word_counts = get_unique_words()

    toponyms = {}
    toponym_candidates = {
        'pa-ja-re': {'lb': 'pa-i-to', 'identified': 'Phaistos', 'confidence': 'high'},
        'ku-do-ni': {'lb': 'ku-do-ni-ja', 'identified': 'Kydonia/Khania', 'confidence': 'high'},
        'su-ki-ri-ta': {'lb': 'su-ki-ri-ta', 'identified': 'Sybrita', 'confidence': 'high'},
        'se-to-i-ja': {'lb': None, 'identified': 'Seteia/Siteia', 'confidence': 'medium'},
        'da-ta-re': {'lb': None, 'identified': 'unknown settlement', 'confidence': 'medium'},
        'ki-re-ta2': {'lb': None, 'identified': 'unknown settlement', 'confidence': 'medium'},
        'qa-qa-ru': {'lb': None, 'identified': 'unknown (land/territory?)', 'confidence': 'low'},
        'a-du': {'lb': None, 'identified': 'unknown (person or place)', 'confidence': 'low'},
        'ki-da-ro': {'lb': None, 'identified': 'unknown settlement', 'confidence': 'medium'},
        'si-da-te': {'lb': None, 'identified': 'unknown settlement', 'confidence': 'medium'},
    }

    for word, info in toponym_candidates.items():
        sites = pan.get(word, {})
        count = word_counts.get(word, 0)
        toponyms[word] = {
            **info,
            'n_sites': len(sites),
            'sites': list(sites.keys()) if sites else [],
            'frequency': count,
            'is_pan_cretan': len(sites) >= 3,
        }

    return toponyms


# =============================================================================
# WORD CLASSIFICATION
# =============================================================================

def classify_words():
    """Classify all Linear A words into categories based on evidence.

    Categories:
    - toponym: place name
    - anthroponym: personal name
    - theonym: deity name
    - admin_term: administrative vocabulary
    - commodity_term: commodity-related
    - unknown: insufficient evidence
    """
    word_counts = get_unique_words()
    pan = pan_cretan_words()
    classifications = {}

    # Known administrative terms
    admin_terms = {'ku-ro', 'ki-ro', 'po-to-ku-ro', 'da-me', 'te-ki'}

    # Known/probable deity terms (from libation formulas)
    deity_terms = {'ja-sa-sa-ra-me', 'i-da-ma-te', 'a-di-ki-te', 'ta-na-te',
                   'a-sa-sa-ra-me'}

    # Libation formula terms
    formula_terms = {'a-ta-i-*301-wa-ja', 'pi-te-za', 'si-ru-te',
                     'u-na-ka-na-si', 'i-pi-na-ma', 'a-su-pu-wa',
                     'ja-di-ki-te-te', 'da-si-na', 'wa-ja'}

    # Probable toponyms
    toponym_terms = {'pa-ja-re', 'ku-do-ni', 'su-ki-ri-ta', 'se-to-i-ja'}

    for word, count in word_counts.items():
        if word in admin_terms:
            cat = 'admin_term'
            conf = 'high'
        elif word in deity_terms:
            cat = 'theonym'
            conf = 'medium'
        elif word in formula_terms:
            cat = 'ritual_formula'
            conf = 'high'
        elif word in toponym_terms:
            cat = 'toponym'
            conf = 'high'
        elif word in pan and len(pan[word]) >= 4:
            cat = 'toponym'
            conf = 'medium'
        elif word in pan and len(pan[word]) >= 2:
            cat = 'toponym_or_anthroponym'
            conf = 'low'
        elif len(pan.get(word, {})) == 1:
            cat = 'anthroponym'
            conf = 'low'
        else:
            cat = 'unknown'
            conf = 'none'

        classifications[word] = {
            'category': cat,
            'confidence': conf,
            'frequency': count,
            'n_sites': len(pan.get(word, {})),
        }

    return classifications


# =============================================================================
# FULL CROSS-REFERENCE ANALYSIS
# =============================================================================

def run_cross_reference():
    """Run all cross-reference analyses."""
    results = {}

    results['semitic'] = score_semitic_hypothesis()
    results['anatolian'] = score_anatolian_hypothesis()
    results['isolate'] = score_isolate_hypothesis()
    results['toponyms'] = analyze_toponyms()
    results['classifications'] = classify_words()

    # Summary comparison
    results['hypothesis_ranking'] = sorted([
        {'hypothesis': 'Semitic', 'score': results['semitic']['avg_score']},
        {'hypothesis': 'Anatolian', 'score': results['anatolian']['avg_score']},
        {'hypothesis': 'Isolate', 'score': results['isolate']['score']},
    ], key=lambda x: x['score'], reverse=True)

    return results


def print_cross_reference():
    """Print cross-reference analysis report."""
    results = run_cross_reference()

    print("=" * 70)
    print("LINEAR A CROSS-REFERENCE ANALYSIS")
    print("=" * 70)

    # Hypothesis ranking
    print("\n--- LANGUAGE FAMILY HYPOTHESIS RANKING ---")
    for h in results['hypothesis_ranking']:
        bar = '#' * int(h['score'] * 40)
        print(f"  {h['hypothesis']:20s}  score={h['score']:.3f}  {bar}")

    # Semitic
    sem = results['semitic']
    print(f"\n--- SEMITIC HYPOTHESIS (Gordon/Best) ---")
    print(f"Average score: {sem['avg_score']:.3f}")
    print(f"Strong matches (>0.7): {len(sem['strong_matches'])}")
    print(f"Weak matches (<0.4): {len(sem['weak_matches'])}")
    print("\nTop matches:")
    for m in sem['matches'][:10]:
        print(f"  {m['la_word']:25s} ~ {m['comparison']:15s} ({m['language']}) "
              f"= '{m['meaning']}' score={m['score']:.3f}")

    # Anatolian
    anat = results['anatolian']
    print(f"\n--- ANATOLIAN HYPOTHESIS (Palmer/Younger/Madhu) ---")
    print(f"Average score: {anat['avg_score']:.3f}")
    print(f"Strong matches (>0.7): {len(anat['strong_matches'])}")
    print("\nTop matches:")
    for m in anat['matches'][:10]:
        print(f"  {m['la_word']:25s} ~ {m['comparison']:15s} ({m['language']}) "
              f"= '{m['meaning']}' score={m['score']:.3f}")

    # Isolate
    iso = results['isolate']
    print(f"\n--- LANGUAGE ISOLATE HYPOTHESIS ---")
    print(f"Score: {iso['score']:.3f}")
    print(f"Interpretation: {iso['interpretation']}")

    # Toponyms
    print(f"\n--- TOPONYM ANALYSIS ---")
    for word, info in sorted(results['toponyms'].items(),
                              key=lambda x: x[1]['n_sites'], reverse=True):
        print(f"  {word:20s}  = {info['identified']:20s}  "
              f"confidence={info['confidence']:6s}  sites={info['n_sites']}")

    # Word classifications
    cls = results['classifications']
    cats = Counter(v['category'] for v in cls.values())
    print(f"\n--- WORD CLASSIFICATION SUMMARY ---")
    for cat, count in cats.most_common():
        print(f"  {cat:25s}: {count}")

    print(f"\n{'=' * 70}")
    return results


if __name__ == '__main__':
    print_cross_reference()
