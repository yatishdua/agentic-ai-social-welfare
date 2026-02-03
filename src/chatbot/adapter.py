from uuid import uuid4

def build_application_state_from_chat(
    ui_data: dict,
    intent: str
) -> dict:
    return {
        "applicant_id": str(uuid4()),
        "interaction_mode": "chatbot",
        "intent": intent,

        "ui_data": ui_data,

        # docs (added later)
        "bank_statement_path": "",
        "credit_report_path": "",

        "bank_text": "",
        "credit_text": "",

        "bank_extraction": {},
        "credit_extraction": {},

        "normalized_features": {},
        "validation_result": {},
        "eligibility_result": {},

        "status": "CHAT_IN_PROGRESS",
        "audit_log": [],
    }
