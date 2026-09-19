# lineara.xyz source files: removed 2026-09-18

This folder held two files. Both are gone from the tree.

| File | Size | What it was |
|---|---|---|
| `lineara_xyz_corpus.js` | 1.5 MB | A verbatim copy of the upstream JavaScript dataset from the lineara.xyz mirror (Robert Hogan, <https://lineara.xyz>). |
| `lineara_xyz_parsed.json` | 512 KB | The same dataset, parsed by this project into JSON. |

## Why they were removed

1. **No grant to redistribute.** The upstream repository carries no LICENSE
   file. This project therefore holds no permission to republish the dataset,
   and no permission to relicense it as CC BY 4.0, which is what the previous
   blanket licence on this repository claimed.
2. **Third-party image rights inside the data.** Every record in
   `lineara_xyz_corpus.js` carries an `imageRights` field. 1,328 records read
   "(c) Ecole Francaise d'Athenes". The `imageRightsURL` values point into
   GORILA PDF pages, for example `papers/GORILA-Vol1.pdf#page=38`. GORILA is in
   copyright.

The readings this project took from the mirror are still credited. See
[CREDITS.md](../../../../CREDITS.md) at the repository root.

## How to obtain the files

Get them from the source, not from this repository.

- The site: <https://lineara.xyz>
- The upstream repository: `mwenge/lineara.xyz` on GitHub. The dataset file is
  `LinearAInscriptions.js`.

Check the upstream terms yourself before you redistribute anything from it.

## If a script needs them

No script in this repository reads either file. The merged corpus in
`linear_a/data/corpus.json` already holds the records this project derived from
the mirror, under the `"lineara"` value in each record's `sources` array and
under the `lineara_id` field.

If you add code that needs the raw upstream dataset, fetch it from the source
above into a path you do not commit, and make the loader fail with a message
that points at this file.
