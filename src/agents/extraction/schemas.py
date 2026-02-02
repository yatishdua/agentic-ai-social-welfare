from pydantic import BaseModel
from typing import Optional


class BankStatementSchema(BaseModel):
    salary_credit_amount: Optional[int]
    salary_credit_detected: bool


class CreditReportSchema(BaseModel):
    credit_score: Optional[int]
