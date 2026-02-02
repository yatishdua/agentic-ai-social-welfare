import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    precision_score
)

DATA_PATH = "data/synthetic/applicants.csv"
RANDOM_STATE = 42


FEATURES = [
    "monthly_income",
    "income_per_capita",
    "net_worth",
    "family_size",
    "employment_status",
    "disability_flag"
]

TARGET = "eligible_label"


def load_data():
    df = pd.read_csv(DATA_PATH)

    # Encode employment_status
    df["employment_status"] = df["employment_status"].map(
        {"employed": 1, "unemployed": 0}
    )

    return df


def split_data(df):
    X = df[FEATURES]
    y = df[TARGET]

    return train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
    )


def train_logistic_regression(X_train, y_train):
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ))
    ])

    pipeline.fit(X_train, y_train)
    return pipeline


def train_gradient_boosting(X_train, y_train):
    model = GradientBoostingClassifier(
        random_state=RANDOM_STATE
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, model_name):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print(f"\n===== {model_name} Evaluation =====")
    print(classification_report(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))
    print("Precision:", precision_score(y_test, y_pred))

    return {
        "roc_auc": roc_auc_score(y_test, y_prob),
        "precision": precision_score(y_test, y_pred)
    }


def bias_analysis(df, model, model_name):
    print(f"\n===== Bias Analysis: {model_name} =====")

    df_eval = df.copy()
    
    df_eval["prediction"] = model.predict(df_eval[FEATURES])

    # Gender parity
    print("\nEligibility rate by gender:")
    print(df_eval.groupby("gender")["prediction"].mean())

    # Disability impact (expected positive skew)
    print("\nEligibility rate by disability:")
    print(df_eval.groupby("disability_flag")["prediction"].mean())


def run_training():
    df = load_data()
    X_train, X_test, y_train, y_test = split_data(df)

    # Logistic Regression
    lr_model = train_logistic_regression(X_train, y_train)
    lr_metrics = evaluate_model(
        lr_model, X_test, y_test, "Logistic Regression"
    )
    bias_analysis(df, lr_model, "Logistic Regression")

    # Gradient Boosting
    gb_model = train_gradient_boosting(X_train, y_train)
    gb_metrics = evaluate_model(
        gb_model, X_test, y_test, "Gradient Boosting"
    )
    bias_analysis(df, gb_model, "Gradient Boosting")

    print("\n===== Model Comparison =====")
    print("Logistic Regression:", lr_metrics)
    print("Gradient Boosting:", gb_metrics)


if __name__ == "__main__":
    run_training()
