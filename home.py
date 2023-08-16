import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="World Cup Group Simulator",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

def initialize_main_app_session_state_vars():

    # if "world_cup_data_image" not in st.session_state:
    #     st.session_state.world_cup_data_image = pd.read_csv("data/CountryImageData.csv")
    #     st.session_state.world_cup_data_image = st.session_state.world_cup_data_image.set_index('Team Name')
    x = 1
