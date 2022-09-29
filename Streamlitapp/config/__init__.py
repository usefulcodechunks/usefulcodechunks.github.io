import streamlit as st



def initialize_session_state_vars():
    if 'cycle' not in st.session_state:
        st.session_state.cycle = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
