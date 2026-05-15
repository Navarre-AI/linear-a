# AI agent starter — point your own bot at lineara.eu's public corpus

This directory is a complete, minimal example of how a third-party LLM agent can use the public `Navarre-AI/linear-a` repo to answer questions about Linear A — with no access to the private references repo, no API key, no licensing negotiations, and no copyright exposure.

The example uses no external services beyond the LLM of your choice (Claude, OpenAI, Gemini, local Llama, etc.). All the structured data, sign tables, tablet positions, scribe profiles, bibliography, and analytical commentary that the agent needs comes from this repo.

## What you get

A Python script (`agent.py`) that:

1. Loads the structured corpus from `linear_a/data/sources/sigla/corpus_structured.json` — 772 Linear A tablets with per-position sign-id, role, reading, and certainty.
2. Loads the sign-attestation index — every sign and the tablets it appears on.
3. Loads the bibliography from `BIBLIOGRAPHY.md`.
4. Wires the above as **tools** that an LLM can call.
5. Lets you ask natural-language questions like "what does tablet HT 31 contain?" or "where does sign AB81 appear?" or "what scholars have published on the libation-formula corpus?"
6. Returns citation-grounded answers — every claim points back to either a structured datum or a bibliography entry.

## What this agent CAN do

- Look up any of 772 tablets by ID and return its full sign sequence, site, period, word count, etc.
- Look up any sign and return every tablet it appears on, with frequencies.
- Cite the bibliography for any author or year.
- Answer questions about scribal-hand distribution (when scribe data is loaded).
- Compare sign frequencies across sites.
- Generate Unicode Linear A sign sequences from sign IDs.
- Point users at primary scholarly sources by name + publisher URL.

## What this agent CANNOT do (without the private repo or chat tool)

- Quote verbatim from any of the ~500 PDFs in the project's library — those PDFs are third-party copyrighted and not in this repo.
- Summarise the *argument* of any specific paper — it has the bibliography metadata but not the paper text.
- Answer "what does Salgarella 2020 argue about sign AB81?" — it can only point you at Salgarella 2020 and let you read it yourself.

For the richer chunked-text retrieval, the invite-only chat tool at `lineara-ask.fly.dev` is the right destination. This starter agent is the **no-licensing-questions-asked** layer.

## Quick start

```bash
# In this directory:
pip install anthropic   # or openai, or any other LLM SDK
export ANTHROPIC_API_KEY=...
python agent.py "What is tablet HT 31?"
python agent.py "Which scribes worked at Khania?"
python agent.py "Who has published on libation-vessel inscriptions?"
```

The first run loads ~772 tablets and ~315 signs into memory in <1 second.

## Adapting to your LLM

The `agent.py` script uses Claude via the Anthropic SDK as its example. The tool-call discipline (which is the key part — every claim must be grounded in a tool result) maps cleanly to:

- **OpenAI**: their function-calling API has the same shape. Swap `client.messages.create(...)` for `client.chat.completions.create(...)` with `tools=[...]`.
- **Gemini**: same — function declarations + automatic function calling.
- **Local models** (llama.cpp, Ollama, etc.): if the model supports tool use, the structure is identical; if not, use a structured prompt that asks the model to emit JSON with a `tool_name` and `args` and parse it in a loop.

The point is the **data shape**, not the LLM. The `tools.py` module is LLM-agnostic — it just exposes a set of functions that any agent can call.

## Architecture in one paragraph

A user query goes to the LLM. The LLM is told it has six tools: `lookup_tablet`, `lookup_sign`, `list_tablets_at_site`, `list_signs_by_role`, `search_bibliography`, and `render_sign_sequence`. The LLM decides which tools to call (often two or three per query). Each tool reads from local JSON files. Results return to the LLM, which composes a final answer that cites which tool calls supported which claims. The answer is rendered with structured citations the user can click through.

This is *exactly* the pattern that `lineara-ask.fly.dev` uses — minus the chunk-retrieval over copyrighted text. For most factual queries about Linear A, this starter agent answers as well as the chat tool. Where it can't is exactly where copyright would have been an issue.

## Where to take it from here

Once you have this running, the obvious extensions:

1. **Add semantic search over your own legally-held PDFs.** The pipeline is documented in the private repo's `research/embedding-storage-design-2026-05-15.md` and the script at `scripts/embed_corpus.py` (also visible in the private repo). Voyage 3-large at 1024 dimensions, packed per-paper `.f32` binaries. ~$2 of API calls embeds a 300-paper corpus.

2. **Hybrid retrieval.** The combination of BM25 + semantic + entity-boost makes a real difference; the implementation is in `scripts/corpus_search.py` of the private repo. We'll mirror that to the public repo as it stabilises.

3. **Citation-grounded output.** Wrap your LLM's answer in a structured response that *forces* every claim to cite a tool call. See `agent.py` `ANSWER_TOOL_SCHEMA` for the shape we use.

4. **Multi-source readings.** When the multi-interpretation reading model (designed; not yet built) lands, the agent will be able to answer "what do SigLA, GORILA, and lineara.xyz each read for position 3 of HT 31?" via a single tool call.

5. **Add tooling for your own domain.** If you have a different scholarly corpus, the data-shape patterns (per-entity JSON, sign-attestation index, citation graph) are domain-agnostic. Linear A is a convenient demonstration because the corpus is small enough to fit on a single laptop.

## Licensing

The code in this directory is MIT-licensed. The data it loads from `linear_a/data/sources/sigla/` is derived from open SigLA data; redistribute with attribution per SigLA's terms. The bibliography in `BIBLIOGRAPHY.md` is the project's compilation; redistribute with attribution per the CC BY-SA 4.0 license used across the lineara.eu catalog.

## Contact

Issues, pull requests, and "I built something with this" reports are welcome:
- GitHub: https://github.com/Navarre-AI/linear-a/issues
- Email: matt@navarre.training
- The lineara.eu contact form
