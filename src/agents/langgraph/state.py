from typing import TypedDict, Dict, Any, List


class ApplicationState(TypedDict):
    applicant_id: str

    # NEW (safe additions)
    interaction_mode: str            # "form" | "chatbot"
    intent: str                      # "APPLY_WELFARE" | "KNOW_CRITERIA"

    ui_data: Dict[str, Any]

    bank_statement_path: str
    credit_report_path: str

    emirates_id_image_path: str

    bank_text: str
    credit_text: str

    emirate_text: str

    # Document-level extraction
    bank_extraction: Dict[str, Any]
    credit_extraction: Dict[str, Any]

    emirate_text_extraction: Dict[str, Any]

    # Normalized business features
    normalized_features: Dict[str, Any]

    validation_result: Dict[str, Any]
    eligibility_result: Dict[str, Any]

    status: str
    audit_log: List[str]
