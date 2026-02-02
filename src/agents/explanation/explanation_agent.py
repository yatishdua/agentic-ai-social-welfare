from src.llm.factory import load_llm
from src.agents.explanation.schemas import EligibilityExplanation


class ExplanationAgent:
    """
    Generates human-readable explanation for eligibility decisions.
    """

    def __init__(self):
        # Use structured output (safe, no JSON parsing)
        self.llm = load_llm().with_structured_output(
            EligibilityExplanation
        )

    def explain(self, decision_payload: dict) -> dict:
        """
        decision_payload should include:
        - recommended_decision
        - eligibility_score
        - validated_data
        - validation_issues (optional)
        """

        explanation: EligibilityExplanation = self.llm.invoke(
            f"""
You are explaining a government social welfare eligibility decision.

Rules:
- Be formal and clear
- Do NOT mention internal model names
- Do NOT mention probabilities explicitly
- Explain in simple terms suitable for applicants

Decision Context:
{decision_payload}
"""
        )

        return explanation.dict()
