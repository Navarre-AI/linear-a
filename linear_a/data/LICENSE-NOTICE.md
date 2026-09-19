# Licence notice for this folder

This folder is mixed. It does not carry one licence, so it carries no folder
`LICENSE` file. Read this notice instead.

The repository default is CC BY 4.0. See [LICENSE](../../LICENSE) at the
repository root. All credits are in [CREDITS.md](../../CREDITS.md).

## CC BY-NC-SA 4.0 in this folder

| Path | Why |
|---|---|
| `sources/sigla/**` | Derived from SigLA. The folder has its own `LICENSE` and `PROVENANCE.md`. |
| `corpus.json`, the records whose `sources` array contains `"sigla"` | SigLA provenance reaches those records. 772 of 1,881 on 2026-09-18. Each one also carries a `sigla_id`. |
| `signs.json` | Occurrence and document counts are computed over the merged corpus, which includes the 772 SigLA records. Derivative measurements fall under the SigLA ShareAlike term. |
| `sources/intermediate/unified_corpus_v2.json`, the records whose `sources` array contains `"sigla"` | An earlier merge of the same data. 772 of 1,880 records carry a `sigla_id`. |
| `sources/intermediate/canonical_id_map.json`, the 772 entries that carry a `sigla_id` | The map ties a SigLA id to a canonical document id. |

Required credit line for those paths, verbatim:

> Sign drawings from SigLA: The Signs of Linear A, a palaeographical database,
> by Ester Salgarella and Simon Castellan (https://sigla.phis.me/), licensed
> under CC BY-NC-SA 4.0.

## CC BY 4.0 in this folder

Everything else, including:

- `corpus.json` records whose `sources` array does not contain `"sigla"`.
- The GORILA-derived index tables `gorila_*.json`, `gorila_sign_index.xlsx` and
  `signs_to_gorila_index.json`. These record facts read out of GORILA (index
  rows, concordance rows, plate page numbers). GORILA itself is in copyright
  and is cited, not included. **Open decision for Matt:** whether these nine
  files stay public. See `verification/licensing-2026-09-18.md`.
- `sources/old_corpus/**` and the rest of `sources/intermediate/**`, which are
  this project's own working tables and code. Two files in
  `sources/intermediate/` are the exception, named above.

## Removed

`sources/lineara/` no longer holds the upstream lineara.xyz dataset. See
`sources/lineara/README.md` for what was there and how to get it from the
source.
