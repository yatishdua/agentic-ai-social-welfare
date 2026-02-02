import yaml
from src.utils.path_utils import project_path
from src.agents.extraction.regex_extractor import RegexExtractor
from src.agents.extraction.llm_extractor import LLMExtractor


class ExtractionAgent:

    def __init__(self):
        self.policy = self._load_policy()
        self.regex_extractor = RegexExtractor()
        self.llm_extractor = LLMExtractor()

    def _load_policy(self):
        with open(project_path("src", "config", "policy.yaml")) as f:
            return yaml.safe_load(f)

    def extract(self, ocr_text: str) -> dict:
        mode = self.policy["extraction"]["mode"]

        # LLM-only mode
        if mode == "LLM":
            result = self.llm_extractor.extract(ocr_text)
            result["fallback_used"] = False
            return result

        # REGEX-first mode
        regex_result = self.regex_extractor.extract(ocr_text)

        if regex_result["overall_confidence"] >= \
           self.policy["extraction"]["regex_confidence_threshold"]:
            regex_result["fallback_used"] = False
            return regex_result

        # Fallback to LLM
        llm_result = self.llm_extractor.extract(ocr_text)
        llm_result["fallback_used"] = True
        return llm_result
