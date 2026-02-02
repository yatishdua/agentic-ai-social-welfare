from src.agents.extraction.document_types import DocumentType
from src.agents.extraction.bank_llm_extractor import BankStatementLLMExtractor
from src.agents.extraction.credit_llm_extractor import CreditReportLLMExtractor
from src.agents.extraction.bank_regex_extractor import BankStatementRegexExtractor


class ExtractionAgent:
    """
    LLM-first extraction agent.
    Regex is used only as a fallback.
    """

    def __init__(self):
        self.bank_llm = BankStatementLLMExtractor()
        self.credit_llm = CreditReportLLMExtractor()
        self.bank_regex = BankStatementRegexExtractor()

    def extract(self, text: str, document_type: DocumentType) -> dict:

        # -------- BANK STATEMENT --------
        if document_type == DocumentType.BANK_STATEMENT:
            try:
                result = self.bank_llm.extract(text)
                result["source"] = "LLM"
                return result
            except Exception as e:
                fallback = self.bank_regex.extract(text)
                fallback["fallback_reason"] = str(e)
                return fallback

        # -------- CREDIT REPORT --------
        if document_type == DocumentType.CREDIT_REPORT:
            try:
                result = self.credit_llm.extract(text)
                result["source"] = "LLM"
                return result
            except Exception as e:
                return {
                    "credit_score": None,
                    "source": "LLM",
                    "fallback_reason": str(e)
                }

        raise ValueError(f"Unsupported document type: {document_type}")
