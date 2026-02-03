import os
import uuid
import streamlit as st

import sys
from pathlib import Path

# Add project root to PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from chatbot.intent import detect_intent
from chatbot.criteria import get_static_eligibility_criteria
from chatbot.intake import REQUIRED_FIELDS, QUESTIONS
from chatbot.adapter import build_application_state_from_chat
from chatbot.normalizer import normalize_chat_ui_data

from src.agents.langgraph.graph import build_application_graph  # ✅ EXISTING GRAPH


UPLOAD_DIR = "data/uploads"


def save_file_to_applicant_folder(uploaded_file, emirates_id, filename):
    folder = os.path.join(UPLOAD_DIR, emirates_id)
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return path

def render_chatbot():


    # -----------------------------
    # Build graph once
    # -----------------------------
    @st.cache_resource
    def load_graph():
        return build_application_graph()

    graph = load_graph()

    # -------------------------------
    # Navigation
    # -------------------------------
    if st.button("⬅ Back to Home"):
        st.session_state.screen = "home"
        st.rerun()

    st.title("🤖 Economic Welfare Assistant")

    # -------------------------------
    # Init chat messages
    # -------------------------------
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello 👋 I’m your **Economic Welfare Assistant**.\n\n"
                    "I can help you:\n"
                    "1️⃣ Apply for economic welfare\n"
                    "2️⃣ Know eligibility criteria\n\n"
                    "What would you like to do?"
                )
            }
        ]

    # -------------------------------
    # Init chatbot state
    # -------------------------------
    if "chat_state" not in st.session_state:
        st.session_state.chat_state = {
            "intent": None,
            "ui_data": {},
            "current_field": None,

            "bank_statement_path": None,
            "credit_report_path": None,
            "emirates_id_path": None,

            "awaiting_bank": False,
            "awaiting_credit": False,
            "awaiting_emirates_id": False,
            "graph_invoked": False,
        }

    # -------------------------------
    # Render chat history
    # -------------------------------
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -------------------------------
    # Bank statement upload
    # -------------------------------
    if st.session_state.chat_state["awaiting_bank"]:
        bank_file = st.file_uploader(
            "Upload Bank Statement (PDF only)",
            type=["pdf"],
            key="bank_upload",
        )

        if bank_file:
            emirates_id = st.session_state.chat_state["ui_data"]["emirates_id"]
            path = save_file_to_applicant_folder(
                bank_file, emirates_id, "bank_statement.pdf"
            )

            st.session_state.chat_state["bank_statement_path"] = path
            st.session_state.chat_state["awaiting_bank"] = False
            st.session_state.chat_state["awaiting_credit"] = True

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": "✅ Bank statement uploaded. Please upload your credit report."
                }
            )
            st.rerun()

    # -------------------------------
    # Credit report upload
    # -------------------------------
    if st.session_state.chat_state["awaiting_credit"]:
        credit_file = st.file_uploader(
            "Upload Credit Report (PDF only)",
            type=["pdf"],
            key="credit_upload",
        )

        if credit_file:
            emirates_id = st.session_state.chat_state["ui_data"]["emirates_id"]
            path = save_file_to_applicant_folder(
                credit_file, emirates_id, "credit_report.pdf"
            )

            st.session_state.chat_state["credit_report_path"] = path
            st.session_state.chat_state["awaiting_credit"] = False
            st.session_state.chat_state["awaiting_emirates_id"] = True

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": "✅ Credit report uploaded. Please upload your Emirates ID."
                }
            )
            st.rerun()

    # -------------------------------
    # Emiratee ID upload
    # -------------------------------
    if st.session_state.chat_state["awaiting_emirates_id"]:
        emirates_file = st.file_uploader(
            "Upload Emirates ID (Image only)",
            type=["png", "jpg", "jpeg"],
            key="emirates_upload",
        )

        if emirates_file:
            emirates_id = st.session_state.chat_state["ui_data"]["emirates_id"]
            path = save_file_to_applicant_folder(
                emirates_file, emirates_id, "emirates_id.jpg"
            )

            st.session_state.chat_state["emirates_id_path"] = path
            st.session_state.chat_state["awaiting_emirates_id"] = False

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": "✅ Emirates ID uploaded. Assessing eligibility now..."
                }
            )
            st.rerun()

    # -------------------------------
    # Invoke application graph
    # -------------------------------
    if (
        st.session_state.chat_state["bank_statement_path"]
        and st.session_state.chat_state["credit_report_path"]
        and st.session_state.chat_state["emirates_id_path"]
        and not st.session_state.chat_state["graph_invoked"]
    ):
        raw_ui_data = st.session_state.chat_state["ui_data"]

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": f"### raw_ui_data\n\n{raw_ui_data}"
            }
        )

        normalized_ui_data = normalize_chat_ui_data(raw_ui_data)

        app_state = build_application_state_from_chat(
            ui_data=normalized_ui_data,
            intent="APPLY_WELFARE",
        )

        app_state["bank_statement_path"] = st.session_state.chat_state["bank_statement_path"]
        app_state["credit_report_path"] = st.session_state.chat_state["credit_report_path"]
        app_state["emirates_id_image_path"] = st.session_state.chat_state["emirates_id_path"]

        result = graph.invoke(app_state)

        st.session_state.chat_state["graph_invoked"] = True

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": f"### Eligibility Result\n\n{result.get('eligibility_result')}"
            }
        )

        reommendation=[]
        for r in result["enablement_recommendations"]["recommendations"]:
                        reommendation.append(r["message"])

        
        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": f"### Enablement Recommendations\n\n{'\n\n'.join(reommendation)}"
            }
        )
        st.rerun()

    # -------------------------------
    # User input
    # -------------------------------
    user_input = st.chat_input("Type your response here...")

    if not user_input:
        return

    st.session_state.chat_messages.append(
        {"role": "user", "content": user_input}
    )

    # -------------------------------
    # Handle previous question answer
    # -------------------------------
    current_field = st.session_state.chat_state["current_field"]
    if current_field:
        st.session_state.chat_state["ui_data"][current_field] = user_input
        st.session_state.chat_state["current_field"] = None

    # -------------------------------
    # Intent detection
    # -------------------------------
    if not st.session_state.chat_state["intent"]:
        intent = detect_intent(user_input)
        st.session_state.chat_state["intent"] = intent

        if intent == "KNOW_CRITERIA":
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": get_static_eligibility_criteria()
                }
            )
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": "Would you like to apply for economic welfare?"
                }
            )
            st.rerun()

    # -------------------------------
    # Only APPLY flow continues
    # -------------------------------
    if st.session_state.chat_state["intent"] != "APPLY_WELFARE":
        st.rerun()

    ui_data = st.session_state.chat_state["ui_data"]

    # -------------------------------
    # Ask next missing field
    # -------------------------------
    for field in REQUIRED_FIELDS:
        if field not in ui_data:
            st.session_state.chat_state["current_field"] = field
            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": QUESTIONS[field]
                }
            )
            st.rerun()

    # -------------------------------
    # All fields collected → start upload
    # -------------------------------
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": (
                "✅ I’ve collected all required information.\n\n"
                "Please upload your **bank statement** to continue."
            )
        }
    )
    st.session_state.chat_state["awaiting_bank"] = True
    st.rerun()