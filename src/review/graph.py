from langgraph.graph import END
from langgraph.graph import StateGraph

from src.review.nodes.review_node import (
    create_review_node,
)
from src.review.state import ReviewState


def build_review_graph(llm):
    builder = StateGraph(ReviewState)

    builder.add_node(
        "reviewer",
        create_review_node(llm),
    )

    builder.set_entry_point("reviewer")

    builder.add_edge(
        "reviewer",
        END,
    )

    return builder.compile()