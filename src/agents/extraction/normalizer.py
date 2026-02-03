class FeatureNormalizer:
    """
    Converts document-level extraction into
    validation-ready evidence.
    """

    def normalize(self, bank_data: dict, credit_data: dict, emirate_data: str) -> dict:
        evidence = {"fields": {}}

        # --- Monthly Income ---
        if bank_data.get("salary_credit_detected"):
            evidence["fields"]["monthly_income"] = {
                "value": bank_data["salary_credit_amount"],
                "confidence": bank_data.get("confidence", 0.0),
                "source": bank_data.get("source", "UNKNOWN")
            }

        # --- Credit Score ---
        if credit_data.get("credit_score") is not None:
            evidence["fields"]["credit_score"] = {
                "value": credit_data["credit_score"],
                "confidence": credit_data.get("confidence", 0.8),
                "source": credit_data.get("source", "LLM")
            }

        # --- Emirates ID Validity ---
        if emirate_data.get("emirates_id") is not None:
            evidence["fields"]["emirates_id"] = {
                "value": emirate_data["emirates_id"],
                "confidence": emirate_data.get("confidence", 0.9),
                "source": emirate_data.get("source", "OCR")
            }

        return evidence
