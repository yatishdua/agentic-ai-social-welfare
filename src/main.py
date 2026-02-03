import streamlit as st

from ui.home import render_home
from ui.form_screen import render_form
from ui.chatbot_screen import render_chatbot

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
