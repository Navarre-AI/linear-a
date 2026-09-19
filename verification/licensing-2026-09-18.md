# Licensing correction, 2026-09-18

Group B of the public corpus review. The repository claimed a blanket CC BY 4.0
licence over data that is not ours to relicense. This note records the fix, the
file list, and the two decisions that are still open.

## The defect

`LICENSE` and `README.md` released everything in the repository under
CC BY 4.0. Eight tracked files are derived from upstream sources that do not
permit that:

1. SigLA is CC BY-NC-SA 4.0. CC BY 4.0 drops both the NonCommercial term and
   the ShareAlike term. Seven tracked files are SigLA-derived
   (`corpus_structured.json` plus six FileMaker exports).
2. The lineara.xyz upstream repository carries no licence file, so this project
   holds no grant to redistribute its dataset, let alone to relicense it. Two
   tracked files were copies of it. One of them,
   `lineara_xyz_corpus.js`, also carried `imageRights` strings reading
   "(c) Ecole Francaise d'Athenes" on 1,328 records, and `imageRightsURL`
   values pointing into GORILA PDF pages.
3. The SigLA credit line appeared nowhere in the repository. Attribution is
   required by the licence.

Two further files are SigLA-derived by measurement and were also mislabelled:
`linear_a/data/signs.json` (counts computed over the merged corpus) and
`linear_a/data/sources/intermediate/unified_corpus_v2.json` (an earlier merge
of the same records).

## What changed

### Added

| File | What it does |
|---|---|
| `CREDITS.md` | Credits every source, with what it gave and the licence or permission that applies. |
| `linear_a/data/LICENSE-NOTICE.md` | Marks the split inside the mixed data folder, file by file. |
| `linear_a/data/sources/lineara/README.md` | Says what was removed, why, and how to get it from the source. |
| `linear_a/data/sources/sigla/LICENSE` | CC BY-NC-SA 4.0 with the credit line, for the folder. |
| `linear_a/data/sources/sigla/PROVENANCE.md` | Upstream source, what this project changed, where the data reaches. |
| `linear_a/data/sources/sigla/filemaker_export/LICENSE` | The same terms for the export subfolder, naming `fm_ingest.py` as the CC BY 4.0 exception. |
| `verification/licensing-2026-09-18.md` | This note. |

### Removed

| File | Size | Reason |
|---|---|---|
| `linear_a/data/sources/lineara/lineara_xyz_corpus.js` | 1.5 MB | Verbatim upstream copy. No grant. Carried third-party image-rights strings and GORILA page pointers. |
| `linear_a/data/sources/lineara/lineara_xyz_parsed.json` | 512 KB | The same dataset, parsed. Same grant problem for the underlying text. |

No script in the repository read either file. A grep over every tracked `.py`,
`.md`, `.json`, `.js` and `.sh` file for `lineara_xyz`, `sources/lineara` and
`sources.lineara` returned no hit outside the folder itself. There is no import
to fix. The new `README.md` in that folder tells a future loader what to do
instead: fetch from the source into an uncommitted path, and fail with a
message that points at the README.

### Relabelled

| File | Was | Now |
|---|---|---|
| `LICENSE` | Blanket CC BY 4.0 | Part 1: CC BY 4.0 default, the existing text kept. Part 2: the explicit CC BY-NC-SA 4.0 path list with the verbatim SigLA credit. Part 3: material cited but not licensed here. |
| `README.md`, two sentences | "fully public, released under CC-BY-4.0" | The accurate two-licence statement, with the credit line and links to `LICENSE` and `CREDITS.md`. No other README sentence was touched. |
| `linear_a/data/sources/sigla/corpus_structured.json` | CC BY 4.0 | CC BY-NC-SA 4.0, by the folder `LICENSE` and by part 2.1 of the root `LICENSE`. |
| The six FileMaker exports | CC BY 4.0 | CC BY-NC-SA 4.0, by the subfolder `LICENSE` and by part 2.1. |
| `linear_a/data/corpus.json` | CC BY 4.0 | Split by field. A record is CC BY-NC-SA 4.0 when its `sources` array contains `"sigla"`. 772 of 1,881 records on this date. Every such record also carries a `sigla_id`. |
| `linear_a/data/signs.json` | CC BY 4.0 | CC BY-NC-SA 4.0. The counts are derivative measurements over the merged corpus. |
| `linear_a/data/sources/intermediate/unified_corpus_v2.json` | CC BY 4.0 | Split by the same `sources` field rule. 772 of 1,880 records. |
| `linear_a/data/sources/intermediate/canonical_id_map.json` | CC BY 4.0 | The 772 entries carrying a `sigla_id` are CC BY-NC-SA 4.0. The rest is CC BY 4.0. |

