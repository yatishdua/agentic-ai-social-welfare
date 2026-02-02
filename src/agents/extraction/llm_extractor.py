from src.agents.extraction.base_extractor import BaseExtractor


class LLMExtractor(BaseExtractor):

    def extract(self, text: str) -> dict:
        """
        Stub implementation.
        Replace with real LLM call later.
        """

        fields = {
            "monthly_income": {
                "value": 4500,
                "confidence": 0.95,
                "source": "LLM"
            },
            "credit_score": {
                "value": 720,
                "confidence": 0.9,
                "source": "LLM"
            }
        }

        overall_conf = sum(
            f["confidence"] for f in fields.values()
        ) / len(fields)

        return {
            "fields": fields,
            "overall_confidence": round(overall_conf, 3)
        }
