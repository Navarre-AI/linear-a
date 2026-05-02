"""
Linear A Sign Inventory
========================
Complete catalog of Linear A signs with their hypothesized phonetic values
derived from Linear B correspondences (Ventris grid), plus ideographic values.

Sources:
- GORILA (Godart & Olivier, Recueil des inscriptions en linéaire A)
- Younger, John G. "Linear A Texts in Phonetic Transcription"
- Palmer, Ruth. "Linear A commodities"
- Packard, David W. "Minoan Linear A"
- Davis, Brent. "Minoan Stone Vessels with Linear A Inscriptions"

Sign numbering follows the standard AB numbering system where:
- AB signs are shared between Linear A and Linear B
- A signs are unique to Linear A
"""

# =============================================================================
# SYLLABOGRAPHIC SIGNS (phonetic values via Linear B correspondences)
# =============================================================================
# Format: sign_number -> {
#   'linb_value': phonetic value from Linear B,
#   'confidence': high/medium/low/speculative,
#   'description': sign description,
#   'unicode': Unicode code point if available (Linear A block U+10600-U+1077F)
# }

SYLLABOGRAMS = {
    # ----- SERIES: VOWELS -----
    'AB08': {'linb_value': 'a', 'confidence': 'high', 'description': 'vowel a'},
    'AB38': {'linb_value': 'e', 'confidence': 'high', 'description': 'vowel e'},
    'AB28': {'linb_value': 'i', 'confidence': 'high', 'description': 'vowel i'},
    'AB61': {'linb_value': 'o', 'confidence': 'high', 'description': 'vowel o'},
    'AB10': {'linb_value': 'u', 'confidence': 'high', 'description': 'vowel u'},

    # ----- SERIES: D- -----
    'AB01': {'linb_value': 'da', 'confidence': 'high', 'description': 'syllable da'},
    'AB45': {'linb_value': 'de', 'confidence': 'high', 'description': 'syllable de'},
    'AB07': {'linb_value': 'di', 'confidence': 'high', 'description': 'syllable di'},
    'AB14': {'linb_value': 'do', 'confidence': 'high', 'description': 'syllable do'},
    'AB51': {'linb_value': 'du', 'confidence': 'high', 'description': 'syllable du'},

    # ----- SERIES: J- -----
    'AB57': {'linb_value': 'ja', 'confidence': 'high', 'description': 'syllable ja'},
    'AB46': {'linb_value': 'je', 'confidence': 'high', 'description': 'syllable je'},
    'AB36': {'linb_value': 'jo', 'confidence': 'high', 'description': 'syllable jo'},
    'AB65': {'linb_value': 'ju', 'confidence': 'medium', 'description': 'syllable ju'},

    # ----- SERIES: K- -----
    'AB77': {'linb_value': 'ka', 'confidence': 'high', 'description': 'syllable ka'},
    'AB44': {'linb_value': 'ke', 'confidence': 'high', 'description': 'syllable ke'},
    'AB67': {'linb_value': 'ki', 'confidence': 'high', 'description': 'syllable ki'},
    'AB70': {'linb_value': 'ko', 'confidence': 'high', 'description': 'syllable ko'},
    'AB81': {'linb_value': 'ku', 'confidence': 'high', 'description': 'syllable ku'},

    # ----- SERIES: M- -----
    'AB80': {'linb_value': 'ma', 'confidence': 'high', 'description': 'syllable ma'},
    'AB13': {'linb_value': 'me', 'confidence': 'high', 'description': 'syllable me'},
    'AB73': {'linb_value': 'mi', 'confidence': 'high', 'description': 'syllable mi'},
    'AB15': {'linb_value': 'mo', 'confidence': 'high', 'description': 'syllable mo'},
    'AB23': {'linb_value': 'mu', 'confidence': 'high', 'description': 'syllable mu'},

    # ----- SERIES: N- -----
    'AB06': {'linb_value': 'na', 'confidence': 'high', 'description': 'syllable na'},
    'AB24': {'linb_value': 'ne', 'confidence': 'high', 'description': 'syllable ne'},
    'AB30': {'linb_value': 'ni', 'confidence': 'high', 'description': 'syllable ni'},
    'AB52': {'linb_value': 'no', 'confidence': 'high', 'description': 'syllable no'},
    'AB55': {'linb_value': 'nu', 'confidence': 'high', 'description': 'syllable nu'},

    # ----- SERIES: P- -----
    'AB03': {'linb_value': 'pa', 'confidence': 'high', 'description': 'syllable pa'},
    'AB72': {'linb_value': 'pe', 'confidence': 'high', 'description': 'syllable pe'},
    'AB39': {'linb_value': 'pi', 'confidence': 'high', 'description': 'syllable pi'},
    'AB11': {'linb_value': 'po', 'confidence': 'high', 'description': 'syllable po'},
    'AB50': {'linb_value': 'pu', 'confidence': 'high', 'description': 'syllable pu'},
    'AB29': {'linb_value': 'pu2', 'confidence': 'medium', 'description': 'syllable pu2 variant'},

    # ----- SERIES: Q- -----
    'AB16': {'linb_value': 'qa', 'confidence': 'high', 'description': 'syllable qa (labiovelar)'},
    'AB78': {'linb_value': 'qe', 'confidence': 'high', 'description': 'syllable qe (labiovelar)'},
    'AB21': {'linb_value': 'qi', 'confidence': 'medium', 'description': 'syllable qi (labiovelar)'},

    # ----- SERIES: R- (covers both l and r) -----
    'AB60': {'linb_value': 'ra', 'confidence': 'high', 'description': 'syllable ra'},
    'AB27': {'linb_value': 're', 'confidence': 'high', 'description': 'syllable re'},
    'AB53': {'linb_value': 'ri', 'confidence': 'high', 'description': 'syllable ri'},
    'AB02': {'linb_value': 'ro', 'confidence': 'high', 'description': 'syllable ro'},
    'AB26': {'linb_value': 'ru', 'confidence': 'high', 'description': 'syllable ru'},
    'AB33': {'linb_value': 'ra3', 'confidence': 'medium', 'description': 'syllable rai/rya'},
    'AB68': {'linb_value': 'ro2', 'confidence': 'medium', 'description': 'syllable ro2 variant'},

    # ----- SERIES: S- -----
    'AB31': {'linb_value': 'sa', 'confidence': 'high', 'description': 'syllable sa'},
    'AB09': {'linb_value': 'se', 'confidence': 'high', 'description': 'syllable se'},
    'AB41': {'linb_value': 'si', 'confidence': 'high', 'description': 'syllable si'},
    'AB12': {'linb_value': 'so', 'confidence': 'high', 'description': 'syllable so'},
    'AB58': {'linb_value': 'su', 'confidence': 'high', 'description': 'syllable su'},

    # ----- SERIES: T- -----
    'AB59': {'linb_value': 'ta', 'confidence': 'high', 'description': 'syllable ta'},
    'AB04': {'linb_value': 'te', 'confidence': 'high', 'description': 'syllable te'},
    'AB37': {'linb_value': 'ti', 'confidence': 'high', 'description': 'syllable ti'},
    'AB05': {'linb_value': 'to', 'confidence': 'high', 'description': 'syllable to'},
    'AB69': {'linb_value': 'tu', 'confidence': 'high', 'description': 'syllable tu'},

    # ----- SERIES: W- -----
    'AB54': {'linb_value': 'wa', 'confidence': 'high', 'description': 'syllable wa'},
    'AB75': {'linb_value': 'we', 'confidence': 'high', 'description': 'syllable we'},
    'AB40': {'linb_value': 'wi', 'confidence': 'high', 'description': 'syllable wi'},
    'AB42': {'linb_value': 'wo', 'confidence': 'high', 'description': 'syllable wo'},

    # ----- SERIES: Z- -----
    'AB17': {'linb_value': 'za', 'confidence': 'high', 'description': 'syllable za'},
    'AB74': {'linb_value': 'ze', 'confidence': 'high', 'description': 'syllable ze'},
    'AB20': {'linb_value': 'zo', 'confidence': 'high', 'description': 'syllable zo'},

    # ----- COMPLEX / EXTRA SIGNS -----
    'AB25': {'linb_value': 'a2', 'confidence': 'medium', 'description': 'variant of a'},
    'AB43': {'linb_value': 'a3', 'confidence': 'medium', 'description': 'variant of a (ai?)'},
    'AB85': {'linb_value': 'au', 'confidence': 'medium', 'description': 'diphthong au'},
    'AB22': {'linb_value': 'pi2', 'confidence': 'low', 'description': 'variant of pi or lia?'},
    'AB32': {'linb_value': 'qo', 'confidence': 'medium', 'description': 'syllable qo'},
    'AB34': {'linb_value': 'unknown_34', 'confidence': 'low', 'description': 'no Linear B match'},
    'AB35': {'linb_value': 'unknown_35', 'confidence': 'low', 'description': 'no Linear B match'},
    'AB47': {'linb_value': 'unknown_47', 'confidence': 'low', 'description': 'no clear Linear B match'},
    'AB48': {'linb_value': 'unknown_48', 'confidence': 'low', 'description': 'no clear Linear B match'},
    'AB49': {'linb_value': 'unknown_49', 'confidence': 'low', 'description': 'no clear Linear B match'},
    'AB56': {'linb_value': 'pa3', 'confidence': 'medium', 'description': 'variant pa3 (pai?)'},
    'AB62': {'linb_value': 'pte', 'confidence': 'low', 'description': 'complex sign pte?'},
    'AB63': {'linb_value': 'unknown_63', 'confidence': 'low', 'description': 'no clear match'},
    'AB64': {'linb_value': 'unknown_64', 'confidence': 'low', 'description': 'no clear match'},
    'AB66': {'linb_value': 'ta2', 'confidence': 'medium', 'description': 'variant ta2'},
    'AB71': {'linb_value': 'dwe', 'confidence': 'medium', 'description': 'complex sign dwe'},
    'AB76': {'linb_value': 'ra2', 'confidence': 'medium', 'description': 'variant ra2 (rya?)'},
    'AB79': {'linb_value': 'zu', 'confidence': 'medium', 'description': 'syllable zu'},
    'AB82': {'linb_value': 'unknown_82', 'confidence': 'low', 'description': 'no clear match'},
    'AB83': {'linb_value': 'unknown_83', 'confidence': 'low', 'description': 'no clear match'},
    'AB84': {'linb_value': 'unknown_84', 'confidence': 'low', 'description': 'no clear match'},
    'AB86': {'linb_value': 'nwa', 'confidence': 'medium', 'description': 'complex sign nwa'},
    'AB87': {'linb_value': 'twe', 'confidence': 'medium', 'description': 'complex sign twe'},

    # ----- LINEAR A UNIQUE SIGNS (A-series, no Linear B parallel) -----
    'A301': {'linb_value': 'UNKNOWN_301', 'confidence': 'none', 'description': 'Linear A only - no parallel'},
    'A302': {'linb_value': 'UNKNOWN_302', 'confidence': 'none', 'description': 'Linear A only'},
    'A303': {'linb_value': 'UNKNOWN_303', 'confidence': 'none', 'description': 'Linear A only'},
    'A304': {'linb_value': 'UNKNOWN_304', 'confidence': 'none', 'description': 'Linear A only'},
    'A305': {'linb_value': 'UNKNOWN_305', 'confidence': 'none', 'description': 'Linear A only'},
    'A306': {'linb_value': 'UNKNOWN_306', 'confidence': 'none', 'description': 'Linear A only'},
    'A307': {'linb_value': 'UNKNOWN_307', 'confidence': 'none', 'description': 'Linear A only'},
    'A308': {'linb_value': 'UNKNOWN_308', 'confidence': 'none', 'description': 'Linear A only'},
    'A309': {'linb_value': 'UNKNOWN_309', 'confidence': 'none', 'description': 'Linear A only'},
    'A310': {'linb_value': 'UNKNOWN_310', 'confidence': 'none', 'description': 'Linear A only'},
}

