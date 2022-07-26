import streamlit as st
import pandas as pd

# CONFIG IMPORTS
from config import render_sidebar, initialize_session_state_vars

# view imports
from views.nodeapp import render_node_app
from views.duedillgence import due_dill_app
from views.home import default_home_view


def list_of_pages_to_function():
    pages = {}
    pages["Home"] = default_home_view
    pages["Node App"] = render_node_app
    pages["Due Diligence"] = due_dill_app
    st.session_state.pages_to_functions = pages

def render_page(render_object):
    try:
        selected_page = render_object.session_state.current_page
        render_object.title(selected_page)
        function_to_call = render_object.session_state.pages_to_functions[selected_page]
        function_to_call(render_object)
    except KeyError:
        render_object.error("No Page Found for {0}".format(render_object.session_state.current_page))

# Intitilize the Session Variables Needed for the master app (set in config/__init__.py)
initialize_session_state_vars()
# Sets the pages to function call in session state
list_of_pages_to_function()
# Renders the needed sidebar controls for page navigation
render_sidebar(st.sidebar)
# Renders the selected page
render_page(st)
