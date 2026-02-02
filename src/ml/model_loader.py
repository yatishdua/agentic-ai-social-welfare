import joblib
import os

from src.utils.path_utils import project_path

MODEL_PATH = project_path("models", "eligibility_model.pkl")


def load_eligibility_model():
    print(f"Loading model from {MODEL_PATH}...")
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Eligibility model not found. Train model first."
        )

    return joblib.load(MODEL_PATH)