### Reserved

Part 2.3 of the root `LICENSE` reserves the image paths that the SigLA-derived
image layers will occupy (`images/sigla/`, `images/signs/`, `images/documents/`,
`images/a301/`, `data/signs/`, `data/sigla-merge.json`), with the same terms and
the same credit line. Each one gets its own `LICENSE` file when it lands. No
image file is tracked in this repository today.

## How the marking follows the Creative Commons guidance

- Creative Commons FAQ (page updated 2025-05-13): where only part of a work is
  under a CC licence, mark clearly which parts are under which licence. Part 2
  of the root `LICENSE` does that by path, and by field for the mixed files.
- CC wiki, "Marking your work with a CC license" (last revised 25 February
  2019): note third-party material and attribute each item correctly.
  `CREDITS.md` does that.
- CC BY 4.0 material may be incorporated into a CC BY-NC-SA 4.0 work. The
  reverse does not hold, so no SigLA-derived path is labelled CC BY 4.0.
- Canonical deed and legal-code links are used throughout. No licence text was
  invented. In the deed summaries the separator before each term's description
  is a colon, not a dash, which is a punctuation change and not a wording
  change.
- Per-folder `LICENSE` files are present, so a reader who lands on a deep path,
  or a tool that copies one folder, sees the terms without reading the root.

## Two open decisions for Matt

### 1. The nine GORILA index extract files

The files, all under `linear_a/data/`:

`gorila_sign_index.xlsx`, `gorila_sign_index.json`,
`gorila_sign_index_rows.json`, `gorila_page_map.json`,
`gorila_concordances.json`, `gorila_concordances_full.json`,
`gorila_sign_variants.json`, `gorila_sign_plates.json`,
`signs_to_gorila_index.json`.

The question: concordance rows and plate page numbers are facts, and facts are
not protected. The selection and arrangement of GORILA's own index is the
publisher's. `gorila_page_map.json` and `gorila_sign_plates.json` sit closest
to a reproduction of GORILA's apparatus.

**Recommendation: keep seven, and strip two.** Keep the sign index rows, the
concordances, the variants and the crosswalk: those are read out of the volumes
as data and the project uses them everywhere, 49 of 168 tracked files mention
GORILA. Cut `gorila_page_map.json` and `gorila_sign_plates.json` down to what
the project actually needs, which is the plate reference per sign, and drop any
field that reproduces the page-by-page layout of the printed apparatus. Keep
the GORILA citation in `CREDITS.md` either way. These files stay CC BY 4.0 on
our own arrangement, with GORILA cited as the source, until you say otherwise.
Nothing in this change touched them.

### 2. Registration matrices for the layers that are not permitted

`registration.json` in the private repository holds similarity transforms for
1,643 of 1,643 eligible documents, 2,397 layer pairs. It is not in the public
repository today. The transforms themselves are measurements, so copyright does
not reach them. Two problems block a straight publication. Each record repeats
the restricted mirror photograph's file path, its URL under `/img/mirror/`, and
its exact pixel width and height, which makes the file an index into an image
set this project may not publish. And 704 of the 2,397 pairs are
`sigla_tracing` rows, which are measurements over SigLA tracings and therefore
CC BY-NC-SA 4.0, not CC BY 4.0.

**Recommendation: publish the stripped form.** Keep the matrix (scale, rotation,
tx, ty) and the quality score. Drop every `path`, `url`, `width` and `height`
for the mirror and GORILA layers. Label the `sigla_tracing` rows
CC BY-NC-SA 4.0 under the same field rule this change already uses for
`corpus.json`. That publishes our measurement and nothing of the restricted
layers. For the five permitted documents, the transforms can stay in the
comparator manifests as they are, once the photograph permission is on file.

## Still open elsewhere, not part of this change

The permission for the five photographs is not on file. Until it is, no
photograph and no comparator layer publishes. That blocks the two "five
documents only" classes in the licence map, not this change.
