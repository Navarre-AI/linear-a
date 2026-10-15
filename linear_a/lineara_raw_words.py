"""Words for lineara.xyz-sourced records, taken from the RAW transcription.

lineara.xyz (mwenge/lineara.xyz, LinearAInscriptions.js) stores two layers per
record:

  transcription        the raw glyph stream: Linear A signs, Aegean numbers,
                       the word divider U+10101, line breaks, and the lacuna
                       mark U+1076B (U+1076C..F once each).
  parsedInscription,   a derived layer. Its glyph "words" keep the lacuna
  words,               mark, but "transliteratedWords" drops it from inside
  transliteratedWords  words, which fuses the signs on either side; and
                       parsedInscription re-cuts the lines and in places
                       changes signs (AB021F to AB022F on HT 132).

This module rebuilds the word list from `transcription` alone, by rule:

  * a word is a run of Linear A signs (U+10600..U+1073F; the fraction signs
    U+10740..U+1076A are amounts, not signs of a word);
  * a run ends at the divider U+10101 (and U+10100, U+10102), at a line break,
    at an Aegean number, at a fraction, at any other character, and at a
    lacuna mark U+1076B..U+1076F;
  * a run that a lacuna mark touches carries that damage on its edge, written
    in the Leiden way: "]" before the first sign when the lacuna is just
    before the run, "[" after the last sign when it is just after. A run is
    never joined across a lacuna;
  * a sign's value is lineara.xyz's own value from items_analysis/syllables.txt
    (the table that produced transliteratedWords), lowercased, with subscript
    digits as plain digits (PA₃ -> pa3), the convention of the existing word
    lists;
  * the word list keeps every run of two or more signs, and every run with a
    damaged edge (a lone sign beside a lacuna is the visible part of a word,
    not a logogram). A lone undamaged sign is left out, as the existing
    selection left it out (only hyphenated transliteratedWords were kept).

The raw layer carries no doubt mark: its character inventory is Linear A
signs, Aegean numbers, the word separator dot, the Aegean check mark U+10102,
line breaks, the lacuna marks, spaces, one Linear B sign (B043) and a few
typographic marks (em dash, superscript digits, U+2248, U+007C, U+002C). No
combining dot below (U+0323) and no other doubt mark occurs, so a word built
here cannot say which signs the edition dots.
"""
from __future__ import annotations

import json
import re

