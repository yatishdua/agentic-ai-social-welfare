import pandas as pd
from src.ml.model_loader import load_eligibility_model

FEATURES = [
    "monthly_income",
    "income_per_capita",
    "net_worth",
    "family_size",
    "employment_status",
    "disability_flag"
]


class EligibilityAgent:
    def __init__(self):
        self.model = load_eligibility_model()

    def score(self, applicant_data: dict):
        """
        applicant_data: dict with structured applicant features
        """

        df = pd.DataFrame([applicant_data])

        # Ensure correct column order
        df = df[FEATURES]

        probability = self.model.predict_proba(df)[0][1]

        return {
            "eligibility_score": round(float(probability), 4),
            "recommended_decision": self._decision_from_score(probability)
        }

    def _decision_from_score(self, score: float):
        if score >= 0.9:
            return "AUTO_APPROVE"
        elif score >= 0.6:
            return "HUMAN_REVIEW"
        else:
            return "SOFT_DECLINE"
