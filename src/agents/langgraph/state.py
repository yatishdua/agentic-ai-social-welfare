from typing import TypedDict, Optional, Dict, Any


class ApplicationState(TypedDict):
    applicant_id: str

    # Inputs
    ui_data: Dict[str, Any]
    bank_statement_path: str
    credit_report_path: str

    # OCR
    bank_text: Optional[str]
    credit_text: Optional[str]

    # Extraction
    extracted_fields: Optional[Dict[str, Any]]

    # Validation
    validation_result: Optional[Dict[str, Any]]

    # Eligibility
    eligibility_result: Optional[Dict[str, Any]]

    # Final
    status: Optional[str]
    audit_log: list
