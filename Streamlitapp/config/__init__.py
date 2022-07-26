import streamlit as st



def initialize_session_state_vars():
    if 'cycle' not in st.session_state:
        st.session_state.cycle = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

def render_sidebar(sidebar_object):
    with sidebar_object.expander("Page navigation"):
        selected_page = st.selectbox('Select a page', st.session_state.pages_to_functions.keys())
        st.session_state.current_page = selected_page
