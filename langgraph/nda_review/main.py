"""NDA review walkthrough: input loading followed by placeholder nodes."""

import json
from pathlib import Path
from typing import NotRequired, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph


class ReviewState(TypedDict):
    reached_nodes: list[str]
    nda_text: NotRequired[str]
    playbook: NotRequired[dict[str, object]]


def load_inputs(state: ReviewState) -> ReviewState:
    """Read the fixed sample NDA and playbook without suppressing errors."""
    common_dir = Path(__file__).resolve().parents[2] / "common"
    nda_path = common_dir / "ndas" / "nda-001-mutual.md"
    playbook_path = common_dir / "playbooks" / "mutual-nda-v1.json"
    nda_text = nda_path.read_text(encoding="utf-8")
    playbook = json.loads(playbook_path.read_text(encoding="utf-8"))
    if not isinstance(playbook, dict):
        raise TypeError(
            f"Playbook JSON must contain an object at the top level: {playbook_path}"
        )
    return {
        "nda_text": nda_text,
        "playbook": playbook,
        "reached_nodes": [*state["reached_nodes"], "load_inputs"],
    }


def identify_clauses(state: ReviewState) -> ReviewState:
    """Placeholder for identifying NDA clauses; records traversal only."""
    return {"reached_nodes": [*state["reached_nodes"], "identify_clauses"]}


def review_against_playbook(state: ReviewState) -> ReviewState:
    """Placeholder for comparing clauses with policy; records traversal only."""
    return {"reached_nodes": [*state["reached_nodes"], "review_against_playbook"]}


def draft_revisions(state: ReviewState) -> ReviewState:
    """Placeholder for proposing clause revisions; records traversal only."""
    return {"reached_nodes": [*state["reached_nodes"], "draft_revisions"]}


def human_review(state: ReviewState) -> ReviewState:
    """Placeholder for human review; records traversal without pausing or approving."""
    return {"reached_nodes": [*state["reached_nodes"], "human_review"]}


def produce_report(state: ReviewState) -> ReviewState:
    """Placeholder for report generation; records traversal without creating a report."""
    return {"reached_nodes": [*state["reached_nodes"], "produce_report"]}


def build_graph():
    graph = StateGraph(ReviewState)

    graph.add_node("load_inputs", load_inputs)
    graph.add_node("identify_clauses", identify_clauses)
    graph.add_node("review_against_playbook", review_against_playbook)
    graph.add_node("draft_revisions", draft_revisions)
    graph.add_node("human_review", human_review)
    graph.add_node("produce_report", produce_report)

    graph.add_edge(START, "load_inputs")
    graph.add_edge("load_inputs", "identify_clauses")
    graph.add_edge("identify_clauses", "review_against_playbook")
    graph.add_edge("review_against_playbook", "draft_revisions")
    graph.add_edge("draft_revisions", "human_review")
    graph.add_edge("human_review", "produce_report")
    graph.add_edge("produce_report", END)

    return graph.compile()


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)
    graph = build_graph()
    initial_state: ReviewState = {"reached_nodes": []}
    result = graph.invoke(initial_state)
    print(f"Loaded NDA: {len(result['nda_text'])} characters.")
    print(f"Loaded playbook: {len(result['playbook'])} top-level fields.")
    print("Scaffold: remaining nodes are placeholders; no NDA review is performed.")
    print(" -> ".join(result["reached_nodes"]))


if __name__ == "__main__":
    main()
