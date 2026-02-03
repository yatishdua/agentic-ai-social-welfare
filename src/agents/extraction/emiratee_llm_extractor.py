from src.llm.factory import load_llm
from src.agents.extraction.schemas import EmiratesIDResult

class EmirateeLLMExtractor:
    """
    LLM-first extractor for credit reports.
    """

    def __init__(self):
        self.llm = load_llm().with_structured_output(EmiratesIDResult)


    def extract(self, text: str) -> dict:
        parsed: EmiratesIDResult = self.llm.invoke(
                    f"""
            Extract Emirates ID from the text and validate it.

        OCR Text:
        {text}


        Rules:
        - Emirates ID starts with 784
        - Return structured output only
        """
                )

        return parsed.dict()