# =============================================================================
# IDEOGRAMS / LOGOGRAMS (semantic signs for commodities, quantities, etc.)
# =============================================================================

IDEOGRAMS = {
    # Commodity ideograms (from Linear B parallels and Palmer's work)
    'AB100': {'value': 'VIR', 'meaning': 'man/person', 'confidence': 'high'},
    'AB102': {'value': 'MUL', 'meaning': 'woman', 'confidence': 'high'},
    'AB104': {'value': 'CERV', 'meaning': 'deer/stag', 'confidence': 'medium'},
    'AB105': {'value': 'SUS', 'meaning': 'pig', 'confidence': 'high'},
    'AB106': {'value': 'OVIS', 'meaning': 'sheep', 'confidence': 'high'},
    'AB107': {'value': 'CAP', 'meaning': 'goat', 'confidence': 'high'},
    'AB108': {'value': 'BOS', 'meaning': 'ox/cattle', 'confidence': 'high'},
    'AB109': {'value': 'SUS+SI', 'meaning': 'pig variant', 'confidence': 'medium'},

    'AB120': {'value': 'GRA', 'meaning': 'grain/wheat', 'confidence': 'high'},
    'AB121': {'value': 'HORD', 'meaning': 'barley', 'confidence': 'medium'},
    'AB122': {'value': 'OLIV', 'meaning': 'olives', 'confidence': 'high'},
    'AB123': {'value': 'AROM', 'meaning': 'aromatic/spice', 'confidence': 'medium'},
    'AB125': {'value': 'CYP', 'meaning': 'cyperus/spice', 'confidence': 'medium'},
    'AB130': {'value': 'OLE', 'meaning': 'oil/olive oil', 'confidence': 'high'},
    'AB131': {'value': 'VIN', 'meaning': 'wine', 'confidence': 'high'},
    'AB132': {'value': 'unknown_liquid', 'meaning': 'some liquid', 'confidence': 'low'},

    'AB140': {'value': 'AES', 'meaning': 'bronze/copper', 'confidence': 'high'},
    'AB141': {'value': 'AUR', 'meaning': 'gold', 'confidence': 'medium'},
    'AB142': {'value': 'unknown_metal', 'meaning': 'some metal/material', 'confidence': 'low'},

    'AB150': {'value': 'TELA', 'meaning': 'cloth/textile', 'confidence': 'high'},
    'AB151': {'value': 'TELA+TE', 'meaning': 'cloth variant', 'confidence': 'medium'},
    'AB152': {'value': 'unknown_textile', 'meaning': 'textile product', 'confidence': 'low'},

    'AB160': {'value': 'FIC', 'meaning': 'figs', 'confidence': 'high'},
    'AB161': {'value': 'unknown_food', 'meaning': 'some food product', 'confidence': 'low'},

    # Vessel ideograms
    'AB200': {'value': 'VAS', 'meaning': 'vessel (generic)', 'confidence': 'medium'},
    'AB201': {'value': 'VAS_TRIPOD', 'meaning': 'tripod vessel', 'confidence': 'medium'},
    'AB202': {'value': 'VAS_HANDLED', 'meaning': 'handled vessel', 'confidence': 'medium'},
    'AB203': {'value': 'VAS_SMALL', 'meaning': 'small vessel/cup', 'confidence': 'medium'},

    # Transaction ideograms unique to Linear A
    'A501': {'value': 'TRANSACTION_1', 'meaning': 'transaction marker 1', 'confidence': 'low'},
    'A502': {'value': 'TRANSACTION_2', 'meaning': 'transaction marker 2', 'confidence': 'low'},
}

