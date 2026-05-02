#!/usr/bin/env python3
"""Per-paper TF-IDF keyword extraction.

For each corpus paper, compute top 20 distinctive terms (unigrams +
bigrams) using TF-IDF against the corpus as the reference collection.
Additionally compute paper-to-paper cosine similarity to surface the
most thematically related papers.

Output: private/_extracted/_KEYWORDS.json, _PAPER_SIMILARITY.json
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent))
from _paths import REFS_ROOT
EXT = REFS_ROOT / "private" / "_extracted"

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿА-я][A-Za-zÀ-ÿА-я\-]{2,}")

STOPWORDS = set("""
a an and or but the of to in on at by for with from this that these those these
is are was were be been being have has had do does did not no nor so if then
than as at into onto up down out over under also such which who whom whose
their them they there here where when why how what our your his her its we us
i you me my your our would could should may might will shall can must any
some each every all most more less much many few several same other another
very just only also even about after before during between among across
against within without toward towards through throughout upon despite however
therefore moreover furthermore although though while whereas since because
thus hence ibid loc cit op seq pp vol fig figs no nos ch chs ed eds vol vols
new york cambridge oxford london paris press university see note fig figures
first second third fourth last well mostly often usually sometimes
probably likely rather quite somewhat certain certainly perhaps perhaps
following followed therein hereby thereby whereby whereby anyone everything
something someone anything nothing himself herself myself yourself ourselves
themselves itself whose whom ones one two three four five six seven eight nine ten
doi isbn issn pmid pmcid org https http www com edu gov net html pdf jpg png
""".split())


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in TOKEN_RE.findall(text)
            if w.lower() not in STOPWORDS and len(w) >= 3]


def main():
    manifests = sorted(EXT.glob("*/manifest.json"))
    doc_tokens = {}   # uuid -> Counter
    for mf in manifests:
        m = json.loads(mf.read_text())
        text_path = mf.parent / "text.md"
        if not text_path.exists():
            continue
        try:
            txt = text_path.read_text(errors="ignore")
        except Exception:
            continue
        toks = tokenize(txt)
        if not toks:
            continue
        # unigrams + bigrams
        c = Counter(toks)
        for i in range(len(toks) - 1):
            bg = toks[i] + " " + toks[i + 1]
            c[bg] += 1
        doc_tokens[m["uuid"]] = c

    n_docs = len(doc_tokens)
    if not n_docs:
        print("no docs")
        return

    df = Counter()
    for c in doc_tokens.values():
        for term in c:
            df[term] += 1

    # Drop terms appearing in only 1 doc (noise) or >60% of docs (generic)
    max_df = int(n_docs * 0.6)
    valid_terms = {t for t, d in df.items() if 2 <= d <= max_df}

    # tf-idf
    keywords = {}
    tfidf_vectors = {}
    for uid, c in doc_tokens.items():
        total = sum(c.values())
        scores = []
        vec = {}
        for term, cnt in c.items():
            if term not in valid_terms:
                continue
            tf = cnt / total
            idf = math.log(n_docs / df[term])
            s = tf * idf
            scores.append((term, s, cnt))
            vec[term] = s
        scores.sort(key=lambda x: -x[1])
        keywords[uid] = [{"term": t, "score": round(s, 5), "count": cnt} for t, s, cnt in scores[:20]]
        tfidf_vectors[uid] = vec

    # Filename lookup
    fn_lookup = {}
    for mf in manifests:
        m = json.loads(mf.read_text())
        fn_lookup[m["uuid"]] = Path(m["source_path"]).name

    # Paper similarity — cosine on top-50 tfidf terms each
    top_vecs = {}
    for uid, vec in tfidf_vectors.items():
        top = dict(sorted(vec.items(), key=lambda x: -x[1])[:50])
        norm = math.sqrt(sum(v * v for v in top.values())) or 1
        top_vecs[uid] = (top, norm)

    similarity = {}
    uids = list(top_vecs.keys())
    for i, a in enumerate(uids):
        va, na = top_vecs[a]
        sims = []
        for b in uids:
            if a == b:
                continue
            vb, nb = top_vecs[b]
            dot = sum(va[k] * vb[k] for k in va if k in vb)
            if dot == 0:
                continue
            sims.append((b, dot / (na * nb)))
        sims.sort(key=lambda x: -x[1])
        similarity[a] = [
            {"uuid": b, "filename": fn_lookup.get(b, ""), "cosine": round(s, 4)}
            for b, s in sims[:10]
        ]

    out = {
        "stats": {
            "docs": n_docs,
            "vocab": len(df),
            "valid_terms": len(valid_terms),
        },
        "filenames": fn_lookup,
        "by_doc": keywords,
    }
    (EXT / "_KEYWORDS.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")

    sim_out = {
        "stats": {"docs": n_docs, "neighbours_per_doc": 10},
        "by_doc": similarity,
    }
    (EXT / "_PAPER_SIMILARITY.json").write_text(json.dumps(sim_out, indent=2, ensure_ascii=False) + "\n")

    print(f"docs: {n_docs}  vocab: {len(df):,}  valid: {len(valid_terms):,}")
    # Sample: Petrakis-Salgarella 2026
    sample = next((u for u, fn in fn_lookup.items() if "Petrakis" in fn and "Salgarella" in fn), None)
    if sample:
        print(f"\n{fn_lookup[sample]} top keywords:")
        for kw in keywords[sample][:15]:
            print(f"  {kw['score']:.4f}  {kw['term']:30s} (x{kw['count']})")
        print(f"\n  Most similar papers:")
        for s in similarity[sample][:5]:
            print(f"  {s['cosine']:.3f}  {s['filename']}")


if __name__ == "__main__":
    main()
