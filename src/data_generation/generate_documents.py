import pandas as pd

from src.utils.path_utils import project_path
from src.data_generation.generate_bank_statements import generate_bank_statement
from src.data_generation.generate_credit_reports import generate_credit_report
from src.data_generation.generate_assets_excel import generate_assets_excel


def run_document_generation(limit=50):
    df = pd.read_csv(
        project_path("data", "synthetic", "applicants.csv")
    ).head(limit)

    for _, row in df.iterrows():
        applicant_id = row["applicant_id"]
        name = row["full_name"]
        income = row["monthly_income"]

        generate_bank_statement(applicant_id, name, income)
        generate_credit_report(applicant_id, name)
        generate_assets_excel(applicant_id)

    print(f"Generated documents for {len(df)} applicants")


if __name__ == "__main__":
    run_document_generation()
