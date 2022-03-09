import streamlit as st
import pandas as pd








def initialize_session_state_vars():

    if 'cycle' not in st.session_state:
        st.session_state.cycle = 0
    if 'change_log' not in st.session_state:
        st.session_state.change_log = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'cache' not in st.session_state:
        st.session_state.cache = {}

# def render_page():
#     # ROUTING FUNCTION ========================
#     if(st.session_state.current_page == "Home"):
#         home()
#     elif(st.session_state.current_page == "User Navigation Logs"):
#         nav_search_logs()
#     elif(st.session_state.current_page == "Custom Scripts"):
#         custom_scripts()
#     else:
#         st.error("NO PAGE FOUND")




initialize_session_state_vars()



st.title("Example Code")
