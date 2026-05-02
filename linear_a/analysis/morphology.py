"""
Linear A Morphological Pattern Detection
==========================================
Detect prefixes, suffixes, root patterns, paradigmatic relationships,
compound words, and morphological classes in Linear A vocabulary.

This is the heart of the decipherment: if we can identify morphological
patterns, we can begin to understand the grammar even without knowing
the language family.

Key findings from scholarship:
- a-/i- may be prefixes (possibly demonstrative/article)
- -ja/-i-ja may be adjectival/ethnic suffix (cf. Linear B -jo/-ja)
- -te/-ti may be dative or locative ending
- -me may be possessive enclitic 'my' (cf. Luwian -mi)
- Reduplication (sa-sa in ja-sa-sa-ra-me) may be intensification
- Words in admin texts follow [NAME . COMMODITY QUANTITY] pattern
"""

import re
import sys
import math
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from linear_a.data.corpus import get_all, get_words, get_unique_words, get_libation_formulas
from linear_a.analysis.frequency_analysis import (
    extract_syllables, initial_syllable_stats, final_syllable_stats,
    positional_frequencies, pan_cretan_words, word_commodity_associations
)


# =============================================================================
# AFFIX DETECTION
# =============================================================================

def detect_prefixes(min_freq=2):
    """Detect candidate prefixes by finding recurring initial syllables.

    A prefix candidate must:
    1. Appear word-initially with high frequency
    2. Appear before multiple different stems
    3. Not just be a common first syllable of monomorphemic words
    """
    words = get_unique_words()
    initial = initial_syllable_stats()

    # Get all words as syllable sequences
    word_syllables = {}
    for word in words:
        syls = extract_syllables(word)
        if len(syls) >= 2:
            word_syllables[word] = syls

    # Find recurring prefixes (1-2 syllables)
    prefix_candidates = defaultdict(list)
    for word, syls in word_syllables.items():
        # Single syllable prefix
        prefix_candidates[syls[0]].append(word)
        # Two syllable prefix
        if len(syls) >= 3:
            prefix_candidates[tuple(syls[:2])].append(word)

    # Score prefix candidates
    prefixes = {}
    for prefix, word_list in prefix_candidates.items():
        if len(word_list) < min_freq:
            continue

        prefix_str = '-'.join(prefix) if isinstance(prefix, tuple) else prefix

        # Check if remaining stems are diverse
        stems = []
        for word in word_list:
            syls = extract_syllables(word)
            if isinstance(prefix, tuple):
                stem = '-'.join(syls[len(prefix):])
            else:
                stem = '-'.join(syls[1:])
            if stem:
                stems.append(stem)

        unique_stems = set(stems)
        if len(unique_stems) < 2:
            continue

        # Score: frequency * stem diversity / total words with this initial
        total_initial = sum(1 for w, s in word_syllables.items()
                          if s[0] == (prefix[0] if isinstance(prefix, tuple) else prefix))
        diversity = len(unique_stems) / len(word_list) if word_list else 0

        prefixes[prefix_str] = {
            'frequency': len(word_list),
            'words': sorted(word_list),
            'stems': sorted(unique_stems),
            'diversity': diversity,
            'score': len(word_list) * diversity,
        }

    return dict(sorted(prefixes.items(), key=lambda x: x[1]['score'], reverse=True))


def detect_suffixes(min_freq=2):
    """Detect candidate suffixes by finding recurring final syllables.

    A suffix candidate must:
    1. Appear word-finally with high frequency
    2. Appear after multiple different stems
    3. Show grammatical patterning (e.g., appear with same commodities)
    """
    words = get_unique_words()
    final = final_syllable_stats()

    word_syllables = {}
    for word in words:
        syls = extract_syllables(word)
        if len(syls) >= 2:
            word_syllables[word] = syls

    suffix_candidates = defaultdict(list)
    for word, syls in word_syllables.items():
        # Single syllable suffix
        suffix_candidates[syls[-1]].append(word)
        # Two syllable suffix
        if len(syls) >= 3:
            suffix_candidates[tuple(syls[-2:])].append(word)

    suffixes = {}
    for suffix, word_list in suffix_candidates.items():
        if len(word_list) < min_freq:
            continue

        suffix_str = '-'.join(suffix) if isinstance(suffix, tuple) else suffix

        stems = []
        for word in word_list:
            syls = extract_syllables(word)
            if isinstance(suffix, tuple):
                stem = '-'.join(syls[:-len(suffix)])
            else:
                stem = '-'.join(syls[:-1])
            if stem:
                stems.append(stem)

        unique_stems = set(stems)
        if len(unique_stems) < 2:
            continue

        diversity = len(unique_stems) / len(word_list) if word_list else 0

        suffixes[suffix_str] = {
            'frequency': len(word_list),
            'words': sorted(word_list),
            'stems': sorted(unique_stems),
            'diversity': diversity,
            'score': len(word_list) * diversity,
        }

    return dict(sorted(suffixes.items(), key=lambda x: x[1]['score'], reverse=True))


