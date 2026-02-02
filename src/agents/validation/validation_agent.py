class ValidationAgent:
    """
    Validates and reconciles extracted applicant data
    coming from multiple sources.
    """

    def __init__(self, income_tolerance=0.1, min_confidence=0.7):
        self.income_tolerance = income_tolerance
        self.min_confidence = min_confidence

    def validate_income(self, ui_income, bank_income, bank_confidence):
        issues = []

        if bank_confidence < self.min_confidence:
            return None, "HUMAN_REVIEW", ["Low confidence in bank statement extraction"]

        diff_ratio = abs(ui_income - bank_income) / max(ui_income, 1)

        if diff_ratio <= self.income_tolerance:
            return bank_income, "AUTO_PROCEED", []
        else:
            issues.append(
                f"Income mismatch: UI={ui_income}, Bank={bank_income}"
            )
            return None, "ASK_USER", issues

    def validate(self, ui_data: dict, extracted_data: dict):
        """
        ui_data: values provided in UI form
        extracted_data: output of ExtractionAgent
        """

        validated = {}
        issues = []
        actions = []

        # --- Income validation ---
        if "monthly_income" in extracted_data["fields"]:
            bank_income = extracted_data["fields"]["monthly_income"]["value"]
            bank_conf = extracted_data["fields"]["monthly_income"]["confidence"]

            income, action, inc_issues = self.validate_income(
                ui_income=ui_data["monthly_income"],
                bank_income=bank_income,
                bank_confidence=bank_conf
            )

            actions.append(action)
            issues.extend(inc_issues)

            if income:
                validated["monthly_income"] = income

        else:
            actions.append("ASK_USER")
            issues.append("Monthly income missing from bank statement")

        # --- Final decision ---
        if "HUMAN_REVIEW" in actions:
            final_action = "HUMAN_REVIEW"
        elif "ASK_USER" in actions:
            final_action = "ASK_USER"
        else:
            final_action = "AUTO_PROCEED"

        return {
            "validated_data": validated,
            "issues": issues,
            "action": final_action
        }
