def normalize_chat_ui_data(ui_data: dict) -> dict:
    """
    Converts chatbot raw inputs into the exact schema
    expected by LangGraph.
    """

    normalized = {}

    # Emirates ID (string)
    normalized["emirates_id"] = str(ui_data["emirates_id"])

    # Employment status → numeric encoding
    # Assuming: Yes/Employed = 1, No/Unemployed = 0
    employment = ui_data["employment_status"].lower()
    normalized["employment_status"] = 1 if employment in ["yes", "employed"] else 0

    # Disability flag → numeric
    disability = ui_data["disability_flag"].lower()
    normalized["disability_flag"] = 1 if disability == "yes" else 0

    # Numeric fields
    normalized["family_size"] = int(ui_data["family_size"])
    normalized["monthly_income"] = int(ui_data["monthly_income"])
    normalized["net_worth"] = int(ui_data["net_worth"])

    # Derived feature
    normalized["income_per_capita"] = int(
        normalized["monthly_income"] / max(normalized["family_size"], 1)
    )

    return normalized
