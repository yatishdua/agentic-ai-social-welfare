from pydantic import BaseModel
from typing import List


class EligibilityExplanation(BaseModel):
    summary: str
    key_factors: List[str]