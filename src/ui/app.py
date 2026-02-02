import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")


import streamlit as st

from src.agents.langgraph.graph import build_application_graph
from src.utils.path_utils import project_path


st.set_page_config(
    page_title="AI Social Welfare Eligibility",
    layout="wide"
)

st.title("🏛️ Social Welfare Eligibility Application")

# -----------------------------
# Build graph once
# -----------------------------
@st.cache_resource
def load_graph():
    return build_application_graph()

graph = load_graph()

# -----------------------------
# Base upload directory
# -----------------------------
UPLOAD_ROOT = project_path("data", "uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Application Form
# -----------------------------
st.header("📄 Applicant Information")

with st.form("application_form"):

    emirates_id = st.text_input(
        "Emirates ID",
        placeholder="784-XXXX-XXXXXXX-X"
    )

    family_size = st.number_input(
        "Family Size",
        min_value=1,
        step=1
    )

    employment_status = st.selectbox(
        "Employment Status",
        ["employed", "unemployed"]
    )

    disability_flag = st.checkbox("Disability (Yes / No)")

    # -------- Financial Declaration --------
    st.subheader("💰 Financial Details (Self-declared)")

    monthly_income = st.number_input(
        "Declared Monthly Income",
        min_value=0,
        step=500
    )

    total_assets = st.number_input(
        "Total Assets",
        min_value=0,
        step=5000
    )

    # -------- Documents --------
    st.subheader("📎 Upload Documents")

    bank_file = st.file_uploader(
        "Upload Bank Statement (PDF)",
        type=["pdf"]
    )

    credit_file = st.file_uploader(
        "Upload Credit Report (PDF)",
        type=["pdf"]
    )

    submitted = st.form_submit_button("Submit Application")

# -----------------------------
# Handle Submission
# -----------------------------
if submitted:

    if not emirates_id:
        st.error("Emirates ID is required.")
        st.stop()

    if not bank_file or not credit_file:
        st.error("Both bank statement and credit report are required.")
        st.stop()

    # Create applicant-specific folder
    applicant_dir = UPLOAD_ROOT / emirates_id.replace(" ", "")
    applicant_dir.mkdir(parents=True, exist_ok=True)

    bank_path = applicant_dir / "bank_statement.pdf"
    credit_path = applicant_dir / "credit_report.pdf"

    # Save files (overwrite allowed for retries)
    with open(bank_path, "wb") as f:
        f.write(bank_file.getbuffer())

    with open(credit_path, "wb") as f:
        f.write(credit_file.getbuffer())

    # Initial graph state
    state = {
        "ui_data": {
            "emirates_id": emirates_id,
            "family_size": family_size,
            "employment_status": 1 if employment_status == "employed" else 0,
            "disability_flag": 1 if disability_flag else 0,
            "monthly_income": monthly_income,
            "net_worth": total_assets,
            "income_per_capita": (monthly_income / family_size) if family_size > 0 else 0
        },
        "bank_statement_path": str(bank_path),
        "credit_report_path": str(credit_path),
        "audit_log": []
    }

    # Run graph
    result = graph.invoke(state)

    # -----------------------------
    # Display Results
    # -----------------------------
    st.divider()
    st.header("✅ Application Result")


    st.subheader("Decision")

    status = result.get("status")

    if status == "AUTO_APPROVE":
        st.success("🎉 Application Auto-Approved")
    elif status == "ASK_USER":
        st.warning("⚠️ Additional Information Required from Applicant")
    elif status == "HUMAN_REVIEW":
        st.error("🧑‍⚖️ Application Sent for Human Review")
    else:
        st.info(f"Status: {status}")

    if status == "ASK_USER":
        st.write("Please review the validation issues and resubmit the application with correct information.")
        st.write("**Validation Issues:**")
        for issue in result["validation_result"].get("issues", []):
            st.write("-", issue)

    if "eligibility_result" in result:
        st.metric(
            label="Eligibility Score",
            value=result["eligibility_result"]["eligibility_score"]
        )

        # -----------------------------
        # Explanation
        # -----------------------------
        if "explanation" in result["eligibility_result"]:
            st.subheader("📝 Decision Explanation")
            st.write(result["eligibility_result"]["explanation"]["summary"])

            st.markdown("**Key Factors:**")
            for factor in result["eligibility_result"]["explanation"]["key_factors"]:
                st.write("•", factor)

    # -----------------------------
    # Audit / Debug
    # -----------------------------
    with st.expander("🔍 Audit Trail"):
        for step in result["audit_log"]:
            st.write("-", step)

    with st.expander("📄 Stored Documents"):
        st.write("Bank Statement:", str(bank_path))
        st.write("Credit Report:", str(credit_path))

    # ----------------------------------------------------------------
    # Debug Section (Optional)
    # ----------------------------------------------------------------
    with st.expander("🔍 Debug: Full State Output"):
        st.json(result)
