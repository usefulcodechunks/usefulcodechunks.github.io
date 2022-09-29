import streamlit as st
import pandas as pd

# CONFIG IMPORTS
from config import initialize_session_state_vars

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Home Page")