LAYER = "lineara.xyz transcription (raw)"
DAMAGE = range(0x1076B, 0x10770)
DIVIDERS = {0x10100, 0x10101, 0x10102}
SIGN_LO, SIGN_HI = 0x10600, 0x1073F
_SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def load_inscriptions(js_path) -> dict:
    """The `inscriptions` Map of LinearAInscriptions.js, as a dict.

    The file is JavaScript: trailing commas and \\u{...} escapes are turned
    into JSON. A key that occurs twice (KH101) keeps its last value, as a
    JavaScript Map does."""
    s = open(js_path, encoding="utf-8").read()
    head = "var inscriptions = new Map("
    a = s.index(head) + len(head)
    b = s.index("]);", a) + 1
    body = s[a:b]
    body = re.sub(r",(\s*[\]}])", r"\1", body)
    body = re.sub(r"\\u\{([0-9a-fA-F]+)\}", lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def load_values(syllables_path) -> dict:
    """items_analysis/syllables.txt: glyph TAB value."""
    out = {}
    for line in open(syllables_path, encoding="utf-8"):
        line = line.rstrip("\n")
        if "\t" in line:
            g, v = line.split("\t", 1)
            out[g] = v.strip()
    return out


def sign_value(ch: str, values: dict) -> str:
    v = values.get(ch)
    if v is None:
        raise KeyError(f"no lineara.xyz value for U+{ord(ch):05X}")
    return v.translate(_SUB).lower()


FRACTION_LO, FRACTION_HI = 0x10740, 0x1076A


def is_sign(ch: str) -> bool:
    return SIGN_LO <= ord(ch) <= SIGN_HI


def is_fraction(ch: str) -> bool:
    return FRACTION_LO <= ord(ch) <= FRACTION_HI


def derived_tokens(glyph_words: list) -> tuple[str, list[int]]:
    """lineara.xyz's glyph `words` list, joined, with the token number of
    every character. Line-break tokens are left out."""
    text, tok = [], []
    for n, w in enumerate(glyph_words):
        if w == "\n":
            continue
        for ch in w:
            text.append(ch)
            tok.append(n)
    return "".join(text), tok


def align(raw: str, derived: str) -> dict[int, int]:
    """Raw position -> derived position, from difflib opcodes. A position is
    aligned inside an equal block, and inside a replace block of equal length
    on both sides (the same slot read as another sign). Every other position
    is unaligned."""
    import difflib
    out = {}
    sm = difflib.SequenceMatcher(None, raw, derived, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal" or (op == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                out[i1 + k] = j1 + k
    return out


def runs(transcription: str, values: dict, glyph_words: list | None = None,
         line_rule: str = "derived") -> list[dict]:
    """Every run of word signs in the raw transcription, with edge damage.

    Signs, lacunae, dividers, numbers and line breaks come from the raw
    layer. Where the raw layer puts two signs side by side with nothing
    between them, the cut between two words, and whether a fraction-range
    glyph is a sign of a word, come from lineara.xyz's glyph `words` list, at
    the aligned positions. An unaligned position takes no cut from it.

    line_rule says what a raw line break does:
      "cut"      it always ends a word;
      "join"     it never does (the line break is ignored);
      "derived"  it ends a word unless the signs on both sides are aligned to
                 one and the same glyph word of lineara.xyz (a word that runs
                 on to the next line there)."""
    if line_rule not in ("cut", "join", "derived"):
        raise ValueError(line_rule)
    # Line breaks are taken out of the stream before alignment (the derived
    # layer cuts its lines elsewhere) and remembered by position.
    raw_chars, nl_before = [], set()
    for ch in transcription:
        if ch == "\n":
            nl_before.add(len(raw_chars))
        else:
            raw_chars.append(ch)
    raw = "".join(raw_chars)
    amap, tok = {}, []
    if glyph_words is not None:
        derived, tok = derived_tokens(glyph_words)
        amap = align(raw, derived)
        dtext = derived

    def member(i: int, ch: str) -> bool:
        if is_sign(ch):
            return True
        if is_fraction(ch) and i in amap:
            # a fraction-range glyph inside a derived word token that also
            # holds a sign of the syllabary range is read there as a sign
            t = tok[amap[i]]
            return any(is_sign(c) for c, tt in zip(dtext, tok) if tt == t)
        return False

    out: list[dict] = []
    cur: list[str] = []
    before = False
    last_was_damage = False
    prev_i = None

    def close(after: bool):
        nonlocal cur, before
        if cur:
            out.append({"signs": cur, "damaged_before": before, "damaged_after": after})
        cur = []
        before = False

    for i, ch in enumerate(raw):
        cp = ord(ch)
        if i in nl_before and cur:
            joined = (prev_i is not None and prev_i in amap and i in amap
                      and tok[amap[prev_i]] == tok[amap[i]])
            if line_rule == "cut" or (line_rule == "derived" and not joined):
                close(after=False)
                prev_i = None
        if member(i, ch):
            if cur and prev_i is not None and prev_i in amap and i in amap \
                    and tok[amap[prev_i]] != tok[amap[i]]:
                close(after=False)
            if not cur:
                before = last_was_damage
            cur.append(sign_value(ch, values))
            last_was_damage = False
            prev_i = i
        elif cp in DAMAGE:
            close(after=True)
            last_was_damage = True
            prev_i = None
        else:
            close(after=False)
            last_was_damage = False
            prev_i = None
    close(after=False)
    return out


def word_string(run: dict) -> str:
    w = "-".join(run["signs"])
    if run["damaged_before"]:
        w = "]" + w
    if run["damaged_after"]:
        w = w + "["
    return w


def raw_words(transcription: str, values: dict, glyph_words: list | None = None,
              line_rule: str = "derived") -> list[str]:
    return [
        word_string(r)
        for r in runs(transcription, values, glyph_words, line_rule)
        if len(r["signs"]) >= 2 or r["damaged_before"] or r["damaged_after"]
    ]
