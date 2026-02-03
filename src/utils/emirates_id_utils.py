import re


EMIRATES_ID_REGEX = r"(784[- ]?\d{4}[- ]?\d{7}[- ]?\d)"

class EmiratesIdUtils:
    """
    Utility functions for parsing and validating Emirates ID numbers.
    """

    def __init__(self):
        self.emirates_id_regex = EMIRATES_ID_REGEX

    def extract_emirates_id(self, text: str) -> str | None:
        match = re.search(self.emirates_id_regex, text)
        if match:
            return match.group(0).replace(" ", "")
        return None


    def validate_emirates_id(self, extracted_id: str, user_id: str | None = None) -> bool:
        if not extracted_id:
            return False

        if user_id:
            return extracted_id.replace("-", "") == user_id.replace("-", "")

        return True
