from langgraph.graph import END, StateGraph

from src.graph.smart.nodes.aggregator import aggregator_node
from src.graph.smart.nodes.db_impact import db_impact_node
from src.graph.smart.nodes.quality import quality_node
from src.graph.smart.nodes.security import security_node
from src.graph.smart.nodes.test_coverage import test_coverage_node
from src.graph.smart.nodes.triage import triage_node
from src.graph.state import ReviewState

builder = StateGraph(ReviewState)

builder.add_node("triage", triage_node)
builder.add_node("security", security_node)
builder.add_node("quality", quality_node)
builder.add_node("db_impact", db_impact_node)
builder.add_node("test_coverage", test_coverage_node)
builder.add_node("aggregator", aggregator_node)

builder.set_entry_point("triage")


def route_after_quality(state: ReviewState):
    flags = state["routing_flags"]

    if flags["db"]:
        return "db_impact"

    if flags["test"]:
        return "test_coverage"

    return "aggregator"


def route_after_db(state: ReviewState):
    flags = state["routing_flags"]

    if flags["test"]:
        return "test_coverage"

    return "aggregator"


# Always run these
builder.add_edge("triage", "security")
builder.add_edge("security", "quality")

# Conditionally run DB / Test reviewers
builder.add_conditional_edges(
    "quality",
    route_after_quality,
)

builder.add_conditional_edges(
    "db_impact",
    route_after_db,
)

# Test reviewer only runs when routed to
builder.add_edge("test_coverage", "aggregator")

builder.add_edge("aggregator", END)

graph = builder.compile()