# =============================================================================
# NUMERIC SYSTEM
# =============================================================================

NUMERALS = {
    'UNIT': {'value': 1, 'description': 'single stroke/dot = 1'},
    'TEN': {'value': 10, 'description': 'horizontal bar = 10'},
    'HUNDRED': {'value': 100, 'description': 'circle = 100'},
    'THOUSAND': {'value': 1000, 'description': 'circle with rays = 1000'},
    'FRACTION_J': {'value': '1/2', 'description': 'fraction J = 1/2'},
    'FRACTION_E': {'value': '1/4', 'description': 'fraction E = 1/4'},
    'FRACTION_F': {'value': '1/8', 'description': 'fraction F = 1/8'},
    'FRACTION_K': {'value': '1/16', 'description': 'fraction K = 1/16'},
    'FRACTION_L': {'value': '3/4', 'description': 'fraction L = 3/4'},
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_phonetic_value(sign_id):
    """Return the hypothesized phonetic value for a sign."""
    if sign_id in SYLLABOGRAMS:
        return SYLLABOGRAMS[sign_id]['linb_value']
    if sign_id in IDEOGRAMS:
        return IDEOGRAMS[sign_id]['value']
    return f'[{sign_id}]'

def get_high_confidence_signs():
    """Return only signs with high-confidence phonetic values."""
    return {k: v for k, v in SYLLABOGRAMS.items() if v['confidence'] == 'high'}

def get_sign_by_value(phonetic_value):
    """Reverse lookup: find sign(s) by phonetic value."""
    results = []
    for sign_id, data in SYLLABOGRAMS.items():
        if data['linb_value'] == phonetic_value:
            results.append(sign_id)
    return results

def get_all_cv_patterns():
    """Return all consonant-vowel patterns in the syllabary."""
    consonants = set()
    vowels = {'a', 'e', 'i', 'o', 'u'}
    patterns = {}
    for sign_id, data in SYLLABOGRAMS.items():
        val = data['linb_value']
        if data['confidence'] in ('high', 'medium') and len(val) == 2 and val[1] in vowels:
            c = val[0]
            v = val[1]
            consonants.add(c)
            if c not in patterns:
                patterns[c] = {}
            patterns[c][v] = sign_id
    return patterns

if __name__ == '__main__':
    print(f"Total syllabograms: {len(SYLLABOGRAMS)}")
    print(f"High confidence: {len(get_high_confidence_signs())}")
    print(f"Total ideograms: {len(IDEOGRAMS)}")
    print("\nCV Grid:")
    patterns = get_all_cv_patterns()
    vowels = ['a', 'e', 'i', 'o', 'u']
    print(f"{'':>4}", end='')
    for v in vowels:
        print(f"{v:>6}", end='')
    print()
    for c in sorted(patterns.keys()):
        print(f"{c:>4}", end='')
        for v in vowels:
            sign = patterns[c].get(v, '-')
            print(f"{sign:>6}", end='')
        print()
