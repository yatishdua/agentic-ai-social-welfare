import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/synthetic/applicants.csv"


def load_data(path=DATA_PATH):
    return pd.read_csv(path)


def basic_overview(df):
    print("\n=== Dataset Shape ===")
    print(df.shape)

    print("\n=== Column Info ===")
    print(df.info())

    print("\n=== Missing Values ===")
    print(df.isna().sum())


def numeric_summary(df):
    print("\n=== Numeric Summary ===")
    print(df.describe())


def eligibility_distribution(df):
    print("\n=== Eligibility Distribution ===")
    print(df["eligible_label"].value_counts(normalize=True))

    df["eligible_label"].value_counts().plot(
        kind="bar",
        title="Eligibility Distribution"
    )
    plt.xlabel("Eligibility")
    plt.ylabel("Count")
    plt.show()


def income_analysis(df):
    df["monthly_income"].plot(
        kind="hist",
        bins=50,
        title="Monthly Income Distribution"
    )
    plt.xlabel("Monthly Income")
    plt.show()

    df["income_per_capita"].plot(
        kind="hist",
        bins=50,
        title="Income Per Capita Distribution"
    )
    plt.xlabel("Income Per Capita")
    plt.show()


def disability_analysis(df):
    print("\n=== Disability Impact on Eligibility ===")
    print(df.groupby("disability_flag")["eligible_label"].mean())

    df.groupby("disability_flag")["eligible_label"].mean().plot(
        kind="bar",
        title="Eligibility Rate by Disability"
    )
    plt.xlabel("Disability Flag")
    plt.ylabel("Eligibility Rate")
    plt.show()


def family_size_analysis(df):
    df.groupby("family_size")["eligible_label"].mean().plot(
        kind="line",
        marker="o",
        title="Eligibility Rate by Family Size"
    )
    plt.xlabel("Family Size")
    plt.ylabel("Eligibility Rate")
    plt.show()


def asset_vs_income(df):
    plt.scatter(
        df["monthly_income"],
        df["net_worth"],
        alpha=0.3
    )
    plt.xlabel("Monthly Income")
    plt.ylabel("Net Worth")
    plt.title("Income vs Net Worth")
    plt.show()


def run_eda(path=DATA_PATH):
    df = load_data(path)

    basic_overview(df)
    numeric_summary(df)
    eligibility_distribution(df)
    income_analysis(df)
    disability_analysis(df)
    family_size_analysis(df)
    asset_vs_income(df)

    return df
