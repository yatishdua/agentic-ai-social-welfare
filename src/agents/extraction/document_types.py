from enum import Enum


class DocumentType(str, Enum):
    BANK_STATEMENT = "bank_statement"
    CREDIT_REPORT = "credit_report"
    EMIRATES_ID = "emirates_id"
