from langgraph.graph import END, StateGraph

from src.graph.nodes.db_impact import db_impact_node
from src.graph.nodes.quality import quality_node
from src.graph.nodes.security import security_node
from src.graph.nodes.aggregator import aggregator_node
from src.graph.nodes.test_coverage import test_coverage_node
from src.graph.nodes.triage import triage_node
from src.graph.state import ReviewState

builder = StateGraph(ReviewState)

builder.add_node("triage", triage_node)

builder.add_node("security", security_node)
builder.add_node("quality", quality_node)
builder.add_node("db_impact", db_impact_node)
builder.add_node("test_coverage", test_coverage_node)

builder.add_node("aggregator", aggregator_node)

builder.set_entry_point("triage")

builder.add_edge("triage", "security")
builder.add_edge("security", "quality")
builder.add_edge("quality", "db_impact")
builder.add_edge("db_impact", "test_coverage")
builder.add_edge("test_coverage", "aggregator")

builder.add_edge("aggregator", END)

graph = builder.compile()