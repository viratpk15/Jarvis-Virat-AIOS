"""
Jarvis AIOS
--------------------
Agent Node

Calls the LLM, parses the JSON response, validates the action,
and updates the LangGraph state.

Every LLM response is validated against the ParsedAction Pydantic
model before being used. The final action dict is additionally
validated for structural integrity before it enters the graph
state, providing defense-in-depth against malformed or unexpected
LLM outputs.
"""

import json

from langchain_core.messages import HumanMessage
from pydantic import ValidationError

from app.LLM.client import llm
from app.Prompts.agent import AGENT_PROMPT
from app.Models.action import ParsedAction, FinalAction
from app.Tools.registry import registry

from app.LangGraph.state import State


def _validate_tool_name_against_registry(tool_name: str) -> bool:
    """Check if a tool name is registered in the tool registry.

    This whitelist-based validation ensures the LLM can only request
    execution of tools that actually exist. Any unknown tool name
    is rejected, preventing the LLM from hallucinating tool names
    or attempting to call internal functions.

    Args:
        tool_name: The tool name to validate.

    Returns:
        True if the tool is registered, False otherwise.
    """
    try:
        registry.get(tool_name)
        return True
    except ValueError:
        return False


def _validate_action_dict(action: dict) -> None:
    """Validate the action dict structure before it enters the graph state.

    Ensures the action dict has the correct type field, all required
    keys for that type, and properly typed values. This is defense-
    in-depth: even if the Pydantic model validation passes, the final
    dict must still satisfy structural invariants.

    Args:
        action: The action dict to validate.

    Raises:
        ValueError: If the action dict is malformed or missing required
            fields. The error message is security-focused and does not
            leak internal implementation details.
    """
    if not isinstance(action, dict):
        raise ValueError(
            "The action must be a dictionary."
        )

    # Validate that the action has a type field
    action_type = action.get("type")
    if not isinstance(action_type, str) or not action_type.strip():
        raise ValueError(
            "The action must include a valid 'type' field "
            "with value 'final' or 'tool'."
        )

    # Validate action type is one of the known types
    if action_type not in ("final", "tool"):
        raise ValueError(
            f"Unknown action type: '{action_type}'. "
            "Allowed types are 'final' and 'tool'."
        )

    # Validate final action structure
    if action_type == "final":
        response = action.get("response")
        if not isinstance(response, str) or not response.strip():
            raise ValueError(
                "A 'final' action must include a non-empty "
                "'response' field with a string value."
            )
        return

    # Validate tool action structure
    if action_type == "tool":
        tool_name = action.get("tool")
        if not isinstance(tool_name, str) or not tool_name.strip():
            raise ValueError(
                "A 'tool' action must include a non-empty "
                "'tool' field with a string value."
            )

        # Arguments must be a dict if present
        arguments = action.get("arguments")
        if arguments is not None and not isinstance(arguments, dict):
            raise ValueError(
                "The 'arguments' field of a 'tool' action "
                "must be a dictionary."
            )


def _build_action_from_llm(raw_content: str) -> dict:
    """Parse and validate LLM response content into a safe action dict.

    The LLM response is first parsed as JSON, then validated against
    the ParsedAction Pydantic model. Tool actions are additionally
    validated against the registered tool registry to prevent execution
    of non-existent or hallucinated tools. Invalid or unsafe responses
    are rejected and replaced with a safe final action containing the
    original LLM output as a fallback.

    Args:
        raw_content: The raw string content from the LLM response.

    Returns:
        A validated action dict with either 'final' or 'tool' type.
    """
    # Step 1: Try to parse as JSON
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        # LLM response is not valid JSON — treat as final response
        return {
            "type": "final",
            "response": raw_content,
        }

    # Step 2: Reject non-dict values (e.g. LLM returned a string or array)
    if not isinstance(parsed, dict):
        return {
            "type": "final",
            "response": raw_content,
        }

    # Step 3: Validate against the shared action model
    try:
        validated = ParsedAction(**parsed)
    except ValidationError:
        # LLM response does not match the expected action schema
        return {
            "type": "final",
            "response": raw_content,
        }

    action_type = validated.action_type

    # Step 4: Validate final action
    if action_type == "final":
        response_text = validated.response or raw_content
        # Ensure response is a string (not a dict/list leaking internal state)
        if not isinstance(response_text, str):
            response_text = str(response_text)
        return {
            "type": "final",
            "response": response_text,
        }

    # Step 5: Validate tool action
    if action_type == "tool":
        tool_name = validated.tool or ""

        # Reject empty tool names
        if not tool_name.strip():
            return {
                "type": "final",
                "response": raw_content,
            }

        # Whitelist check: only allow registered tools
        if not _validate_tool_name_against_registry(tool_name):
            return {
                "type": "final",
                "response": raw_content,
            }

        # Extract and bounds-check arguments
        args = validated.arguments.model_dump(exclude_none=True)

        # Validate string argument lengths to prevent resource exhaustion
        for arg_key, arg_value in args.items():
            if isinstance(arg_value, str) and len(arg_value) > 100_000:
                return {
                    "type": "final",
                    "response": raw_content,
                }

        return {
            "type": "tool",
            "tool": tool_name,
            "arguments": args,
        }

    # Step 6: Unknown action type — fall back to final response
    return {
        "type": "final",
        "response": raw_content,
    }


def agent(state: State):
    """Call the LLM, parse the response as a JSON action, and update state.

    Every LLM response is validated against the ParsedAction Pydantic
    model before being used. Invalid responses are replaced with a safe
    final action containing the raw LLM output. The final action dict
    is additionally validated for structural integrity before it enters
    the graph state.

    Args:
        state: The current LangGraph state.

    Returns:
        A state update dict containing the validated action and
        optional response. If validation fails, a safe final action
        is returned with the raw LLM output instead of raising an
        exception, ensuring the graph continues normally.
    """
    prompt = f"""
{AGENT_PROMPT}

User:

{state["message"]}

Observation:

{json.dumps(state["observation"])}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    action = _build_action_from_llm(response.content)

    # Structural validation before the action enters the graph state.
    # This provides defense-in-depth: even if Pydantic validation and
    # registry checks pass, the final dict must still satisfy the
    # structural invariants required by downstream nodes.
    #
    # If validation fails, a safe final action is returned with the
    # raw LLM output as the response. This prevents malformed LLM
    # output from causing HTTP 500 errors — the graph continues
    # normally and the user always receives a response.
    try:
        _validate_action_dict(action)
    except ValueError:
        return {
            "action": {"type": "final", "response": response.content},
            "response": response.content,
        }

    if action.get("type") == "final":
        return {
            "action": action,
            "response": action.get("response", response.content),
        }

    if action.get("type") == "tool":
        return {
            "action": action,
        }

    # Defensive fallback — should not reach here if _build_action_from_llm is correct
    return {
        "action": {"type": "final", "response": response.content},
        "response": response.content,
    }