import streamlit as st

from ui.home import render_home
from ui.form_screen import render_form
from ui.chatbot_screen import render_chatbot
from ui.chatbot_manager_screen import render_chatbot_manager


from rag.policy_loader import load_policy_rag

@st.cache_resource
def load_policy_rag_():
    return load_policy_rag()

policy_vectorstore = load_policy_rag_()
# policy_vectorstore = None

st.set_page_config(
    page_title="Social Welfare Assistant",
    layout="centered"
)

if "screen" not in st.session_state:
    st.session_state.screen = "home"

if st.session_state.screen == "home":
    render_home()

elif st.session_state.screen == "chatbot":
    render_chatbot()

elif st.session_state.screen == "form":
    render_form()

elif st.session_state.screen == "chatbot_llm":
    render_chatbot_manager(policy_vectorstore)

