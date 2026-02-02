from src.llm.factory import load_llm
from src.agents.extraction.schemas import CreditReportSchema


class CreditReportLLMExtractor:
    """
    LLM-first extractor for credit reports.
    """

    def __init__(self):
        self.llm = load_llm().with_structured_output(CreditReportSchema)

    def extract(self, text: str) -> dict:
        parsed: CreditReportSchema = self.llm.invoke(
            f"""
You are extracting information from a CREDIT REPORT.

Rules:
- Extract numeric credit score only

Document Text:
{text[:1500]}
"""
        )

        return parsed.dict()
