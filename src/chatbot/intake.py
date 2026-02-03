REQUIRED_FIELDS = [
    "employment_status",
    "monthly_income",
    "family_size",
    "disability_flag",
    "net_worth",
    "emirates_id",
]

QUESTIONS = {
    "employment_status": "What is your current employment status?",
    "monthly_income": "What is your total monthly income?",
    "family_size": "How many people are there in your family (including you)?",
    "disability_flag": "Do you or any dependent have a registered disability? (Yes/No)",
    "net_worth": "What is your approximate total asset value?",
    "emirates_id": "Please enter your Emirates ID number.",
}


def get_next_missing_field(ui_data: dict):
    for field in REQUIRED_FIELDS:
        if field not in ui_data:
            return field
    return None