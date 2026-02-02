from langgraph.graph import StateGraph, END
from src.agents.langgraph.state import ApplicationState
from src.agents.langgraph.nodes import (
    ocr_node,
    extraction_node,
    validation_node,
    eligibility_node
)


def build_application_graph():
    graph = StateGraph(ApplicationState)

    graph.add_node("ocr", ocr_node)
    graph.add_node("extract", extraction_node)
    graph.add_node("validate", validation_node)
    graph.add_node("eligibility", eligibility_node)

    graph.set_entry_point("ocr")

    graph.add_edge("ocr", "extract")
    graph.add_edge("extract", "validate")

    # Conditional branching
    def validation_router(state):
        if state["status"] == "AUTO_PROCEED":
            return "eligibility"
        return END

    graph.add_conditional_edges(
        "validate",
        validation_router,
        {
            "eligibility": "eligibility",
            END: END
        }
    )

    graph.add_edge("eligibility", END)

    return graph.compile()
