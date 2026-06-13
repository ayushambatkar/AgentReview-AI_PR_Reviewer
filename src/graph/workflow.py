from src.graph.fast.workflow import graph as fast_graph
from src.graph.smart.workflow import graph as smart_graph


def get_graph(review_mode: str):
    if review_mode == "smart":
        return smart_graph

    return fast_graph


graph = fast_graph
