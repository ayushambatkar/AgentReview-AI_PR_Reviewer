from src.graph.state import ReviewState


def triage_node(state: ReviewState):
    flags = {
        "security": "auth" in state["diff"].lower() or "sql" in state["diff"].lower() or "secret" in state["diff"].lower(),
        "db": "migration" in state["diff"].lower() or "schema" in state["diff"].lower(),
        "quality": True,
        "test": "test" in state["diff"].lower() or "spec" in state["diff"].lower() or "assert" in state["diff"].lower(),
    }
    
    return {
        "routing_flags": flags,
    }