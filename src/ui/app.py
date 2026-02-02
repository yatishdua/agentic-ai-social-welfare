import streamlit as st
import pandas as pd

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")



from src.agents.langgraph.graph import build_application_graph
from src.utils.path_utils import project_path


st.set_page_config(
    page_title="AI Social Support Eligibility System",
    layout="wide"
)

st.title("🧠 AI-Driven Social Support Eligibility System")

st.markdown(
    """
    This system evaluates social support applications using:
    - Document OCR
    - Policy-driven extraction (Regex / LLM)
    - Validation & conflict resolution
    - ML-based eligibility scoring
    - Human-in-the-loop governance
    """
)

# -------------------------------------------------------------------
# Sidebar – Configuration
# -------------------------------------------------------------------
st.sidebar.header("⚙️ Configuration")

extraction_mode = st.sidebar.selectbox(
    "Extraction Mode",
    ["REGEX", "LLM"],
    help="Controls how document extraction is performed"
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Change extraction mode in policy.yaml for backend execution.\n\n"
    "This toggle is for demo visibility."
)

# -------------------------------------------------------------------
# Load graph once
# -------------------------------------------------------------------
@st.cache_resource
def load_graph():
    return build_application_graph()


graph = load_graph()

# -------------------------------------------------------------------
# Applicant Form
# -------------------------------------------------------------------
st.header("📄 Applicant Application Form")

col1, col2 = st.columns(2)

with col1:
    monthly_income = st.number_input(
        "Monthly Income (Declared)", min_value=0, value=4000
    )
    family_size = st.number_input(
        "Family Size", min_value=1, value=4
    )
    net_worth = st.number_input(
        "Net Worth", min_value=0, value=50000
    )

with col2:
    employment_status = st.selectbox(
        "Employment Status",
        ["employed", "unemployed"]
    )
    disability_flag = st.checkbox(
        "Applicant has a disability"
    )

st.markdown("---")

# -------------------------------------------------------------------
# Document Selection
# -------------------------------------------------------------------
st.header("📎 Select Applicant Documents")

df = pd.read_csv(project_path("data", "synthetic", "applicants.csv"))

selected_applicant = st.selectbox(
    "Select Applicant ID (for demo)",
    df["applicant_id"].tolist()
)

bank_path = project_path(
    "data", "raw", "bank_statements",
    f"{selected_applicant}_bank_statement.pdf"
)

credit_path = project_path(
    "data", "raw", "credit_reports",
    f"{selected_applicant}_credit_report.pdf"
)

st.write("📄 Bank Statement:", bank_path.name)
st.write("📄 Credit Report:", credit_path.name)

# -------------------------------------------------------------------
# Run Decision
# -------------------------------------------------------------------
st.markdown("---")

if st.button("🚀 Submit Application"):
    with st.spinner("Processing application..."):

        state = {
            "applicant_id": selected_applicant,
            "ui_data": {
                "monthly_income": monthly_income,
                "income_per_capita": monthly_income / family_size,
                "net_worth": net_worth,
                "family_size": family_size,
                "employment_status": 1 if employment_status == "employed" else 0,
                "disability_flag": 1 if disability_flag else 0
            },
            "bank_statement_path": bank_path,
            "credit_report_path": credit_path,
            "audit_log": []
        }

        result = graph.invoke(state)

    st.success("Application processed successfully!")

    # ----------------------------------------------------------------
    # Decision Output
    # ----------------------------------------------------------------
    st.header("✅ Decision Result")

    status = result.get("status")

    if status == "AUTO_APPROVE":
        st.success("🎉 Application Auto-Approved")
    elif status == "ASK_USER":
        st.warning("⚠️ Additional Information Required from Applicant")
    elif status == "HUMAN_REVIEW":
        st.error("🧑‍⚖️ Application Sent for Human Review")
    else:
        st.info(f"Status: {status}")

    if "eligibility_result" in result:
        st.metric(
            label="Eligibility Score",
            value=result["eligibility_result"]["eligibility_score"]
        )

    # ----------------------------------------------------------------
    # Audit Trail
    # ----------------------------------------------------------------
    st.header("🧾 Audit Trail")

    for step in result["audit_log"]:
        st.write("•", step)

    # ----------------------------------------------------------------
    # Debug Section (Optional)
    # ----------------------------------------------------------------
    with st.expander("🔍 Debug: Full State Output"):
        st.json(result)
