import streamlit as st


def render_home():
    st.title("🏛️ Social Welfare Assistant")

    st.markdown(
        """
        Welcome to the **AI-powered Social Welfare Eligibility System**.

        You can apply for welfare benefits in two ways:
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Chat with Assistant")
        st.write(
            "Have a conversation with our AI assistant. "
            "Best if you prefer guided, step-by-step help."
        )
        if st.button("Start Chat"):
            st.session_state.screen = "chatbot"

    with col2:
        st.subheader("📝 Apply via Form")
        st.write(
            "Fill out a structured form and upload documents directly. "
            "Best if you already know the details."
        )
        if st.button("Apply via Form"):
            st.session_state.screen = "form"

    st.markdown("---")

    st.caption(
        "Both options use the same eligibility engine and policy rules."
    )
