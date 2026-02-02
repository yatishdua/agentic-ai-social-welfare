from src.agents.ocr.ocr_agent import OCRAgent
from src.agents.extraction.extraction_agent import ExtractionAgent
from src.agents.validation.validation_agent import ValidationAgent
from src.agents.eligibility_agent import EligibilityAgent


ocr_agent = OCRAgent()
extraction_agent = ExtractionAgent()
validation_agent = ValidationAgent()
eligibility_agent = EligibilityAgent()


def ocr_node(state):
    state["audit_log"].append("OCR started")

    bank = ocr_agent.extract_text(state["bank_statement_path"])
    credit = ocr_agent.extract_text(state["credit_report_path"])

    state["bank_text"] = bank["text"]
    state["credit_text"] = credit["text"]

    state["audit_log"].append("OCR completed")
    return state


def extraction_node(state):
    state["audit_log"].append("Extraction started")

    bank_extracted = extraction_agent.extract(state["bank_text"])
    credit_extracted = extraction_agent.extract(state["credit_text"])

    state["extracted_fields"] = {
        **bank_extracted["fields"],
        **credit_extracted["fields"]
    }

    state["audit_log"].append("Extraction completed")
    return state


def validation_node(state):
    state["audit_log"].append("Validation started")

    result = validation_agent.validate(
        ui_data=state["ui_data"],
        extracted_data={"fields": state["extracted_fields"]}
    )

    state["validation_result"] = result
    state["status"] = result["action"]

    state["audit_log"].append(f"Validation action={result['action']}")
    return state


def eligibility_node(state):
    state["audit_log"].append("Eligibility scoring started")

    eligibility_input = {
        **state["ui_data"],
        **state["validation_result"]["validated_data"]
    }

    result = eligibility_agent.score(eligibility_input)

    state["eligibility_result"] = result
    state["status"] = result["recommended_decision"]

    state["audit_log"].append("Eligibility scoring completed")
    return state
