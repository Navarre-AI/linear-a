#!/usr/bin/env python3
"""Cross-layer check: the glyph string against the word list, record by record.

Population: every record of linear_a/data/corpus.json with a nonempty
`unicode_text` (the glyph layer) and a nonempty `words` list (the word layer).

Glyph layer. Each character of `unicode_text` in the Linear A block is read by
its Unicode 16.0 character name (Python unicodedata), which gives the sign
number, for example U+1062D "LINEAR A SIGN AB053" gives 53. The glyph counts as
mapped only when signs.json holds an entry of that sign number whose `unicode`
field is that same character. That is the name check: the codepoint, the
Unicode name and the signs.json entry must agree. Aegean numbers, the word
separator, line breaks, spaces and other punctuation are dropped, because the
word layer never carries them. U+1076B to U+1076F are damage placeholders.

Word layer. Each word is split on "-" (and "+" for a ligature). A token is a
syllable value (looked up in signs.json `phonetic`), a sign number (*301,
A301, AB120/GRA), "[?]" or "[unclassified]" (a sign SigLA does not identify),
or a value with a trailing "?" (a sign SigLA marks unsure).

The two sequences are compared by sign number after an alignment
(difflib.SequenceMatcher). Every record whose sequences are not identical is a
disagreement, and every difference is put in one class:

  a  damage placeholder, erasure, or a sign not identified in one layer
  b  a sign marked unsure in the word layer, present there only or read
     differently there
  c  logogram, fraction, numeral, ligature or separator handled differently.
     A glyph-only sign counts here when the record's own sign array gives it a
     non-syllabic role, or when it stands alone between numerals, separators
     or line breaks (logogram use)
  d  mapping gap: a glyph with no name-verified entry in signs.json, or a word
     token with no sign number
  t  subscript cut: the glyph reads ra2 (or ta2, pu2 ...) and the SigLA word
     reads ra. This is the known importer defect, not a reading conflict
  e  same signs, different order
  f  reading conflict: a different identified sign at the same aligned
     position, both sides sure and mapped
  u  unexplained: an identified sign present in one layer only

A record takes every class it shows (flags) and one primary class, by the
precedence f, d, t, b, a, c, e, u.

Nothing is chosen. The report lists both readings.

Usage:
    python3 scripts/layer_check.py --json OUT.json --md OUT.md
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORPUS = ROOT / "linear_a" / "data" / "corpus.json"
SIGNS = ROOT / "linear_a" / "data" / "signs.json"

DAMAGE = set(range(0x1076B, 0x10770))
PRECEDENCE = "fdtbaceu"
NON_SYLLABIC = {"logogram", "fraction", "compound_logogram", "ligature"}


def num_key(sign_id: str) -> str | None:
    """AB058 -> 58, A301 -> 301, AB131a -> 131, A709-2 -> 709-2, A402-VAS -> 402.

    A100-102 (the Unicode name of the VIR sign) and *100 are one sign: 100.
    """
    m = re.match(r"^\*?(?:AB|A)?0*(\d+)((?:-\d+)?)", sign_id)
    if not m:
        return None
    key = m.group(1) + m.group(2)
    return "100" if key == "100-102" else key


def is_fraction(key: str | None) -> bool:
    """Signs A701 to A799 are the fraction signs of the Unicode block."""
    return bool(key) and key.split("-")[0].isdigit() and 700 <= int(key.split("-")[0]) < 800


class Signs:
    def __init__(self):
        raw = json.loads(SIGNS.read_text(encoding="utf-8"))
        raw.pop("provenance", None)
        self.entries = raw
        self.by_key = collections.defaultdict(list)
        for sid, e in raw.items():
            k = num_key(sid)
            if k:
                self.by_key[k].append(e)
        self.value_to_key = {}
        for sid, e in raw.items():
            if e.get("phonetic"):
                assert e["phonetic"] not in self.value_to_key, e["phonetic"]
                self.value_to_key[e["phonetic"]] = num_key(sid)
        self.key_value = {k: v for v, k in self.value_to_key.items()}
        # Logogram abbreviations, from primary_reading such as "AB131/VIN".
        self.logogram_key = {}
        for sid, e in raw.items():
            pr = e.get("primary_reading") or ""
            if "/" in pr and "+" not in pr:
                self.logogram_key[pr.split("/", 1)[1].lower()] = num_key(sid)

    def category(self, key: str) -> str | None:
        cats = [e.get("category") for e in self.by_key.get(key, []) if e.get("category")]
        if not cats:
            return None
        if any(c not in NON_SYLLABIC for c in cats):
            return "sign"
        return cats[0]

    def kind(self, key: str) -> str:
        if is_fraction(key) or self.category(key) in NON_SYLLABIC:
            return "other"
        return "syllabogram"

    def glyph(self, ch: str) -> dict:
        cp = ord(ch)
        if cp in DAMAGE:
            return {"kind": "damage", "key": None, "cp": cp}
        name = unicodedata.name(ch, None)
        m = re.match(r"^LINEAR A SIGN (AB|A)(\d+(?:-\d+)?)", name or "")
        if not m:
            return {"kind": "unmapped", "key": None, "cp": cp, "name": name}
        key = num_key(m.group(1) + m.group(2))
        verified = any(e.get("unicode") == ch for e in self.by_key.get(key, []))
        if not verified:
            if is_fraction(key):
                # A fraction by its Unicode name; no signs.json entry holds it.
                return {"kind": "other", "key": key, "cp": cp, "name": name,
                        "verified": False}
            return {"kind": "unmapped", "key": key, "cp": cp, "name": name}
        return {"kind": self.kind(key), "key": key, "cp": cp, "name": name,
                "value": self.key_value.get(key), "verified": True}

    def token(self, t: str, local: dict | None = None) -> dict:
        if t in ("[?]", "[unclassified]"):
            return {"kind": "unknown", "key": None, "text": t}
        unsure = t.endswith("?")
        base = t.rstrip("?")
        if base == "vs":
            # lineara's vessel marker, part of an A4xx-VAS sign
            return {"kind": "other", "key": "VAS", "text": t, "unsure": False}
        if local and base in local:
            # The record's own sign array (same source as a SigLA word)
            # names the sign type for this reading.
            key = local[base]
        elif base in self.value_to_key:
            key = self.value_to_key[base]
        elif base in self.logogram_key:
            key = self.logogram_key[base]
        else:
            key = num_key(base.split("/")[0])
            if key and not self.by_key.get(key):
                key = None
        if key is None:
            return {"kind": "unmapped", "key": None, "text": t}
        return {"kind": self.kind(key), "key": key, "text": t, "unsure": unsure,
                "value": self.key_value.get(key)}


def glyph_seq(signs: Signs, text: str) -> list[dict]:
    """Signs of the glyph string. seg numbers the runs of signs between
    numerals, separators, line breaks and spaces."""
    out = []
    seg = 0
    for ch in text:
        cp = ord(ch)
        if 0x10600 <= cp <= 0x1077F or 0xE000 <= cp <= 0xF8FF or cp >= 0xF0000:
            d = signs.glyph(ch)
            d["seg"] = seg
            out.append(d)
        else:
            seg += 1
    sizes = collections.Counter(d["seg"] for d in out if d["kind"] != "damage")
    for d in out:
        d["alone"] = sizes[d["seg"]] == 1
    return out


def local_map(rec: dict) -> dict:
    """reading -> sign number, from the record's own sign array, where the
    reading names exactly one sign number in that record."""
    seen = collections.defaultdict(set)
    for sg in rec.get("signs") or []:
        k = num_key(sg.get("type") or "")
        if k and sg.get("reading"):
            seen[sg["reading"]].add(k)
    return {r: next(iter(ks)) for r, ks in seen.items() if len(ks) == 1}


def word_seq(signs: Signs, words: list[str], local: dict) -> list[dict]:
    out = []
    for wi, w in enumerate(words):
        for part in w.split("-"):
            pieces = part.split("+")
            for p in pieces:
                if not p:
                    continue
                d = signs.token(p, local)
                d["word"] = wi
                d["ligature"] = len(pieces) > 1
                out.append(d)
    return out


def label(d: dict) -> str:
    if "cp" in d:
        if d["kind"] == "damage":
            return f"U+{d['cp']:X} (damage)"
        base = d.get("value") or (f"*{d['key']}" if d.get("key") else "?")
        return f"{base} (U+{d['cp']:X})"
    return d["text"]


def classify_one_sided(d: dict, side: str, roles: dict) -> str:
    if d["kind"] in ("damage", "unknown"):
        return "a"
    if d["kind"] == "unmapped":
        return "d"
    if side == "w" and d.get("unsure"):
        return "b"
    if d.get("ligature") or d["kind"] == "other":
        return "c"
    if side == "g" and (roles.get(d["key"], set()) - {"syllabogram"} or d.get("alone")):
        return "c"
    return "u"


def classify_pair(g: dict, w: dict, source: str | None) -> str:
    if g["kind"] == "damage" or w["kind"] == "unknown":
        return "a"
    if g["kind"] == "unmapped" or w["kind"] == "unmapped":
        return "d"
    gv, wv = g.get("value") or "", w.get("value") or ""
    if source == "sigla" and gv and wv and gv != wv and re.fullmatch(re.escape(wv) + r"\d+", gv):
        return "t"
    if w.get("unsure"):
        return "b"
    if g["kind"] == "other" or w["kind"] == "other" or w.get("ligature"):
        return "c"
    return "f"


def _sub_cost(g: dict, w: dict) -> float:
    if g.get("key") and g.get("key") == w.get("key"):
        return 0.0
    if g["kind"] in ("damage", "unmapped") or w["kind"] in ("unknown", "unmapped"):
        return 0.4
    if g["kind"] == "other" or w["kind"] == "other":
        return 1.5
    return 1.0


def _gap_cost(d: dict) -> float:
    if d["kind"] == "damage":
        return 0.5
    if d["kind"] in ("other", "unknown") or d.get("alone"):
        return 0.3
    return 1.0


def align_chunk(gs: list[dict], ws: list[dict]) -> list[tuple]:
    """Least-cost pairing inside one non-equal chunk of the alignment. A
    damage placeholder or an unidentified sign pairs cheaply with anything, so
    a damaged glyph is set against the word sign it hides rather than against
    a neighbouring sign."""
    n, m = len(gs), len(ws)
    INF = float("inf")
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if i and D[i - 1][j] + _gap_cost(gs[i - 1]) < D[i][j]:
                D[i][j] = D[i - 1][j] + _gap_cost(gs[i - 1])
            if j and D[i][j - 1] + _gap_cost(ws[j - 1]) < D[i][j]:
                D[i][j] = D[i][j - 1] + _gap_cost(ws[j - 1])
            if i and j:
                c = D[i - 1][j - 1] + _sub_cost(gs[i - 1], ws[j - 1])
                if c < D[i][j]:
                    D[i][j] = c
    out = []
    i, j = n, m
    while i or j:
        if i and j and D[i][j] == D[i - 1][j - 1] + _sub_cost(gs[i - 1], ws[j - 1]):
            out.append((gs[i - 1], ws[j - 1])); i -= 1; j -= 1
        elif i and D[i][j] == D[i - 1][j] + _gap_cost(gs[i - 1]):
            out.append((gs[i - 1], None)); i -= 1
        else:
            out.append((None, ws[j - 1])); j -= 1
    return out[::-1]


def glyph_value(g: dict | None) -> str:
    if g is None:
        return "(none)"
    if g["kind"] == "damage":
        return "[damage]"
    return g.get("value") or (f"*{g['key']}" if g.get("key") else "?")


def conflict_words(W: list[dict], wmap: dict, diffs: list[dict], rec: dict) -> list[dict]:
    """For each word holding an f difference: the word as the word layer
    stores it, and the same span read from the glyph layer."""
    out = []
    for wi in sorted({d["word_index"] for d in diffs if d["cls"] == "f"}):
        idx = [j for j, w in enumerate(W) if w["word"] == wi]
        glyphs = [wmap.get(j) for j in idx]
        out.append({
            "word_index": wi,
            "word_layer": rec["words"][wi],
            "glyph_layer": "-".join(glyph_value(g) for g in glyphs),
            "glyph_codepoints": " ".join(f"U+{g['cp']:X}" if g else "-" for g in glyphs),
            "positions": [
                {"glyph": d["glyph"], "word": d["word"]}
                for d in diffs if d["cls"] == "f" and d["word_index"] == wi
            ],
        })
    return out


def check_record(signs: Signs, rid: str, rec: dict) -> dict:
    G = glyph_seq(signs, rec["unicode_text"])
    W = word_seq(signs, rec["words"], local_map(rec) if rec.get("word_source") == "sigla" else {})
    gk = [g["key"] or f"#{g['kind']}{i}" for i, g in enumerate(G)]
    wk = [w["key"] or f"@{w['kind']}{i}" for i, w in enumerate(W)]
    res = {"id": rid, "glyph_signs": len(G), "word_signs": len(W),
           "word_source": rec.get("word_source"), "diffs": []}
    src = rec.get("word_source")
    cut = []  # t: equal sign, SigLA word reading cut (ra for ra2)
    roles = collections.defaultdict(set)
    for sg in rec.get("signs") or []:
        k = num_key(sg.get("type") or "")
        if k:
            roles[k].add(sg.get("role"))
    sm = difflib.SequenceMatcher(None, gk, wk, autojunk=False)
    diffs = []
    wmap = {}  # word-layer token index -> aligned glyph
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for jj, g in zip(range(j1, j2), G[i1:i2]):
                wmap[jj] = g
            for g, w in zip(G[i1:i2], W[j1:j2]):
                v, t = g.get("value") or "", w["text"].rstrip("?")
                if src == "sigla" and v and v != t and re.fullmatch(re.escape(t) + r"\d+", v):
                    diffs.append({"cls": "t", "glyph": label(g), "word": w["text"],
                                  "word_index": w["word"]})
            continue
        gs, ws = G[i1:i2], W[j1:j2]
        damaged = any(x["kind"] in ("damage", "unknown", "unmapped") for x in gs + ws)
        for g, w in align_chunk(gs, ws):
            if g is not None and w is not None:
                wmap[W.index(w)] = g
                cls = classify_pair(g, w, src)
                possible = False
                if cls == "f" and damaged:
                    # The pairing sits next to damage or an unidentified
                    # sign, so the position is not certain. Not a conflict.
                    cls, possible = "a", True
                diffs.append({"cls": cls, "possible_conflict": possible, "glyph": label(g), "word": label(w),
                              "word_index": w["word"], "glyph_key": g.get("key"),
                              "word_key": w.get("key")})
            elif g is not None:
                diffs.append({"cls": classify_one_sided(g, "g", roles), "glyph": label(g), "word": None})
            else:
                diffs.append({"cls": classify_one_sided(w, "w", roles), "glyph": None,
                              "word": label(w), "word_index": w["word"]})
    # e: the same identified signs, in a different order.
    gc = collections.Counter(g["key"] for g in G if g["key"])
    wc = collections.Counter(w["key"] for w in W if w["key"])
    if (gc == wc and all(g["key"] for g in G) and all(w["key"] for w in W)
            and [g["key"] for g in G] != [w["key"] for w in W]):
        diffs = [d for d in diffs if d["cls"] == "t"] + [{"cls": "e", "glyph": None, "word": None}]
    if not diffs and all(g["key"] for g in G) and all(w["key"] for w in W):
        res["classes"] = []
        return res
    res["diffs"] = diffs
    if any(d["cls"] == "f" for d in diffs):
        res["conflict_words"] = conflict_words(W, wmap, diffs, rec)
    res["classes"] = sorted({d["cls"] for d in diffs}, key=PRECEDENCE.index)
    return res


def run() -> dict:
    signs = Signs()
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    rows = []
    for rid, rec in corpus.items():
        if rec.get("unicode_text") and rec.get("words"):
            rows.append(check_record(signs, rid, rec))
    dis = [r for r in rows if r["classes"]]
    primary = collections.Counter(r["classes"][0] for r in dis)
    flags = collections.Counter(c for r in dis for c in r["classes"])
    diff_counts = collections.Counter(d["cls"] for r in dis for d in r["diffs"])
    return {"population": len(rows), "agree": len(rows) - len(dis),
            "disagree": len(dis), "primary": dict(primary), "flags": dict(flags),
            "differences": dict(diff_counts), "records": rows}


def _sign_name(key: str | None, text: str) -> str:
    if not key:
        return text
    n = key.split("-")[0]
    return (f"AB{int(n):03d}" if int(n) < 200 else f"A{n}") + f" ({text})"


def conflict_entries(out: dict) -> dict[str, list[dict]]:
    """One `conflicts` entry per word holding an f difference, in the shape of
    the 2026-09-18 write-back. The word layer is "ours", the glyph layer is
    "theirs". No reading is chosen."""
    signs = Signs()
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    entries = {}
    for r in out["records"]:
        for cw in r.get("conflict_words", []):
            rec = corpus[r["id"]]
            W = word_seq(signs, [cw["word_layer"]], local_map(rec))
            G = [signs.glyph(chr(int(x[2:], 16))) if x != "-" else None
                 for x in cw["glyph_codepoints"].split()]
            diff_pos = []
            for pos, (w, g) in enumerate(zip(W, G), start=1):
                if g is None or g.get("key") != w.get("key"):
                    gname = unicodedata.name(chr(g["cp"]))[len("LINEAR A SIGN "):] if g else "none"
                    diff_pos.append(
                        f"position {pos}: word layer {_sign_name(w.get('key'), w['text'])}, "
                        f"glyph layer {gname} ({glyph_value(g)})")
            decoded = ", ".join(
                f"{x} {unicodedata.name(chr(int(x[2:], 16)))[len('LINEAR A SIGN '):]} {glyph_value(g)}"
                for x, g in zip(cw["glyph_codepoints"].split(), G) if x != "-")
            entries.setdefault(r["id"], []).append({
                "field": "w",
                "ours": cw["word_layer"],
                "theirs": cw["glyph_layer"],
                "ours_layer": "words (w): SigLA, through our own import",
                "theirs_layer": "unicode_text (u): lineara.xyz glyph string",
                "difference": "; ".join(diff_pos),
                "our_source": "SigLA, through our own import; the same reading stands in the SigLA document page of 2026-08-14 (references/inbox/sigla-refresh-2026-08-13/sigla-live-2026-08-14.json)",
                "their_source": f"lineara.xyz, the unicode_text of this record, decoded by Unicode 16.0 character name: {decoded}",
                "note": f"Found by the cross-layer check of 2026-09-18 (word {cw['word_index'] + 1} of the record). The two layers of this one record read a different sign at the same position. No reading is chosen. The drawing decides.",
            })
    return entries


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", type=pathlib.Path)
    a = ap.parse_args()
    out = run()
    out["conflict_entries"] = conflict_entries(out)
    print({k: v for k, v in out.items() if k not in ("records", "conflict_entries")})
    if a.json:
        a.json.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
