import streamlit as st
import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.ui.app import run_form_app

def render_form():

    if st.button("⬅ Back to Home"):
        st.session_state.screen = "home"
        st.rerun()

    st.title("📝 Welfare Application Form")

    st.caption(
        "This form uses the same eligibility engine and validation logic "
        "as the chatbot-based flow."
    )

    st.markdown("---")

    # 👇 EXISTING FORM WILL BE CALLED HERE
    run_form_app()
    
