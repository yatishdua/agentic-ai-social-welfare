from src.agents.ocr.ocr_agent import OCRAgent
from src.agents.extraction.extraction_agent import ExtractionAgent
from src.agents.validation.validation_agent import ValidationAgent
from src.agents.eligibility_agent import EligibilityAgent
from src.utils.path_utils import project_path


class ApplicationOrchestrator:
    """
    Orchestrates the full application workflow
    from documents to final decision.
    """

    def __init__(self):
        self.ocr_agent = OCRAgent()
        self.extraction_agent = ExtractionAgent()
        self.validation_agent = ValidationAgent()
        self.eligibility_agent = EligibilityAgent()

    def process_application(
        self,
        applicant_id: str,
        ui_data: dict,
        bank_statement_path,
        credit_report_path
    ):
        audit_log = []

        # --- OCR ---
        bank_ocr = self.ocr_agent.extract_text(bank_statement_path)
        audit_log.append("OCR completed for bank statement")

        credit_ocr = self.ocr_agent.extract_text(credit_report_path)
        audit_log.append("OCR completed for credit report")

        # --- Extraction ---
        bank_extracted = self.extraction_agent.extract(bank_ocr["text"])
        audit_log.append(
            f"Bank extraction (fallback_used={bank_extracted['fallback_used']})"
        )

        credit_extracted = self.extraction_agent.extract(credit_ocr["text"])
        audit_log.append(
            f"Credit extraction (fallback_used={credit_extracted['fallback_used']})"
        )

        # --- Merge extracted fields ---
        merged_extracted = {
            "fields": {
                **bank_extracted["fields"],
                **credit_extracted["fields"]
            }
        }

        # --- Validation ---
        validation_result = self.validation_agent.validate(
            ui_data=ui_data,
            extracted_data=merged_extracted
        )

        audit_log.append(
            f"Validation action={validation_result['action']}"
        )

        # --- Decision branching ---
        if validation_result["action"] != "AUTO_PROCEED":
            return {
                "applicant_id": applicant_id,
                "status": validation_result["action"],
                "issues": validation_result["issues"],
                "audit_log": audit_log
            }

        # --- Eligibility Scoring ---
        eligibility_input = {
            **ui_data,
            **validation_result["validated_data"]
        }

        eligibility_result = self.eligibility_agent.score(
            eligibility_input
        )

        audit_log.append("Eligibility scoring completed")

        return {
            "applicant_id": applicant_id,
            "status": eligibility_result["recommended_decision"],
            "eligibility_score": eligibility_result["eligibility_score"],
            "audit_log": audit_log
        }
