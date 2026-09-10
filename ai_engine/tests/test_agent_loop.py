import json

import pytest

from core.agent_loop import AgentLoopError, run_agent_loop
from core.tools import ToolRegistry
from ingestion.corpus_store import CorpusStore
from ingestion.fetch import FetchedDocument


class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments


class FakeToolCall:
    def __init__(self, id_, name, arguments):
        self.id = id_
        self.function = FakeFunction(name, arguments)


class FakeMessage:
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


class FakeChoice:
    def __init__(self, message):
        self.message = message


class FakeResponse:
    def __init__(self, message):
        self.choices = [FakeChoice(message)]


class ScriptedClient:
    """Returns a scripted sequence of responses, one per .chat() call."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0

    def chat(self, messages, tools=None, **kwargs):
        self.calls += 1
        return self._responses.pop(0)


@pytest.fixture
def tool_registry(tmp_path):
    store = CorpusStore(tmp_path)
    store.ingest_document(
        FetchedDocument(
            url="http://siac.example/report",
            content_type="html",
            text="SIAC administered 663 new cases in 2024.",
            fetched_at="2026-01-01T00:00:00",
        ),
        institution="SIAC",
    )
    return ToolRegistry(store)


def test_loop_returns_immediately_on_final_message(tool_registry):
    client = ScriptedClient([FakeResponse(FakeMessage(content="final answer"))])
    run = run_agent_loop(client, tool_registry, [{"role": "user", "content": "hi"}])
    assert run.final_content == "final answer"
    assert run.iterations_used == 1
    assert run.tool_calls_made == []


def test_loop_executes_tool_call_then_returns_final(tool_registry):
    tool_call = FakeToolCall("call_1", "search_corpus", json.dumps({"query": "new cases"}))
    responses = [
        FakeResponse(FakeMessage(content=None, tool_calls=[tool_call])),
        FakeResponse(FakeMessage(content="Found 663 cases.")),
    ]
    client = ScriptedClient(responses)
    run = run_agent_loop(client, tool_registry, [{"role": "user", "content": "how many cases?"}])

    assert run.final_content == "Found 663 cases."
    assert run.iterations_used == 2
    assert len(run.tool_calls_made) == 1
    assert run.tool_calls_made[0]["name"] == "search_corpus"

    # a tool result message should have been appended to the conversation
    tool_messages = [m for m in run.messages if m.get("role") == "tool"]
    assert len(tool_messages) == 1
    assert "663" in tool_messages[0]["content"]


def test_loop_raises_when_max_iterations_exceeded(tool_registry):
    tool_call = FakeToolCall("call_1", "list_ingested_sources", "{}")
    # model keeps requesting tool calls forever
    responses = [FakeResponse(FakeMessage(content=None, tool_calls=[tool_call])) for _ in range(3)]
    client = ScriptedClient(responses)

    with pytest.raises(AgentLoopError):
        run_agent_loop(
            client, tool_registry, [{"role": "user", "content": "hi"}], max_iterations=3
        )


def test_loop_handles_unknown_tool_gracefully(tool_registry):
    tool_call = FakeToolCall("call_1", "not_a_real_tool", "{}")
    responses = [
        FakeResponse(FakeMessage(content=None, tool_calls=[tool_call])),
        FakeResponse(FakeMessage(content="handled the error")),
    ]
    client = ScriptedClient(responses)
    run = run_agent_loop(client, tool_registry, [{"role": "user", "content": "hi"}])
    assert run.final_content == "handled the error"
    tool_messages = [m for m in run.messages if m.get("role") == "tool"]
    assert "Unknown tool" in tool_messages[0]["content"]
