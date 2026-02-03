from typing import Optional, List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


# 🔒 Explicit UIData schema (NO dict)
class UIData(BaseModel):
    employment_status: Optional[str]
    monthly_income: Optional[int]
    family_size: Optional[int]
    disability_flag: Optional[str]
    net_worth: Optional[int]
    emirates_id: Optional[str]

    class Config:
        extra = "forbid"


class IntakeResult(BaseModel):
    ui_data: UIData
    missing_fields: List[str]
    next_question: Optional[str]

    class Config:
        extra = "forbid"


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).with_structured_output(IntakeResult)


SYSTEM_PROMPT = """
You are collecting data for an economic welfare application.

Already collected fields (DO NOT ask again):
{state_data}

Required fields:
- employment_status (employed, unemployed)
- monthly_income (int)
- family_size (int)
- disability_flag (yes, no) Whether you are disabled or not
- net_worth (int)
- emirates_id (string)

Rules:
- Ask ONE question at a time
- Only focus on collecting data
- Normalize values
"""


def run_intake(chat_history: list, session_id: str,state) -> IntakeResult:
    messages = [SystemMessage(content=SYSTEM_PROMPT.format(state_data=state))]

    for m in chat_history:
        if m["role"] == "user":
            messages.append(HumanMessage(content=m["content"]))

    return llm.invoke(
        messages,
        config={"configurable": {"session_id": session_id}},
    )
