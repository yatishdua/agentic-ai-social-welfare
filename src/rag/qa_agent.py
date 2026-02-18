from typing import Literal, Optional, List

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class QARoute(BaseModel):
    action: Literal["ASK_CLARIFY", "RETRIEVE", "ANSWER_DIRECT"]
    clarification: Optional[str] = None


SYSTEM_PROMPT = """
You route policy questions for a social welfare assistant.

Choose ONE action:
- ASK_CLARIFY: only if the user question is ambiguous in a way that prevents any useful answer.
- RETRIEVE: for eligibility criteria/requirements, benefits, documents, thresholds, or any policy details.
- ANSWER_DIRECT: only for trivial, obvious responses that don't need policy lookup.

Important:
- If the user asks generally for eligibility criteria (even without naming a program), choose RETRIEVE.
- Do not ask which program unless the question explicitly implies multiple programs and no general criteria can be given.

If ASK_CLARIFY, provide a short clarification question.
Return structured output only.
"""


class PolicyQARouter:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        ).with_structured_output(QARoute)

    def route(self, user_question: str) -> QARoute:
        q = (user_question or "").lower()
        if any(
            k in q
            for k in [
                "eligibility",
                "criteria",
                "requirements",
                "eligible",
                "qualify",
                "qualification",
                "who can apply",
            ]
        ):
            return QARoute(action="RETRIEVE")

        return self.llm.invoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_question),
            ]
        )
