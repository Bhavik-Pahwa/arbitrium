"""The agentic loop: send messages to the model, execute any tool calls it
requests, feed results back, repeat until the model returns a final
(non-tool-call) message or the iteration cap is hit.
"""

from dataclasses import dataclass, field

from core.client import OpenRouterClient
from core.tools import TOOL_SCHEMAS, ToolRegistry

DEFAULT_MAX_ITERATIONS = 8


class AgentLoopError(RuntimeError):
    pass


@dataclass
class AgentRun:
    messages: list[dict]
    final_content: str
    iterations_used: int
    tool_calls_made: list[dict] = field(default_factory=list)


def _message_to_dict(message) -> dict:
    entry: dict = {"role": "assistant", "content": message.content}
    if message.tool_calls:
        entry["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in message.tool_calls
        ]
    return entry


def run_agent_loop(
    client: OpenRouterClient,
    tool_registry: ToolRegistry,
    messages: list[dict],
    tools: list[dict] | None = TOOL_SCHEMAS,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
) -> AgentRun:
    conversation = list(messages)
    tool_calls_made: list[dict] = []

    for iteration in range(1, max_iterations + 1):
        response = client.chat(conversation, tools=tools)
        message = response.choices[0].message

        if not message.tool_calls:
            conversation.append({"role": "assistant", "content": message.content or ""})
            return AgentRun(
                messages=conversation,
                final_content=message.content or "",
                iterations_used=iteration,
                tool_calls_made=tool_calls_made,
            )

        conversation.append(_message_to_dict(message))

        for tool_call in message.tool_calls:
            result = tool_registry.dispatch(tool_call.function.name, tool_call.function.arguments)
            tool_calls_made.append(
                {"name": tool_call.function.name, "arguments": tool_call.function.arguments}
            )
            conversation.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": result}
            )

    raise AgentLoopError(
        f"Agent loop did not terminate within {max_iterations} iterations "
        f"(model kept requesting tool calls)."
    )