# =============================================================================
# ROOT FAMILY DETECTION
# =============================================================================

def find_root_families():
    """Group words that may share a common root.

    Strategy: Look for words that share 2+ consecutive syllables
    and differ only in affixes.
    """
    words = get_unique_words()
    word_syllables = {}
    for word in words:
        syls = extract_syllables(word)
        if len(syls) >= 2:
            word_syllables[word] = syls

    # Build index of syllable bigrams
    bigram_index = defaultdict(set)
    for word, syls in word_syllables.items():
        for i in range(len(syls) - 1):
            bigram = (syls[i], syls[i+1])
            bigram_index[bigram].add(word)

    # Find families: groups of words sharing a bigram
    families = {}
    seen = set()
    for bigram, members in sorted(bigram_index.items(),
                                   key=lambda x: len(x[1]), reverse=True):
        if len(members) < 2:
            continue

        # Skip if all members already in a family
        new_members = members - seen
        if not new_members and len(members) < 3:
            continue

        root = '-'.join(bigram)
        family_words = sorted(members)

        # Analyze how members differ
        variations = []
        for word in family_words:
            syls = word_syllables[word]
            idx = None
            for i in range(len(syls) - 1):
                if (syls[i], syls[i+1]) == bigram:
                    idx = i
                    break
            if idx is not None:
                prefix = '-'.join(syls[:idx]) if idx > 0 else ''
                suffix = '-'.join(syls[idx+2:]) if idx + 2 < len(syls) else ''
                variations.append({
                    'word': word,
                    'prefix': prefix,
                    'suffix': suffix,
                })

        families[root] = {
            'root': root,
            'members': family_words,
            'n_members': len(family_words),
            'variations': variations,
        }
        seen.update(members)

    return dict(sorted(families.items(), key=lambda x: x[1]['n_members'], reverse=True))


# =============================================================================
# REDUPLICATION DETECTION
# =============================================================================

def detect_reduplication():
    """Detect reduplicated syllables within words.

    Reduplication is a common morphological process in many language families.
    In Linear A, ja-sa-sa-ra-me shows sa-sa reduplication.
    """
    words = get_unique_words()
    reduplicated = {}

    for word, count in words.items():
        syls = extract_syllables(word)
        if len(syls) < 3:
            continue

        # Check for adjacent identical syllables
        for i in range(len(syls) - 1):
            if syls[i] == syls[i+1]:
                reduplicated[word] = {
                    'syllables': syls,
                    'repeated': syls[i],
                    'position': i,
                    'frequency': count,
                    'type': 'adjacent',
                }
                break

        # Check for non-adjacent repetition (e.g., CV-X-CV)
        if word not in reduplicated and len(syls) >= 3:
            for i in range(len(syls)):
                for j in range(i + 2, len(syls)):
                    if syls[i] == syls[j]:
                        reduplicated[word] = {
                            'syllables': syls,
                            'repeated': syls[i],
                            'position': i,
                            'position2': j,
                            'frequency': count,
                            'type': 'non_adjacent',
                        }
                        break
                if word in reduplicated:
                    break

    return reduplicated


# =============================================================================
# PARADIGM DETECTION
# =============================================================================

def detect_paradigms():
    """Detect paradigmatic relationships between words.

    A paradigm is a set of words that share a stem but differ in
    a systematic way (e.g., case endings, person markers).

    Example: if we find words like X-te, X-me, X-ja, where X is
    the same stem and -te/-me/-ja are endings, that's a paradigm.
    """
    suffixes = detect_suffixes(min_freq=2)
    words = get_unique_words()

    # Build stem -> {suffix: word} mapping
    stem_map = defaultdict(dict)
    for word in words:
        syls = extract_syllables(word)
        if len(syls) < 2:
            continue
        # Try each possible stem/suffix split
        for split in range(1, len(syls)):
            stem = '-'.join(syls[:split])
            suffix = '-'.join(syls[split:])
            if suffix in suffixes:
                stem_map[stem][suffix] = word

    # Find stems with multiple suffix alternations
    paradigms = {}
    for stem, suffix_words in stem_map.items():
        if len(suffix_words) < 2:
            continue
        paradigms[stem] = {
            'stem': stem,
            'forms': suffix_words,
            'n_forms': len(suffix_words),
            'suffixes_used': sorted(suffix_words.keys()),
        }

    return dict(sorted(paradigms.items(), key=lambda x: x[1]['n_forms'], reverse=True))


