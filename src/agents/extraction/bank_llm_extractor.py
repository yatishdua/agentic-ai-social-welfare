from src.llm.factory import load_llm
from src.agents.extraction.schemas import BankStatementSchema


class BankStatementLLMExtractor:
    """
    LLM-first extractor for bank statements.
    """

    def __init__(self):
        self.llm = load_llm().with_structured_output(BankStatementSchema)

    def extract(self, text: str) -> dict:
        parsed: BankStatementSchema = self.llm.invoke(
            f"""
You are extracting information from a BANK STATEMENT.

Rules:
- Identify salary credit transactions
- Ignore bonuses, refunds, and transfers
- If salary credit exists, set salary_credit_detected = true

Document Text:
{text[:2000]}
"""
        )

        return  {
            "salary_credit_amount": parsed.salary_credit_amount,
            "salary_credit_detected": parsed.salary_credit_detected,
            "confidence": 0.85,        # LLM confidence
            "source": "LLM"
        }
