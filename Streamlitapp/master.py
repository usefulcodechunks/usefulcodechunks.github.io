import streamlit as st
import pandas as pd

from nodehelperfunctions import run_sub_node_app
from duedillgence import due_dill_app




def initialize_session_state_vars():
    if 'cycle' not in st.session_state:
        st.session_state.cycle = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'node_app_cache' not in st.session_state:
        st.session_state.node_app_cache = {}





def render_sidebar(sidebar_object):
    with sidebar_object.expander("Page navigation"):
        selected_page = st.selectbox('Select a page', ["Home", "Node App", "Due diligence"])
        st.session_state.current_page = selected_page

def render_page(main_page_object):

    if(main_page_object.session_state.current_page == "Home"):
        main_page_object.title(main_page_object.session_state.current_page)

    elif(main_page_object.session_state.current_page == "Node App"):
        main_page_object.title(main_page_object.session_state.current_page)
        run_sub_node_app()

    elif(main_page_object.session_state.current_page == "Due diligence"):
        main_page_object.title(main_page_object.session_state.current_page)
        due_dill_app(main_page_object)

    else:
        main_page_object.title("404 No Page Found")

render_sidebar(st.sidebar)
render_page(st)