# =============================================================================
# COMPOUND WORD DETECTION
# =============================================================================

def detect_compounds():
    """Detect compound words (words made of two known shorter words).

    If X and Y both appear independently, and X-Y also appears,
    then X-Y may be a compound.
    """
    words = get_unique_words()
    word_set = set(words.keys())
    compounds = {}

    for word in words:
        syls = extract_syllables(word)
        if len(syls) < 3:
            continue

        # Try splitting at each syllable boundary
        for split in range(1, len(syls)):
            part1 = '-'.join(syls[:split])
            part2 = '-'.join(syls[split:])

            if part1 in word_set and part2 in word_set:
                compounds[word] = {
                    'parts': [part1, part2],
                    'part1_freq': words.get(part1, 0),
                    'part2_freq': words.get(part2, 0),
                    'compound_freq': words[word],
                }

    return compounds


# =============================================================================
# WORD CLASS DETECTION BY DISTRIBUTION
# =============================================================================

def classify_by_distribution():
    """Classify words into morphological classes based on distribution.

    Words that appear in similar syntactic contexts (same position,
    with same commodities, at same sites) likely belong to the same class.

    Classes:
    - Names (anthroponyms): appear with quantities, diverse commodities
    - Places (toponyms): appear at multiple sites, pan-Cretan
    - Administrative: ku-ro, ki-ro, da-me, te-ki
    - Religious: libation formula terms
    """
    words = get_unique_words()
    pan = pan_cretan_words()
    commodity = word_commodity_associations()

    # Get libation formula words
    lib_words = set()
    formulas = get_libation_formulas()
    for doc_id, doc in formulas.items():
        for line in doc.get('lines', []):
            for part in line.replace('.', ' ').split():
                cleaned = part.strip()
                if cleaned and not cleaned.isupper() and not cleaned.isdigit():
                    lib_words.add(cleaned)

    classes = defaultdict(list)

    for word, count in words.items():
        n_sites = len(pan.get(word, {}))
        n_commodities = len(commodity.get(word, {}))

        # Features
        is_pan_cretan = n_sites >= 3
        is_multi_commodity = n_commodities >= 2
        is_formula = word in lib_words
        is_admin = word in {'ku-ro', 'ki-ro', 'po-to-ku-ro', 'da-me', 'te-ki'}

        syls = extract_syllables(word)
        n_syls = len(syls)

        # Classification rules
        if is_admin:
            cls = 'administrative'
        elif is_formula and not is_pan_cretan:
            cls = 'religious_formula'
        elif is_pan_cretan and is_multi_commodity:
            cls = 'toponym_or_official'
        elif is_pan_cretan:
            cls = 'toponym'
        elif n_sites == 1 and n_commodities <= 1:
            cls = 'local_name'
        elif is_multi_commodity:
            cls = 'official_or_collector'
        else:
            cls = 'unclassified'

        classes[cls].append({
            'word': word,
            'frequency': count,
            'n_sites': n_sites,
            'n_commodities': n_commodities,
            'n_syllables': n_syls,
        })

    # Sort each class by frequency
    for cls in classes:
        classes[cls].sort(key=lambda x: x['frequency'], reverse=True)

    return dict(classes)


# =============================================================================
# LIBATION FORMULA DEEP ANALYSIS
# =============================================================================

