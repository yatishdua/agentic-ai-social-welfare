from src.agents.ocr.ocr_agent import OCRAgent
from src.agents.extraction.extraction_agent import ExtractionAgent
from src.agents.validation.validation_agent import ValidationAgent
from src.agents.eligibility_agent import EligibilityAgent
from src.agents.explanation.explanation_agent import ExplanationAgent
from src.agents.extraction.document_types import DocumentType
from src.agents.extraction.normalizer import FeatureNormalizer
from src.agents.ocr.emirates_id_ocr import OcrEmiratesId



ocr_agent = OCRAgent()



extraction_agent = ExtractionAgent()
normalizer = FeatureNormalizer()
eligibility_agent = EligibilityAgent()
validation_agent = ValidationAgent()
explanation_agent = ExplanationAgent()
emirates_id_ocr_agent = OcrEmiratesId()


# -------------------------------
# OCR NODE
# -------------------------------
def ocr_node(state):
    state["status"] = "Running OCR"
    state["audit_log"].append("OCR started")

    bank = ocr_agent.extract_text(state["bank_statement_path"])
    credit = ocr_agent.extract_text(state["credit_report_path"])

    emirates_id = emirates_id_ocr_agent.ocr_emirates_id(state["emirates_id_image_path"])

    state["bank_text"] = bank["text"]
    state["credit_text"] = credit["text"]
    state["emirate_text"] = emirates_id

    state["audit_log"].append("OCR completed")
    return state


# -------------------------------
# EXTRACTION NODE
# -------------------------------
def extraction_node(state):
    state["audit_log"].append("Extraction started")

    bank_extracted = extraction_agent.extract(
        state["bank_text"],
        DocumentType.BANK_STATEMENT
    )

    credit_extracted = extraction_agent.extract(
        state["credit_text"],
        DocumentType.CREDIT_REPORT
    )

    emiratee_id_extracted = extraction_agent.extract(
        state["emirate_text"],
        DocumentType.EMIRATES_ID
    )

    
    

    state["bank_extraction"] = bank_extracted
    state["credit_extraction"] = credit_extracted
    state["emirate_text_extraction"] = emiratee_id_extracted

    state["normalized_features"] = normalizer.normalize(
        bank_data=bank_extracted,
        credit_data=credit_extracted,
        emirate_data=emiratee_id_extracted
    )

    state["audit_log"].append("Extraction completed")
    return state


# -------------------------------
# VALIDATION NODE
# -------------------------------
def validation_node(state):
    state["audit_log"].append("Validation started")

    result = validation_agent.validate(
            ui_data=state["ui_data"],
            extracted_data=state["normalized_features"]
        )

    state["validation_result"] = result
    state["status"] = result["action"]

    state["audit_log"].append(f"Validation action={result['action']}")
    return state

# -------------------------------
# ELIGIBILITY NODE
# -------------------------------
def eligibility_node(state):
    state["audit_log"].append("Eligibility started")

    eligibility_input = {
        **state["ui_data"],
        **state["validation_result"]["validated_data"]
    }

    result = eligibility_agent.score(eligibility_input)

    # 🔥 ADD EXPLANATION STEP
    explanation = explanation_agent.explain({
        "recommended_decision": result["recommended_decision"],
        "eligibility_score": result.get("eligibility_score"),
        "validated_data": state["validation_result"]["validated_data"],
        "validation_issues": state["validation_result"].get("issues", [])
    })

    result["explanation"] = explanation

    state["eligibility_result"] = result
    state["status"] = result["recommended_decision"]

    state["audit_log"].append("Eligibility completed")
    return state
