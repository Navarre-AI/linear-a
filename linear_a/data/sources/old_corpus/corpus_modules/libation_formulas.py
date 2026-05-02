"""
Linear A Libation Formula Inscriptions
========================================
Found on stone vessels at peak sanctuaries and caves across Crete.
Recurring religious formula that appears at multiple sites.

The standard formula pattern:
  a-ta-i-*301-wa-ja + [recipient/deity] + ja-sa-sa-ra-me + [other terms]

Sources: GORILA, Younger, Davis (2014)
"""

LIBATION_CORPUS = {

    # IOUKHTAS PEAK SANCTUARY (IO)
    'IO Za 1': {
        'site': 'Ioukhtas', 'type': 'libation_table', 'period': 'MM III - LM IA',
        'lines': ['a-ta-i-*301-wa-ja'],
        'condition': 'fragmentary',
        'notes': 'Standard formula opening. Peak sanctuary on Mount Ioukhtas.',
    },
    'IO Za 2': {
        'site': 'Ioukhtas', 'type': 'libation_table', 'period': 'MM III - LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Standard formula with ja-sa-sa-ra-me.',
    },
    'IO Za 3': {
        'site': 'Ioukhtas', 'type': 'libation_table', 'period': 'MM III - LM IA',
        'lines': ['a-ta-i-*301-wa-ja . i-da-ma-te'],
        'condition': 'complete',
        'notes': 'Formula with i-da-ma-te. Possibly "Mother Ida".',
    },
    'IO Za 4': {
        'site': 'Ioukhtas', 'type': 'stone_vessel', 'period': 'MM III - LM IA',
        'lines': ['ja-sa-sa-ra-me . i-da-ma-te'],
        'condition': 'fragmentary',
        'notes': 'Both key terms together without opening formula.',
    },
    'IO Za 5': {
        'site': 'Ioukhtas', 'type': 'libation_table', 'period': 'MM III - LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me . i-da-ma-te'],
        'condition': 'complete',
        'notes': 'COMPLETE three-part formula. Fullest attestation.',
    },
    'IO Za 6': {
        'site': 'Ioukhtas', 'type': 'stone_vessel', 'period': 'MM III - LM IA',
        'lines': ['ta-na-te'],
        'condition': 'fragmentary',
        'notes': 'ta-na-te in ritual context. Possibly a deity name.',
    },

    # APODOULOU (AP)
    'AP Za 1': {
        'site': 'Apodoulou', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-di-ki-te-te . a-di-ki-te'],
        'condition': 'complete',
        'notes': 'a-di-ki-te = likely Dikte/Dikta (Mount Dikte).',
    },
    'AP Za 2': {
        'site': 'Apodoulou', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . pi-te-za'],
        'condition': 'complete',
        'notes': 'Formula with pi-te-za. Appears at multiple sites.',
    },

    # KOPHINAS PEAK SANCTUARY (KO)
    'KO Za 1': {
        'site': 'Kophinas', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me . u-na-ka-na-si . i-pi-na-ma . si-ru-te'],
        'condition': 'complete',
        'notes': 'LONGEST libation formula. 5 terms. u-na-ka-na-si and i-pi-na-ma unique here.',
    },

    # PSYCHRO CAVE (PS)
    'PS Za 1': {
        'site': 'Psychro', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . a-di-ki-te'],
        'condition': 'complete',
        'notes': 'Formula with Dikte. Found IN the Diktaean Cave.',
    },
    'PS Za 2': {
        'site': 'Psychro', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'ja-sa-sa-ra-me alone. Can stand independently.',
    },

    # PALAIKASTRO (PK)
    'PK Za 11': {
        'site': 'Palaikastro', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Standard formula. Eastern Crete.',
    },
    'PK Za 12': {
        'site': 'Palaikastro', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me . i-da-ma-te'],
        'condition': 'complete',
        'notes': 'Full three-part formula. Standardized across the island.',
    },

    # SYME VIANNOU (SY)
    'SY Za 1': {
        'site': 'Syme Viannou', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Standard formula at Syme.',
    },
    'SY Za 2': {
        'site': 'Syme Viannou', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . pi-te-za'],
        'condition': 'complete',
        'notes': 'Formula with pi-te-za. Same variant as AP Za 2.',
    },
    'SY Za 3': {
        'site': 'Syme Viannou', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['ta-na-te'],
        'condition': 'complete',
        'notes': 'ta-na-te alone. Same as IO Za 6.',
    },
    'SY Za 4': {
        'site': 'Syme Viannou', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['a-su-pu-wa . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'a-su-pu-wa replaces standard a-ta-i-*301-wa-ja opening.',
    },

    # KATO ZAKROS (ZA)
    'ZA Zb 3': {
        'site': 'Zakros', 'type': 'stone_vessel', 'period': 'LM IB',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me . i-da-ma-te . si-ru-te'],
        'condition': 'complete',
        'notes': 'Four-term formula. si-ru-te also at Kophinas.',
    },

    # PRASSA (PR)
    'PR Za 1': {
        'site': 'Prassa', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . pi-te-za . wa-ja'],
        'condition': 'complete',
        'notes': 'Formula with pi-te-za and additional wa-ja.',
    },

    # TROULLOS (TR)
    'TR Za 1': {
        'site': 'Troullos', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Standard two-part formula.',
    },
    'TR Za 2': {
        'site': 'Troullos', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['ja-sa-sa-ra-me'],
        'condition': 'fragmentary',
        'notes': 'ja-sa-sa-ra-me alone.',
    },

    # KNOSSOS (KN)
    'KN Za 10': {
        'site': 'Knossos', 'type': 'libation_table', 'period': 'MM III',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me . i-da-ma-te'],
        'condition': 'complete',
        'notes': 'Full formula at Knossos, the largest palace.',
    },

    # TYLISSOS (TL)
    'TL Za 1': {
        'site': 'Tylissos', 'type': 'libation_table', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Standard formula. Near Knossos.',
    },

    # VRYSINAS (VRY)
    'VRY Za 1': {
        'site': 'Vrysinas', 'type': 'libation_table', 'period': 'MM III',
        'lines': ['a-ta-i-*301-wa-ja'],
        'condition': 'fragmentary',
        'notes': 'Opening formula only. Western Crete peak sanctuary.',
    },

    # PETSOPHAS (PTS)
    'PTS Za 1': {
        'site': 'Petsophas', 'type': 'libation_table', 'period': 'MM III - LM IA',
        'lines': ['a-ta-i-*301-wa-ja . ja-sa-sa-ra-me'],
        'condition': 'fragmentary',
        'notes': 'Standard formula at eastern peak sanctuary.',
    },

    # ARCHANES (AR)
    'AR Zf 1': {
        'site': 'Archanes', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['i-da-ma-te'],
        'condition': 'complete',
        'notes': 'i-da-ma-te alone. Archanes on slopes of Ioukhtas.',
    },
    'AR Zf 2': {
        'site': 'Archanes', 'type': 'stone_vessel', 'period': 'LM IA',
        'lines': ['a-ta-i-*301-wa-ja'],
        'condition': 'fragmentary',
        'notes': 'Opening formula only.',
    },

    # PLATANOS (PL)
    'PL Zf 1': {
        'site': 'Platanos', 'type': 'stone_vessel', 'period': 'MM II',
        'lines': ['a-sa-sa-ra-me'],
        'condition': 'complete',
        'notes': 'Variant WITHOUT ja- prefix. Earliest attestation. '
                 'Critical for understanding ja- as prefix vs. integral.',
    },

    # MALIA (MA)
    'MA Za 1': {
        'site': 'Malia', 'type': 'libation_table', 'period': 'MM III',
        'lines': ['a-ta-i-*301-wa-ja . da-si-na'],
        'condition': 'complete',
        'notes': 'Unique da-si-na term instead of ja-sa-sa-ra-me.',
    },
}