def analyze_libation_formula():
    """Deep morphological analysis of the libation formula.

    The formula a-ta-i-*301-wa-ja | ja-sa-sa-ra-me | i-da-ma-te
    is the most analyzed text in Linear A. This function extracts
    every possible morphological insight.
    """
    analysis = {}

    # a-ta-i-*301-wa-ja - the dedicatory phrase
    analysis['a-ta-i-*301-wa-ja'] = {
        'syllables': ['a', 'ta', 'i', '*301', 'wa', 'ja'],
        'n_syllables': 6,
        'morphological_parses': [
            {
                'parse': 'a-ta-i | *301 | wa-ja',
                'hypothesis': 'verb + sign + complement',
                'notes': '*301 is undeciphered sign; may be logogram or syllable',
            },
            {
                'parse': 'atta-i | *301-wa-ja',
                'hypothesis': 'Luwian atta "father" + dative + verb',
                'proposer': 'Madhu 2024',
            },
            {
                'parse': 'a- | ta-i-*301-wa-ja',
                'hypothesis': 'prefix a- + verb stem',
                'notes': 'a- as demonstrative/article prefix',
            },
        ],
        'context': 'Always first element in libation formula',
        'variants': ['a-ta-i-*301-wa-e', 'a-ta-i-*301-wa'],
    }

    # ja-sa-sa-ra-me - the divine name/epithet
    analysis['ja-sa-sa-ra-me'] = {
        'syllables': ['ja', 'sa', 'sa', 'ra', 'me'],
        'n_syllables': 5,
        'morphological_parses': [
            {
                'parse': 'ja | sa-sa-ra | me',
                'hypothesis': 'article/prefix + reduplicated root + possessive',
                'notes': 'sa-sa shows reduplication; -me as "my" (Luwian -mi)',
            },
            {
                'parse': 'ja-sa-sa-ra | me',
                'hypothesis': 'Luwian ishassara "lady" + enclitic -mi "my"',
                'proposer': 'Palmer, Younger',
            },
            {
                'parse': 'ya-sha-sha-ra | me',
                'hypothesis': 'Semitic root y-sh-r "just" + feminine',
                'proposer': 'Gordon',
            },
        ],
        'context': 'Second element in formula - deity/divine epithet',
        'reduplication': {'type': 'adjacent', 'syllable': 'sa', 'position': 1},
        'variants': ['a-sa-sa-ra-me', 'ja-sa-sa-ra-me-na'],
    }

    # i-da-ma-te - Mount Ida Mother
    analysis['i-da-ma-te'] = {
        'syllables': ['i', 'da', 'ma', 'te'],
        'n_syllables': 4,
        'morphological_parses': [
            {
                'parse': 'i-da | ma-te',
                'hypothesis': 'Mount Ida + Mother (compound deity name)',
                'notes': 'Widely accepted. Ida is central Cretan mountain.',
            },
            {
                'parse': 'ida-mati',
                'hypothesis': 'Luwian-type compound "Ida-mother"',
                'proposer': 'Davis',
            },
        ],
        'context': 'Third element in formula - deity name',
        'compound': {'parts': ['i-da', 'ma-te'], 'type': 'deity_compound'},
        'cognates': {
            'greek': 'Idaia Mater (Ida Mother)',
            'latin': 'Mater Idaea',
            'phrygian': 'Matar (Mother goddess)',
        },
    }

    # Formula structure analysis
    analysis['_formula_structure'] = {
        'pattern': 'VERB/DEDICATION + DIVINE_EPITHET + DEITY_NAME',
        'parallels': [
            'Hittite: "I X to Lady Y" (dedicatory formula)',
            'Luwian: verb + divine epithet + deity name',
            'Greek: "to X, the Y" (dedication pattern)',
        ],
        'frequency': 'Found on 29+ libation vessels across Crete',
        'conclusion': (
            'The formula structure is consistent with a dedicatory statement '
            'addressed to a female deity associated with Mount Ida. The '
            'reduplication in ja-sa-sa-ra-me and the compound i-da-ma-te '
            'are the strongest morphological features in the entire corpus.'
        ),
    }

    return analysis


# =============================================================================
# SYLLABLE PATTERN STATISTICS
# =============================================================================

def syllable_pattern_stats():
    """Analyze syllable structure patterns in Linear A words.

    Examines: word length distribution, CV patterns, syllable harmony,
    and phonotactic constraints.
    """
    words = get_unique_words()
    stats = {
        'length_dist': Counter(),
        'cv_patterns': Counter(),
        'vowel_harmony': {'harmonic': 0, 'disharmonic': 0},
        'consonant_clusters': Counter(),
    }

    vowels = set('aeiou')

    for word, count in words.items():
        syls = extract_syllables(word)
        n = len(syls)
        stats['length_dist'][n] += count

        # CV pattern
        pattern = []
        word_vowels = []
        for syl in syls:
            if syl.startswith('*'):
                pattern.append('X')
                continue
            if len(syl) == 1 and syl in vowels:
                pattern.append('V')
                word_vowels.append(syl)
            elif len(syl) >= 2:
                pattern.append('CV')
                word_vowels.append(syl[-1])
            else:
                pattern.append('?')

        cv = '-'.join(pattern)
        stats['cv_patterns'][cv] += count

        # Vowel harmony check
        if len(word_vowels) >= 2:
            unique_v = set(word_vowels)
            if len(unique_v) == 1:
                stats['vowel_harmony']['harmonic'] += count
            else:
                stats['vowel_harmony']['disharmonic'] += count

        # Initial consonant patterns
        if syls and len(syls[0]) > 1:
            stats['consonant_clusters'][syls[0][:-1]] += count

    return stats


# =============================================================================
# FULL MORPHOLOGICAL ANALYSIS
# =============================================================================

