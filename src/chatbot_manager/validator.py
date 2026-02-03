from typing import Literal
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class ValidationResult(BaseModel):
    intent: Literal[
        "ANSWER",
        "ASK_CRITERIA",
        "START_APPLY",
        "OUT_OF_SCOPE"
    ]
    raw_answer: str



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).with_structured_output(ValidationResult)


SYSTEM_PROMPT = """
Classify the user's last message.

ANSWER:
- numeric answers
- yes / no
- short responses to a question
- employed / unemployed

ASK_CRITERIA:
- eligibility
- criteria
- conditions
- am I eligible
- eligible

START_APPLY:
- apply
- start application
- I want to apply

OUT_OF_SCOPE:
- anything unrelated to economic welfare

Return ONLY structured output.
"""


def validate_user_message(user_message: str, session_id: str) -> ValidationResult:
    result = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ],
        config={"configurable": {"session_id": session_id}},
    )
    result.raw_answer = user_message
    return result
