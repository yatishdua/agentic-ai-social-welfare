import streamlit as st

def render_chatbot():
    # Back navigation
    if st.button("⬅ Back to Home"):
        st.session_state.screen = "home"
        st.rerun()

    st.title("🤖 Social Welfare Chat Assistant")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! I am your Social Welfare Assistant 🤖\n\n"
                    "How can I help you today?\n\n"
                    "1️⃣ Apply for Economic Welfare\n"
                    "2️⃣ Know Eligibility Criteria\n\n"
                    "Please type **1** or **2**."
                )
            }
        ]

    # Display chat messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your response here...")

    if user_input:
        # Add user message
        st.session_state.chat_messages.append(
            {"role": "user", "content": user_input}
        )

        # Temporary placeholder logic (no LangGraph yet)
        if user_input.strip() == "1":
            assistant_reply = (
                "✅ You selected **Apply for Economic Welfare**.\n\n"
                "I will guide you through the application step by step."
            )
        elif user_input.strip() == "2":
            assistant_reply = (
                "📘 You selected **Know Eligibility Criteria**.\n\n"
                "I can explain eligibility rules for welfare schemes."
            )
        else:
            assistant_reply = (
                "❗ Please type **1** or **2** to continue."
            )

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        st.rerun()
