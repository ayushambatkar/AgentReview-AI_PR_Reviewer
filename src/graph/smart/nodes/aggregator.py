from src.graph.state import ReviewState


def format_issue(item: object) -> str:
    if isinstance(item, dict):
        severity = item.get("severity")
        issue = item.get("issue")
        if severity and issue:
            return f"- [{severity}] {issue}"
        if issue:
            return f"- {issue}"
        return f"- {item}"

    return f"- {item}"


def format_issue_section(items: list[object]) -> str:
    if not items:
        return "- No findings"

    return "\n".join(format_issue(item) for item in items)


def aggregator_node(state: ReviewState):

    has_issues = any(
        [
            state["security_issues"],
            state["quality_issues"],
            state["db_issues"],
            state["test_issues"],
        ]
    )

    if not has_issues:
        return {
            "summary": "",
            "inline_comments": [],
        }

    summary = f"""
## AI Review

### Security
{format_issue_section(state["security_issues"])}

### Quality
{format_issue_section(state["quality_issues"])}

### Database
{format_issue_section(state["db_issues"])}

### Testing
{format_issue_section(state["test_issues"])}
"""

    return {
        "summary": summary,
        "inline_comments": state["inline_comments"],
    }
