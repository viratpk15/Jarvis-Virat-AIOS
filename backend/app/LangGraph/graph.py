import logging

from langgraph.graph import StateGraph, START, END

from app.LangGraph.state import State

from app.LangGraph.nodes.router import router
from app.LangGraph.nodes.planner import planner
from app.LangGraph.nodes.executor import executor
from app.LangGraph.nodes.agent import agent
from app.LangGraph.nodes.tool_node import tool_node

logger = logging.getLogger(__name__)

# Maximum number of tool-calling iterations before forcing a final response.
# Prevents infinite loops when the LLM repeatedly requests tool execution.
MAX_TOOL_ITERATIONS = 10

builder = StateGraph(State)

builder.add_node("router", router)
builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.add_node("agent", agent)
builder.add_node("tool", tool_node)


def route_from_router(state: State):
    """Route from router to appropriate execution path.

    Routes based on request type:
    - resume → executor (if unfinished plan exists) or agent (if no plan)
    - conversation → agent (direct response)
    - single_tool → agent (direct tool execution)
    - multi_step → planner (plan generation)

    Args:
        state: The current LangGraph state.

    Returns:
        The next node name ('agent', 'planner', 'executor', or END).
    """
    request_type = state.get("request_type", "conversation")

    # Handle resume requests
    if request_type == "resume":
        plan = state.get("plan", {})
        # If there's an unfinished plan with pending steps, resume execution
        if (
            plan
            and plan.get("steps")
            and any(step.get("status") == "pending" for step in plan.get("steps", []))
        ):
            logger.info("Resuming interrupted plan")
            return "executor"
        else:
            # No unfinished plan, treat as normal conversation
            logger.info(
                "Resume requested but no unfinished plan, treating as conversation"
            )
            return "agent"

    if request_type == "multi_step":
        return "planner"

    # conversation and single_tool both go to agent
    return "agent"


def route_from_planner(state: State):
    """Route from planner to executor.

    After planning, route to executor only if the plan is structurally valid
    (non-empty steps). A plan that failed validation and was rejected carries
    an INVALID_PLAN termination outcome and an empty step list; such plans
    must never reach the executor and are routed to END instead.

    Args:
        state: The current LangGraph state.

    Returns:
        The next node name ('executor' or END).
    """
    plan = state.get("plan", {})
    steps = plan.get("steps", [])

    # Rejected plan (validation failed after retry): never execute it.
    if state.get("termination_reason") == "INVALID_PLAN":
        return END

    # Check if there are any pending steps
    if steps and any(step.get("status") == "pending" for step in steps):
        return "executor"

    return END


def route_from_executor(state: State):
    """Route from executor to appropriate next node.

    Routes based on executor's decision:
    - agent → execute next step
    - planner → replanning needed
    - END → execution complete

    Args:
        state: The current LangGraph state.

    Returns:
        The next node name ('agent', 'planner', or END).
    """
    route_to = state.get("_route_to", "agent")

    if route_to == END:
        return END

    return route_to


def route_from_agent(state: State):
    """Route from agent to tool node or back to executor.

    If the action type is 'tool', route to the tool node.
    Otherwise, route back to executor for completion.
    If the iteration count exceeds the maximum, force a final response.

    Args:
        state: The current LangGraph state.

    Returns:
        The next node name ('tool', 'executor', or END).
    """
    if state["action"].get("type") == "tool":
        iteration_count = state.get("iteration_count", 0)
        if iteration_count >= MAX_TOOL_ITERATIONS:
            return END
        return "tool"

    # Return to executor for completion
    return "executor"


builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    route_from_router,
    {
        "agent": "agent",
        "planner": "planner",
        END: END,
    },
)

builder.add_conditional_edges(
    "planner",
    route_from_planner,
    {
        "executor": "executor",
        END: END,
    },
)

builder.add_conditional_edges(
    "executor",
    route_from_executor,
    {
        "agent": "agent",
        "planner": "planner",
        END: END,
    },
)

builder.add_conditional_edges(
    "agent",
    route_from_agent,
    {
        "tool": "tool",
        "executor": "executor",
        END: END,
    },
)

builder.add_edge("tool", "executor")

graph = builder.compile()
