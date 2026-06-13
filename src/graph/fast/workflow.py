from langgraph.graph import END, StateGraph

from src.graph.fast.node import fast_review_node
from src.graph.state import ReviewState

builder = StateGraph(ReviewState)

builder.add_node("fast_review", fast_review_node)
builder.set_entry_point("fast_review")
builder.add_edge("fast_review", END)

graph = builder.compile()
