import re


class BankStatementRegexExtractor:
    """
    Regex fallback extractor for bank statements.
    """

    def extract(self, text: str) -> dict:
        matches = re.findall(
            r"(Salary Credit|SALARY|Salary)\s+(-?\d+)",
            text
        )

        if not matches:
            return {
                "salary_credit_amount": None,
                "salary_credit_detected": False,
                "source": "REGEX"
            }

        amounts = [int(m[1]) for m in matches]

        return {
            "salary_credit_amount": max(amounts),
            "salary_credit_detected": True,
            "confidence": 0.95,        # Regex confidence
            "source": "REGEX"
        }
