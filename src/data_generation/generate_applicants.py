import uuid
import random
import numpy as np
import pandas as pd
import yaml

from uae_names import generate_local_name
from uae_addresses import generate_uae_address

# Reproducibility
random.seed(42)
np.random.seed(42)


def load_policy(path="src/config/policy.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def generate_company_name():
    prefixes = ["Al", "Emirates", "National", "Gulf", "United"]
    sectors = ["Trading", "Services", "Holdings", "Group", "Enterprises"]
    return f"{random.choice(prefixes)} {random.choice(sectors)} LLC"


def generate_applicant(policy):
    family_size = np.random.randint(1, 8)

    monthly_income = max(500, np.random.lognormal(mean=8, sigma=0.5))
    total_assets = max(0, np.random.lognormal(mean=11, sigma=0.7))
    liabilities = np.random.uniform(0, total_assets * 0.6)

    # Disability prevalence = 4%
    disability_flag = np.random.choice([0, 1], p=[0.96, 0.04])

    income_per_capita = monthly_income / family_size
    net_worth = total_assets - liabilities

    # Base eligibility (policy-driven)
    base_eligible = (
        income_per_capita < policy["income_threshold"]
        and net_worth < policy["asset_threshold"]
    )

    # Disability-aware probabilistic uplift
    if disability_flag == 1 and base_eligible:
        eligible = np.random.choice([1, 0], p=[0.6, 0.4])
    else:
        eligible = int(base_eligible)

    address_info = generate_uae_address()

    return {
        "applicant_id": str(uuid.uuid4()),

        # Identity
        "full_name": generate_local_name(),
        "age": np.random.randint(18, 65),
        "gender": random.choice(["male", "female"]),
        "nationality": "local",

        # Address
        "address": address_info["address"],
        "city": address_info["emirate"],
        "area": address_info["area"],

        # Employment
        "employment_status": random.choice(["employed", "unemployed"]),
        "employer_name": generate_company_name(),

        # Financials
        "family_size": family_size,
        "monthly_income": round(monthly_income, 2),
        "total_assets": round(total_assets, 2),
        "liabilities": round(liabilities, 2),
        "income_per_capita": round(income_per_capita, 2),
        "net_worth": round(net_worth, 2),

        # Special condition
        "disability_flag": disability_flag,

        # Label
        "eligible_label": eligible
    }


def generate_dataset(n_samples, policy):
    return pd.DataFrame(
        generate_applicant(policy)
        for _ in range(n_samples)
    )


if __name__ == "__main__":
    policy = load_policy()

    df = generate_dataset(
        n_samples=5000,
        policy=policy
    )

    output_path = "data/synthetic/applicants.csv"
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} UAE-local applicants → {output_path}")
