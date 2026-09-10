"""Drives the agentic loop for a single extraction task and validates the
model's output through the hallucination guard before anything is treated
as accepted.
"""

import json
import re

from core.agent_loop import run_agent_loop
from core.client import OpenRouterClient
from core.tools import ToolRegistry
from extraction.hallucination_guard import filter_verified_facts
from extraction.schemas import ExtractedFact
from extraction.system_prompt import SYSTEM_PROMPT
from ingestion.corpus_store import CorpusStore

FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


class ExtractionError(RuntimeError):
    pass


def _parse_final_json(raw: str) -> dict:
    cleaned = FENCE_RE.sub("", raw).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ExtractionError(
            f"Model's final response was not valid JSON: {exc}\nRaw output: {raw[:500]}"
        ) from exc


def extract(
    institution: str,
    task_description: str,
    corpus_store: CorpusStore,
    client: OpenRouterClient | None = None,
    max_iterations: int = 8,
) -> dict:
    client = client or OpenRouterClient()
    tool_registry = ToolRegistry(corpus_store)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Institution: {institution}\nTask: {task_description}",
        },
    ]

    run = run_agent_loop(client, tool_registry, messages, max_iterations=max_iterations)
    parsed = _parse_final_json(run.final_content)

    raw_facts = parsed.get("facts", [])
    facts: list[ExtractedFact] = []
    parse_errors: list[dict] = []
    for raw_fact in raw_facts:
        try:
            facts.append(ExtractedFact(**raw_fact))
        except Exception as exc:  # pydantic ValidationError or similar
            parse_errors.append({"raw_fact": raw_fact, "error": str(exc)})

    accepted, rejected = filter_verified_facts(facts, corpus_store)

    return {
        "institution": institution,
        "accepted_facts": accepted,
        "rejected_facts": rejected,
        "parse_errors": parse_errors,
        "iterations_used": run.iterations_used,
        "tool_calls_made": run.tool_calls_made,
        "raw_model_output": run.final_content,
    }
