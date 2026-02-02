import re
from src.agents.extraction.base_extractor import BaseExtractor


class RegexExtractor(BaseExtractor):

    def extract(self, text: str) -> dict:
        fields = {}

        # Monthly income
        salary_match = re.search(r"Salary Credit\s+(-?\d+)", text)
        if salary_match:
            fields["monthly_income"] = {
                "value": int(salary_match.group(1)),
                "confidence": 0.9,
                "source": "REGEX"
            }

        # Credit score
        credit_match = re.search(r"Credit Score:\s*(\d+)", text)
        if credit_match:
            fields["credit_score"] = {
                "value": int(credit_match.group(1)),
                "confidence": 0.85,
                "source": "REGEX"
            }

        overall_conf = (
            sum(f["confidence"] for f in fields.values()) / len(fields)
            if fields else 0.0
        )

        return {
            "fields": fields,
            "overall_confidence": round(overall_conf, 3)
        }
