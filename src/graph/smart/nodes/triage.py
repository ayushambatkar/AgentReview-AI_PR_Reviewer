from src.graph.state import ReviewState


def triage_node(state: ReviewState):

    files = [f.lower() for f in state["files_changed"]]

    db_keywords = (
        "migration",
        "schema",
        "prisma",
        "sqlalchemy",
        "repository",
        "model",
        "transaction",
        ".sql",
    )

    test_keywords = (
        "test",
        "tests",
        "spec",
        "__tests__",
        "pytest",
    )

    db_detected = any(
        keyword in file
        for file in files
        for keyword in db_keywords
    )

    test_detected = any(
        keyword in file
        for file in files
        for keyword in test_keywords
    )

    flags = {
        "security": True,
        "quality": True,
        "db": db_detected,
        "test": test_detected,
    }

    return {
        "routing_flags": flags,
    }