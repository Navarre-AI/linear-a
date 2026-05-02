"""
Linear A Corpus
================
Complete corpus of Linear A inscriptions organized by findsite.
Data sourced from GORILA (Godart & Olivier), Younger's transcriptions,
and published scholarship.

Each inscription is a dict with:
  - site: findspot
  - type: tablet/roundel/libation_table/stone_vessel/pithos/nodule/etc
  - period: MM II, MM III, LM IA, LM IB, etc
  - lines: list of line transcriptions (phonetic, using Linear B values)
  - signs: raw sign sequences (AB numbers)
  - ideograms: commodity ideograms present
  - numbers: numeric values recorded
  - condition: complete/fragmentary/damaged
  - notes: scholarly commentary
"""

CORPUS = {}

def _merge(module_corpus):
    """Merge a sub-corpus into the main CORPUS."""
    CORPUS.update(module_corpus)

# Import sub-corpora as they're built
try:
    from .libation_formulas import LIBATION_CORPUS
    _merge(LIBATION_CORPUS)
except ImportError:
    pass

try:
    from .haghia_triada import HT_CORPUS
    _merge(HT_CORPUS)
except ImportError:
    pass

try:
    from .haghia_triada_2 import HT_CORPUS_2
    _merge(HT_CORPUS_2)
except ImportError:
    pass

try:
    from .zakros import ZA_CORPUS
    _merge(ZA_CORPUS)
except ImportError:
    pass

try:
    from .khania import KH_CORPUS
    _merge(KH_CORPUS)
except ImportError:
    pass

try:
    from .phaistos import PH_CORPUS
    _merge(PH_CORPUS)
except ImportError:
    pass

try:
    from .other_sites import OTHER_CORPUS
    _merge(OTHER_CORPUS)
except ImportError:
    pass

try:
    from .recent_discoveries import RECENT_CORPUS
    _merge(RECENT_CORPUS)
except ImportError:
    pass


# === HELPER FUNCTIONS ===

def get_all():
    """Return the complete corpus."""
    return CORPUS

def get_by_site(site_prefix):
    """Get all inscriptions from a site (e.g., 'HT', 'ZA', 'KH')."""
    return {k: v for k, v in CORPUS.items() if k.startswith(site_prefix)}

def get_by_type(doc_type):
    """Get all inscriptions of a type (e.g., 'tablet', 'libation_table')."""
    return {k: v for k, v in CORPUS.items() if v.get('type') == doc_type}

def get_libation_formulas():
    """Get all inscriptions containing the libation formula."""
    return {k: v for k, v in CORPUS.items()
            if v.get('type') in ('libation_table', 'stone_vessel')
            or 'libation' in v.get('notes', '').lower()}

def get_words():
    """Extract all unique words (sign sequences between dividers) from the corpus."""
    words = []
    for entry in CORPUS.values():
        for line in entry.get('lines', []):
            parts = line.replace('|', '.').replace('  ', '.').split('.')
            for part in parts:
                w = part.strip()
                if w and not w.startswith(('GRA', 'OLE', 'VIN', 'FIC', 'OVIS',
                    'CAP', 'SUS', 'BOS', 'TELA', 'AES', 'HORD', 'OLIV',
                    'AROM', 'CYP', 'VIR', 'MUL', '[', ']')):
                    try:
                        float(w)
                    except ValueError:
                        if len(w) > 1:
                            words.append(w)
    return words

def get_unique_words():
    """Get sorted unique words with frequency counts."""
    from collections import Counter
    return Counter(get_words())

def search_sequence(seq):
    """Find all inscriptions containing a sign sequence."""
    results = {}
    seq_lower = seq.lower()
    for k, v in CORPUS.items():
        for line in v.get('lines', []):
            if seq_lower in line.lower():
                results[k] = v
                break
    return results

def corpus_stats():
    """Return basic corpus statistics."""
    total_lines = sum(len(v.get('lines', [])) for v in CORPUS.values())
    total_words = len(get_words())
    unique = len(get_unique_words())
    sites = set()
    for k in CORPUS:
        prefix = k.split(' ')[0] if ' ' in k else k[:2]
        sites.add(prefix)
    return {
        'total_inscriptions': len(CORPUS),
        'total_lines': total_lines,
        'total_words': total_words,
        'unique_words': unique,
        'sites': sorted(sites),
    }


if __name__ == '__main__':
    stats = corpus_stats()
    print(f"Linear A Corpus")
    print(f"{'='*40}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"\nTop 20 most frequent words:")
    for word, count in get_unique_words().most_common(20):
        print(f"  {word}: {count}")
