from src.llm.factory import load_llm
from src.agents.extraction.schemas import ExtractedFields
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
import yaml
from src.utils.path_utils import project_path


class LLMExtractor:

    def __init__(self):
        self.llm = load_llm()
        self.use_structured = self._should_use_structured_output()

        if not self.use_structured:
            self.parser = PydanticOutputParser(
                pydantic_object=ExtractedFields
            )
            self.prompt = PromptTemplate(
                template="""
You are an information extraction engine.

Extract the required fields from the document.

{format_instructions}

Document Text:
{text}
""",
                input_variables=["text"],
                partial_variables={
                    "format_instructions": self.parser.get_format_instructions()
                },
            )

    def _should_use_structured_output(self) -> bool:
        with open(project_path("src", "config", "policy.yaml")) as f:
            policy = yaml.safe_load(f)

        return (
            policy["llm"]["provider"] == "openai"
            and policy["llm"]["model"]["openai"] == "gpt-4o-mini"
        )

    def extract(self, text: str) -> dict:
        truncated_text = text[:2000]

        # 🔥 OpenAI path (BEST)
        if self.use_structured:
            structured_llm = self.llm.with_structured_output(ExtractedFields)

            parsed: ExtractedFields = structured_llm.invoke(
                f"""
Extract the required fields from the document.

Document Text:
{truncated_text}
"""
            )

        # ⚠️ Ollama / fallback path
        else:
            prompt = self.prompt.format(text=truncated_text)
            parsed: ExtractedFields = self.parser.parse(
                self.llm.invoke(prompt)
            )

        # --- Normalize output ---
        fields = {}

        if parsed.monthly_income is not None:
            fields["monthly_income"] = {
                "value": parsed.monthly_income,
                "confidence": 0.9,
                "source": "LLM"
            }

        if parsed.credit_score is not None:
            fields["credit_score"] = {
                "value": parsed.credit_score,
                "confidence": 0.9,
                "source": "LLM"
            }

        overall_conf = (
            sum(f["confidence"] for f in fields.values()) / len(fields)
            if fields else 0.0
        )

        return {
            "fields": fields,
            "overall_confidence": round(overall_conf, 3)
        }
