from src.graph.state import ReviewState


def aggregator_node(state: ReviewState):

    summary = f"""
## AI Review

### Security
{chr(10).join(state["security_issues"])}

### Quality
{chr(10).join(state["quality_issues"])}

### Database
{chr(10).join(state["db_issues"])}

### Testing
{chr(10).join(state["test_issues"])}
"""

    return {
        "summary": summary,
        "inline_comments": state["inline_comments"],
    }
