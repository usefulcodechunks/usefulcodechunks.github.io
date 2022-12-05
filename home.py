import streamlit as st
import pandas as pd
import urllib.request, json
from datetime import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

WORLD_CUP_DATA = "http://fixturedownload.com/feed/json/fifa-world-cup-2022"

st.set_page_config(
    page_title="World Cup Group Simulator",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)


def initialize_home_session_state_vars():
    if "world_cup_data" not in st.session_state:
        st.session_state.world_cup_data = pd.read_json(WORLD_CUP_DATA)
        st.session_state.world_cup_data['DateUtc'] = pd.to_datetime(st.session_state.world_cup_data['DateUtc'])
        st.session_state.world_cup_data['PlayedMatch'] = st.session_state.world_cup_data.AwayTeamScore.isna()
    if "world_cup_data_image" not in st.session_state:
        st.session_state.world_cup_data_image = pd.read_csv("data/CountryImageData.csv")
        st.session_state.world_cup_data_image = st.session_state.world_cup_data_image.set_index('Team Name')


initialize_home_session_state_vars()

# TIE BREAKDER RULES
# 1 - Goal goal_diffrential
# 2 - Goals for
# 3 - Head to Head Performance
# 4 - Goal Diff between only tied teams
# 5 - Most Goals Score Between Tied Teams
# 6 - Fair Play
