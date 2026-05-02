"""
FileMaker Data Ingestion
=========================
Parse the FileMaker CSV exports and integrate them into the corpus system.

The FM data provides:
- fm_doc.csv: 773 document faces with sign counts (vs our 127 inscriptions)
- fm_role_count.csv: 731 documents x 62 sign role binary matrix
- fm_decode.csv: 5,714 image references
- fm_summary.csv: Site-level totals

This module creates a unified document registry that merges our
hand-transcribed corpus (with actual text) with the FM metadata
(which has sign counts and role data but no transcribed text).
"""

import csv
import io
import sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

DATA_DIR = Path(__file__).parent


def load_fm_doc():
    """Load fm_doc.csv - complete document registry.

    Returns dict of {doc_face: {group, face, site, number, sub, signs}}
    """
    path = DATA_DIR / 'fm_doc.csv'
    if not path.exists():
        return {}

    with open(path, 'r') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

    docs = {}
    for row in rows:
        if len(row) >= 6:
            doc_group = row[0]
            doc_face = row[1]
            site = row[2]
            number = row[3]
            sub = row[4]
            sign_count = int(row[5])

            # Determine document type
            doc_type = 'tablet'
            for prefix, dtype in [('Wa', 'sealing'), ('Wb', 'nodule'),
                                   ('Wc', 'roundel'), ('Za', 'stone_libation'),
                                   ('Zb', 'stone_vessel'), ('Zc', 'stone'),
                                   ('Zd', 'inked'), ('Ze', 'stone'),
                                   ('Zf', 'metal'), ('Zg', 'other')]:
                if prefix in number:
                    doc_type = dtype
                    break

            docs[doc_face] = {
                'group': doc_group,
                'face': doc_face,
                'site': site,
                'number': number,
                'sub': sub,
                'sign_count': sign_count,
                'type': doc_type,
            }

    return docs


def load_fm_role_count():
    """Load fm_role_count.csv - sign role binary matrix.

    Returns dict of {doc_group: [62 binary values]}
    The 62 columns represent sign role categories.
    """
    path = DATA_DIR / 'fm_role_count.csv'
    if not path.exists():
        return {}

    with open(path, 'r') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

    roles = {}
    for row in rows:
        if len(row) >= 2:
            doc_id = row[0]
            values = []
            for v in row[1:]:
                try:
                    values.append(int(v))
                except ValueError:
                    values.append(0)
            roles[doc_id] = values

    return roles


def load_fm_images():
    """Load fm_decode.csv - image catalog.

    Returns dict of {doc_group: [{filename, face, site, detail, type}]}
    """
    path = DATA_DIR / 'fm_decode.csv'
    if not path.exists():
        return {}

    with open(path, 'r') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

    images = defaultdict(list)
    for row in rows:
        if len(row) >= 9:
            doc_group = row[0]
            filename = row[1]
            doc_face = row[2]
            site = row[3]
            detail_num = row[7]
            img_type = row[8]

            images[doc_group].append({
                'filename': filename,
                'face': doc_face,
                'site': site,
                'detail': detail_num,
                'type': img_type,
            })

    return dict(images)


def load_fm_summary():
    """Load fm_summary.csv - site totals.

    Returns dict of {site: {docs, signs}}
    """
    path = DATA_DIR / 'fm_summary.csv'
    if not path.exists():
        return {}

    with open(path, 'r') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)

    summary = {}
    for row in rows:
        if len(row) >= 3:
            site = row[0]
            docs = int(row[1])
            signs = int(row[2])
            summary[site] = {'docs': docs, 'signs': signs}

    return summary


def get_fm_stats():
    """Get comprehensive statistics from FileMaker data."""
    docs = load_fm_doc()
    roles = load_fm_role_count()
    images = load_fm_images()
    summary = load_fm_summary()

    # Site breakdown
    sites = defaultdict(lambda: {'faces': 0, 'signs': 0, 'types': Counter()})
    for face_id, doc in docs.items():
        site = doc['site']
        sites[site]['faces'] += 1
        sites[site]['signs'] += doc['sign_count']
        sites[site]['types'][doc['type']] += 1

    # Document complexity from role matrix
    complexity = {}
    for doc_id, values in roles.items():
        n_roles = sum(values)
        complexity[doc_id] = n_roles

    # Image coverage
    n_images = sum(len(imgs) for imgs in images.values())
    n_overviews = sum(1 for imgs in images.values()
                      for img in imgs if img['type'] == 'Overview')

    return {
        'total_faces': len(docs),
        'total_signs': sum(d['sign_count'] for d in docs.values()),
        'total_sites': len(sites),
        'sites': dict(sites),
        'role_matrix_docs': len(roles),
        'role_columns': len(next(iter(roles.values()))) if roles else 0,
        'complexity': complexity,
        'total_images': n_images,
        'overview_images': n_overviews,
        'detail_images': n_images - n_overviews,
    }


