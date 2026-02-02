from typing import TypedDict, Dict, Any, List


class ApplicationState(TypedDict):
    applicant_id: str

    ui_data: Dict[str, Any]

    bank_statement_path: str
    credit_report_path: str

    bank_text: str
    credit_text: str

    # Document-level extraction
    bank_extraction: Dict[str, Any]
    credit_extraction: Dict[str, Any]

    # Normalized business features
    normalized_features: Dict[str, Any]

    validation_result: Dict[str, Any]
    eligibility_result: Dict[str, Any]

    status: str
    audit_log: List[str]
