import streamlit as st

from ui.home import render_home

# Placeholder imports (we'll implement next)
# from ui.chatbot_screen import render_chatbot
# from ui.form_screen import render_form

st.set_page_config(
    page_title="Social Welfare Assistant",
    layout="centered"
)

if "screen" not in st.session_state:
    st.session_state.screen = "home"

if st.session_state.screen == "home":
    render_home()

elif st.session_state.screen == "chatbot":
    st.title("🤖 Chatbot Screen (Coming Next)")
    st.info("Chatbot UI will be implemented next.")

elif st.session_state.screen == "form":
    st.title("📝 Form Screen (Existing Logic)")
    st.info("Existing form flow will be wired here.")
