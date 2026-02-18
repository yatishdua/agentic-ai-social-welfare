from typing import Literal, Optional, List, Dict

from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class IntakeRoute(BaseModel):
    action: Literal["ASK_CLARIFY", "CONTINUE"]
    clarification: Optional[str] = None


SYSTEM_PROMPT = """
You assist with applicant intake.

Choose ONE action:
- ASK_CLARIFY: if the user's last message is ambiguous or likely incorrect.
- CONTINUE: if the message is clear enough to proceed with extraction.

If ASK_CLARIFY, provide a short clarification question.
Return structured output only.
"""


class IntakeRouter:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        ).with_structured_output(IntakeRoute)

    def route(
        self,
        user_message: str,
        recent_messages: Optional[List[Dict[str, str]]] = None
    ) -> IntakeRoute:
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        if recent_messages:
            # Provide a short conversation window for context (last 10 turns)
            for m in recent_messages[-10:]:
                role = m.get("role", "user")
                content = m.get("content", "")
                messages.append(HumanMessage(content=f"{role.upper()}: {content}"))

        messages.append(HumanMessage(content=user_message))

        return self.llm.invoke(messages)
