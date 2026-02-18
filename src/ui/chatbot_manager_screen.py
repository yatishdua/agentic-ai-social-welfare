import streamlit as st
from chatbot_manager.validator import validate_user_message
from chatbot_manager.intake_llm import run_intake
from chatbot_manager.manager import handle_turn
import os
from src.agents.langgraph.graph import build_application_graph
from chatbot.adapter import build_application_state_from_chat
from chatbot.normalizer import normalize_chat_ui_data

import uuid

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


def render_chatbot_manager(policy_vectorstore=None):
    st.title("🤖 Economic Welfare Assistant")

    # -----------------------------
    # Build graph once
    # -----------------------------
    @st.cache_resource
    def load_graph():
        return build_application_graph()

    graph = load_graph()

    if "state" in st.session_state:
        st.write("DEBUG PHASE:", st.session_state.state)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello 👋 I’m your Economic Welfare Assistant.\n"
                    "I can help you apply or explain eligibility.\n"
                    "How can I help?"
                )
            }
        ]

    if "state" not in st.session_state:
        st.session_state.state = {
            "mode": None,
            "phase": None,
            "ui_data": {},
            "confirm_submit": None,
            "bank_statement_path": None,
            "credit_report_path": None,
            "emirates_id_path": None,
            "audit_log": [],
        }

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    state = st.session_state.state

    # ---------- DOCUMENT UPLOAD ----------
    if state["phase"] == "UPLOAD":
        st.subheader("Upload Documents")

        bank = st.file_uploader("Bank Statement (PDF)", type=["pdf"])
        credit = st.file_uploader("Credit Report (PDF)", type=["pdf"])
        emirates_file = st.file_uploader(
            "Upload Emirates ID (Image only)",
            type=["png", "jpg", "jpeg"],
            key="emirates_upload",
        )

        if bank and credit and emirates_file:
            eid = state["ui_data"]["emirates_id"]
            base = f"data/uploads/{eid}"
            os.makedirs(base, exist_ok=True)

            bank_path = f"{base}/bank_statement.pdf"
            credit_path = f"{base}/credit_report.pdf"
            emirates_path = f"{base}/emirates_id.jpg"

            with open(bank_path, "wb") as f:
                f.write(bank.getbuffer())
            with open(credit_path, "wb") as f:
                f.write(credit.getbuffer())

            with open(emirates_path, "wb") as f:
                f.write(emirates_file.getbuffer())

            st.session_state.state["bank_statement_path"] = bank_path
            st.session_state.state["credit_report_path"] = credit_path
            st.session_state.state["emirates_id_path"] = emirates_path

            # Invoke graph
            normalized_ui_data = normalize_chat_ui_data(st.session_state.state["ui_data"])

            app_state = build_application_state_from_chat(
                ui_data=normalized_ui_data,
                intent="APPLY_WELFARE",
            )

            app_state["bank_statement_path"] = st.session_state.state["bank_statement_path"]
            app_state["credit_report_path"] = st.session_state.state["credit_report_path"]
            app_state["emirates_id_image_path"] = st.session_state.state["emirates_id_path"]

            result = graph.invoke(app_state)

            st.success("Application submitted successfully!")
            
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

            if status == "AUTO_APPROVE":
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

                    for r in result["enablement_recommendations"]["recommendations"]:
                        st.info(r["message"])

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

            state["phase"] = "DONE"


    user_input = st.chat_input("Type here…")
    if not user_input:
        return

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    sid = st.session_state.session_id

    # 1️⃣ Validate
    validation = validate_user_message(user_input,sid)

    # 2️⃣ Intake only if APPLY mode
    intake = None
    if st.session_state.state["mode"] == "APPLY":
        intake = run_intake(st.session_state.messages,sid,st.session_state.state["ui_data"])

    # 3️⃣ Manager decides
    st.session_state.state["recent_messages"] = st.session_state.messages
    response = handle_turn(
        st.session_state.state,
        validation,
        intake,
        policy_vectorstore
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    st.rerun()

    

    
