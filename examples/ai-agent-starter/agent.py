#!/usr/bin/env python3
"""Minimal Linear A agent. Demonstrates how a third-party LLM bot can answer
questions about Linear A using only the public Navarre-AI/linear-a repo.

Usage:
    export ANTHROPIC_API_KEY=...
    pip install anthropic
    python agent.py "What is tablet HT 31?"
    python agent.py "Where does sign AB81 appear?"
    python agent.py "Who has published on the libation-formula corpus?"

The agent calls Claude with a system prompt that tells it about six tools
(see tools.py). Claude decides which tools to call. Each tool returns
plain JSON. Claude composes a final answer citing the tool results.

Adapt to other LLMs by replacing the Anthropic SDK calls with your
provider's tool-use API. The tools.TOOLS dict and tools.TOOL_SCHEMAS list
are LLM-agnostic.
"""
import json
import os
import sys

try:
    from anthropic import Anthropic
except ImportError:
    print("Install the Anthropic SDK first: pip install anthropic", file=sys.stderr)
    sys.exit(1)

import tools  # local module — tools.py in the same directory

MODEL = os.environ.get("LA_AGENT_MODEL", "claude-sonnet-4-6")

SYSTEM = """You are a Linear A research assistant. You answer questions about
Linear A (the undeciphered Bronze Age script of Minoan Crete) using the
tools provided.

Discipline:
- Every factual claim must be grounded in a tool result. If you don't have
  a tool result to back a claim, say "I don't have that information from
  my tools" and suggest where the user might look (e.g., the bibliography,
  the SigLA website at https://sigla.phis.me, lineara.xyz, or the
  lineara.eu chat tool at https://lineara-ask.fly.dev).
- Cite which tool calls supported which claims. The user can audit your
  reasoning.
- If a question is about a specific scholarly argument (e.g., "what does
  Salgarella argue about X"), you don't have the paper text — you only
  have the bibliography entry. Cite the entry and point the user at the
  publisher's URL or institutional library access.
- The corpus you can query is SigLA (Salgarella & Castellan), 772 Linear
  A tablets. There are additional smaller corpora (sigla.phis.me, GORILA,
  Hogan's lineara.xyz) that you should mention when relevant but cannot
  query directly.
- Be concise. The user is sophisticated and does not need long preambles."""


def run(query: str) -> str:
    client = Anthropic()
    messages = [{"role": "user", "content": query}]

    # Tool-use loop: Claude may call multiple tools in sequence.
    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM,
            tools=tools.TOOL_SCHEMAS,
            messages=messages,
        )

        # Did Claude call any tools?
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        text_blocks = [b for b in response.content if b.type == "text"]

        if not tool_uses:
            # No more tools — done. Return the text.
            return "\n".join(b.text for b in text_blocks)

        # Append assistant message + tool results
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tu in tool_uses:
            fn = tools.TOOLS.get(tu.name)
            if fn is None:
                result = {"error": f"unknown tool {tu.name}"}
            else:
                try:
                    result = fn(**tu.input)
                except Exception as e:
                    result = {"error": str(e)}
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": json.dumps(result),
            })
            # Optional: print each tool call so the user can audit
            print(f"  → {tu.name}({tu.input}) → "
                  f"{json.dumps(result)[:120]}…", file=sys.stderr)

        messages.append({"role": "user", "content": tool_results})


def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py 'your question'", file=sys.stderr)
        sys.exit(2)
    query = " ".join(sys.argv[1:])
    answer = run(query)
    print()
    print("─── ANSWER " + "─" * 50)
    print(answer)


if __name__ == "__main__":
    main()

