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
        
    def validate_emirates_id(self, ui_emirates_id, extracted_emirates_id, confidence):
        issues = []

        if confidence < self.min_confidence:
            return None, "HUMAN_REVIEW", ["Low confidence in Emirates ID extraction"]

        if ui_emirates_id != extracted_emirates_id:
            issues.append(f"Emirates ID mismatch: UI={ui_emirates_id}, Extracted={extracted_emirates_id}")
            return None, "ASK_USER", issues

        return extracted_emirates_id, "AUTO_PROCEED", []

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


        # --- Emirates ID validation ---
        if "emirates_id" in extracted_data["fields"]:
            extracted_emirates_id = extracted_data["fields"]["emirates_id"]["value"]
            emirates_id_conf = extracted_data["fields"]["emirates_id"]["confidence"]

            emirates_id, action, eid_issues = self.validate_emirates_id(
                ui_emirates_id=ui_data["emirates_id"],
                extracted_emirates_id=extracted_emirates_id,
                confidence=emirates_id_conf
            )

            actions.append(action)
            issues.extend(eid_issues)

            if emirates_id:
                validated["emirates_id"] = emirates_id

        else:
            actions.append("ASK_USER")
            issues.append("Emirates ID missing from extracted data")

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
