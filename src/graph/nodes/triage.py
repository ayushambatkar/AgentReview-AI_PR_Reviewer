from src.graph.state import ReviewState


def triage_node(state: ReviewState):
    flags = {
        "security": "auth" in state["diff"].lower() or "sql" in state["diff"].lower() or "secret" in state["diff"].lower(),
        "db": "migration" in state["diff"].lower() or "schema" in state["diff"].lower(),
        "quality": True,
        "test": True
    }
    
    return {
        "routing_flags": flags,
    }