# === FORMULA ANALYSIS HELPERS ===

def get_formula_terms():
    """Extract all terms that appear in libation formulas."""
    from collections import Counter
    terms = Counter()
    for entry in LIBATION_CORPUS.values():
        for line in entry['lines']:
            for term in line.split(' . '):
                terms[term.strip()] += 1
    return terms

def get_formula_patterns():
    """Show which combination patterns appear and how often."""
    from collections import Counter
    patterns = Counter()
    for entry in LIBATION_CORPUS.values():
        for line in entry['lines']:
            pattern = ' + '.join(line.split(' . '))
            patterns[pattern] += 1
    return patterns

def get_sites_with_formula():
    """List all sites where the libation formula appears."""
    sites = set()
    for entry in LIBATION_CORPUS.values():
        sites.add(entry['site'])
    return sorted(sites)


if __name__ == '__main__':
    print(f"Libation Formula Corpus")
    print(f"{'='*50}")
    print(f"Total inscriptions: {len(LIBATION_CORPUS)}")
    print(f"Sites: {', '.join(get_sites_with_formula())}")
    print(f"\nFormula terms (frequency):")
    for term, count in get_formula_terms().most_common():
        print(f"  {term}: {count}")
    print(f"\nFormula patterns:")
    for pattern, count in get_formula_patterns().most_common():
        print(f"  [{count}x] {pattern}")