def merge_with_corpus():
    """Merge FileMaker metadata with our hand-transcribed corpus.

    Returns a unified registry showing:
    - Which documents we have transcriptions for
    - Which documents only have metadata
    - Coverage statistics
    """
    from linear_a.data.corpus import get_all

    fm_docs = load_fm_doc()
    corpus = get_all()

    merged = {}

    # Add all FM docs
    for face_id, doc in fm_docs.items():
        group = doc['group']
        merged[group] = {
            'fm_data': doc,
            'has_transcription': False,
            'transcription': None,
            'sign_count': doc['sign_count'],
            'site': doc['site'],
            'type': doc['type'],
        }

    # Match corpus entries to FM docs
    matched = 0
    unmatched_corpus = []
    for corpus_id, corpus_doc in corpus.items():
        # Try to find matching FM doc
        found = False
        for fm_key, fm_doc in fm_docs.items():
            if fm_doc['group'] == corpus_id or fm_doc['face'] == corpus_id:
                if fm_doc['group'] in merged:
                    merged[fm_doc['group']]['has_transcription'] = True
                    merged[fm_doc['group']]['transcription'] = corpus_doc
                    matched += 1
                    found = True
                    break

        if not found:
            # Corpus entry with no FM match - keep it
            site = corpus_doc.get('site', corpus_id.split(' ')[0] if ' ' in corpus_id else corpus_id[:2])
            merged[corpus_id] = {
                'fm_data': None,
                'has_transcription': True,
                'transcription': corpus_doc,
                'sign_count': len(corpus_doc.get('lines', [])),
                'site': site,
                'type': corpus_doc.get('type', 'unknown'),
            }
            unmatched_corpus.append(corpus_id)

    transcribed = sum(1 for v in merged.values() if v['has_transcription'])
    metadata_only = sum(1 for v in merged.values() if not v['has_transcription'])

    return {
        'merged': merged,
        'total': len(merged),
        'transcribed': transcribed,
        'metadata_only': metadata_only,
        'matched': matched,
        'unmatched_corpus': unmatched_corpus,
        'coverage': transcribed / len(merged) if merged else 0,
    }


def print_fm_stats():
    """Print FileMaker data analysis."""
    stats = get_fm_stats()
    merge = merge_with_corpus()

    print("=" * 60)
    print("FILEMAKER DATA ANALYSIS")
    print("=" * 60)

    print(f"\nDocument Registry:")
    print(f"  Total faces: {stats['total_faces']}")
    print(f"  Total signs: {stats['total_signs']}")
    print(f"  Sites: {stats['total_sites']}")

    print(f"\nSign Role Matrix:")
    print(f"  Documents: {stats['role_matrix_docs']}")
    print(f"  Role categories: {stats['role_columns']}")

    print(f"\nImage Catalog:")
    print(f"  Total images: {stats['total_images']}")
    print(f"  Overview photos: {stats['overview_images']}")
    print(f"  Detail photos: {stats['detail_images']}")

    print(f"\nSite Breakdown:")
    print(f"  {'Site':6s} {'Faces':>6s} {'Signs':>7s} {'Types':30s}")
    print(f"  {'-'*55}")
    for site in sorted(stats['sites'].keys()):
        s = stats['sites'][site]
        types = ', '.join(f"{t}:{c}" for t, c in s['types'].most_common(3))
        print(f"  {site:6s} {s['faces']:6d} {s['signs']:7d} {types}")

    print(f"\nCorpus Merge:")
    print(f"  Total unified documents: {merge['total']}")
    print(f"  With transcriptions: {merge['transcribed']} ({merge['coverage']:.1%})")
    print(f"  Metadata only: {merge['metadata_only']}")
    print(f"  Matched FM<->corpus: {merge['matched']}")
    if merge['unmatched_corpus']:
        print(f"  Unmatched corpus entries: {len(merge['unmatched_corpus'])}")
        print(f"    {', '.join(merge['unmatched_corpus'][:10])}")

    # Most complex documents
    print(f"\nMost Complex Documents (by sign role diversity):")
    top = sorted(stats['complexity'].items(), key=lambda x: x[1], reverse=True)[:10]
    for doc_id, n_roles in top:
        has_text = "TRANSCRIBED" if any(
            v['has_transcription'] for k, v in merge['merged'].items()
            if k == doc_id or (v.get('fm_data') and v['fm_data'].get('group') == doc_id)
        ) else "metadata only"
        print(f"  {doc_id:15s} roles={n_roles:3d}  [{has_text}]")

    print(f"\n{'='*60}")
    return stats, merge


if __name__ == '__main__':
    print_fm_stats()