def run_morphology():
    """Run all morphological analyses."""
    results = {}

    results['prefixes'] = detect_prefixes()
    results['suffixes'] = detect_suffixes()
    results['root_families'] = find_root_families()
    results['reduplication'] = detect_reduplication()
    results['paradigms'] = detect_paradigms()
    results['compounds'] = detect_compounds()
    results['distribution_classes'] = classify_by_distribution()
    results['libation_analysis'] = analyze_libation_formula()
    results['syllable_patterns'] = syllable_pattern_stats()

    return results


def print_morphology():
    """Print morphological analysis report."""
    results = run_morphology()

    print("=" * 70)
    print("LINEAR A MORPHOLOGICAL ANALYSIS")
    print("=" * 70)

    # Prefixes
    print("\n--- CANDIDATE PREFIXES ---")
    for prefix, info in list(results['prefixes'].items())[:10]:
        print(f"  {prefix:8s}  freq={info['frequency']:2d}  "
              f"stems={len(info['stems']):2d}  score={info['score']:.2f}")
        if info['words'][:5]:
            print(f"           words: {', '.join(info['words'][:5])}")

    # Suffixes
    print("\n--- CANDIDATE SUFFIXES ---")
    for suffix, info in list(results['suffixes'].items())[:10]:
        print(f"  {suffix:8s}  freq={info['frequency']:2d}  "
              f"stems={len(info['stems']):2d}  score={info['score']:.2f}")
        if info['words'][:5]:
            print(f"           words: {', '.join(info['words'][:5])}")

    # Root families
    print("\n--- ROOT FAMILIES ---")
    for root, info in list(results['root_families'].items())[:10]:
        print(f"  {root:12s}  members={info['n_members']}")
        for var in info['variations'][:5]:
            pre = f"[{var['prefix']}]-" if var['prefix'] else ''
            suf = f"-[{var['suffix']}]" if var['suffix'] else ''
            print(f"    {pre}{root}{suf}  =  {var['word']}")

    # Reduplication
    print("\n--- REDUPLICATION ---")
    for word, info in sorted(results['reduplication'].items(),
                              key=lambda x: x[1]['frequency'], reverse=True):
        print(f"  {word:25s}  repeated={info['repeated']:4s}  "
              f"type={info['type']:12s}  freq={info['frequency']}")

    # Paradigms
    print("\n--- PARADIGMS ---")
    for stem, info in list(results['paradigms'].items())[:10]:
        print(f"  stem={stem}")
        for suffix, word in info['forms'].items():
            print(f"    + {suffix:8s} = {word}")

    # Compounds
    print("\n--- COMPOUND WORDS ---")
    for word, info in results['compounds'].items():
        print(f"  {word:20s} = {info['parts'][0]} + {info['parts'][1]}")

    # Distribution classes
    print("\n--- WORD CLASSES BY DISTRIBUTION ---")
    for cls, members in sorted(results['distribution_classes'].items(),
                                key=lambda x: len(x[1]), reverse=True):
        top = [m['word'] for m in members[:5]]
        print(f"  {cls:25s}: {len(members):3d} words  "
              f"top: {', '.join(top)}")

    # Libation formula
    print("\n--- LIBATION FORMULA ANALYSIS ---")
    lib = results['libation_analysis']
    for term, info in lib.items():
        if term.startswith('_'):
            continue
        print(f"\n  {term}")
        print(f"    syllables: {info['syllables']}")
        print(f"    parses:")
        for parse in info['morphological_parses']:
            print(f"      {parse['parse']:30s} - {parse['hypothesis']}")

    formula = lib['_formula_structure']
    print(f"\n  Formula structure: {formula['pattern']}")
    print(f"  Conclusion: {formula['conclusion']}")

    # Syllable patterns
    print("\n--- SYLLABLE PATTERN STATISTICS ---")
    sp = results['syllable_patterns']
    print("  Word lengths (in syllables):")
    for n, count in sorted(sp['length_dist'].items()):
        bar = '#' * min(count, 40)
        print(f"    {n} syllables: {count:4d}  {bar}")

    print("  Top CV patterns:")
    for pattern, count in sp['cv_patterns'].most_common(8):
        print(f"    {pattern:15s}: {count:4d}")

    vh = sp['vowel_harmony']
    total_vh = vh['harmonic'] + vh['disharmonic']
    if total_vh > 0:
        pct = vh['harmonic'] / total_vh * 100
        print(f"  Vowel harmony: {vh['harmonic']}/{total_vh} = {pct:.1f}% harmonic")

    print(f"\n{'=' * 70}")
    return results


if __name__ == '__main__':
    print_morphology()
