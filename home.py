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

is_mobile = st.checkbox("Check this box if you are using mobile")


# TIE BREAKDER RULES
# 1 - Goal goal_diffrential
# 2 - Goals for
# 3 - Head to Head Performance
# 4 - Goal Diff between only tied teams
# 5 - Most Goals Score Between Tied Teams
# 6 - Fair Play


def get_image_for_country(country, render_object):
    render_object.image(st.session_state.world_cup_data_image.loc[country].Emoji_Flag)

def initialize_home_session_state_vars():
    if "world_cup_data" not in st.session_state:
        st.session_state.world_cup_data = pd.read_json(WORLD_CUP_DATA)
        st.session_state.world_cup_data['DateUtc'] = pd.to_datetime(st.session_state.world_cup_data['DateUtc'])
        st.session_state.world_cup_data['PlayedMatch'] = st.session_state.world_cup_data.AwayTeamScore.isna()
    if "world_cup_data_image" not in st.session_state:
        st.session_state.world_cup_data_image = pd.read_csv("data/CountryImageData.csv")
        st.session_state.world_cup_data_image = st.session_state.world_cup_data_image.set_index('Team Name')

def get_first_two_seeds(df_of_data):

    df_of_data["goal_diffrential"] = df_of_data["goals_for"] - df_of_data["goals_against"]


    df_of_data = df_of_data.sort_values(by=['goals_for'], ascending=False)
    df_of_data = df_of_data.sort_values(by=['goal_diffrential'], ascending=False)
    df_of_data = df_of_data.sort_values(by=['points'], ascending=False)

    if(not is_mobile):
        st.header("2 - Points Table")
        st.write(df_of_data[["points", "goal_diffrential", "goals_for", "goals_against"]])

    final_two_seeds = df_of_data.index.values.tolist()[:2]

    return final_two_seeds

def game_pick_format(records_dict):
    st.info("Start by selecting a group. After selecting a group, mark the teams you expect to win or simulate a tie by checking both boxes off. All matches already played will be disabled in the simulator. ")

    selected_group = st.selectbox("Pick a group",st.session_state.world_cup_data.Group.unique())

    if(selected_group is not None):
        temp_df = st.session_state.world_cup_data[st.session_state.world_cup_data["Group"] == selected_group]


        help_str = "To simulate the team winning simply check the box for the team you expect to win. To simulate a tie check both boxes."
        unique_list_of_teams = []
        counter = 0
        st.header("1 - Game Simulation")
        if(is_mobile):
            cols = st.columns(2)
        else:
            cols = st.columns([1,2,1,1,2,1])

        for index, row in temp_df.iterrows():

            home_win_bool = False
            away_win_bool = False
            disable_bool = False
            if(row["HomeTeam"] not in unique_list_of_teams):
                unique_list_of_teams.append(row["HomeTeam"])
            if(row["AwayTeam"] not in unique_list_of_teams):
                unique_list_of_teams.append(row["AwayTeam"])


            if(row["HomeTeamScore"] > row["AwayTeamScore"]):
                home_win_bool = True
            elif(row["HomeTeamScore"] < row["AwayTeamScore"]):
                away_win_bool = True
            else:
                if(row["PlayedMatch"] == 0):
                    disable_bool = True
                    away_win_bool = True
                    home_win_bool = True
                else:
                    disable_bool = False
                    home_win_bool = False
                    away_win_bool = False

            if(row["PlayedMatch"] == 0):
                disable_bool = True
            else:
                disable_bool = False

            if(is_mobile):
                sc1 = row["HomeTeam"]+" Wins"
                sc2 = row["AwayTeam"]+" Wins"
                sc3 = row["HomeTeam"]+" Ties With "+row["AwayTeam"]

                if(home_win_bool and away_win_bool):
                    rendered_option = [sc3]
                elif(home_win_bool):
                    rendered_option = [sc1]
                elif(away_win_bool):
                    rendered_option = [sc2]
                else:
                    rendered_option = [sc1,sc2,sc3]

                dropdown_str = "Pick outcome for "+row["HomeTeam"] + " VS " + row["AwayTeam"]


                temp_game_result = st.selectbox(dropdown_str,rendered_option,disabled=disable_bool)
                if(temp_game_result == sc1):
                    temp_home_result = True
                    temp_away_result = False
                elif(temp_game_result == sc2):
                    temp_home_result = False
                    temp_away_result = True
                elif(temp_game_result == sc3):
                    temp_home_result = True
                    temp_away_result = True

            else:
                with cols[0]:
                    get_image_for_country(row["HomeTeam"],st)

                with cols[1]:
                    temp_home_result = st.checkbox(row["HomeTeam"],value=home_win_bool, disabled=disable_bool ,help=help_str, key=str(row["HomeTeam"])+str(row["MatchNumber"]))

                with cols[2]:
                    if(disable_bool):
                        st.write(int(row["HomeTeamScore"]))

                with cols[3]:
                    if(disable_bool):
                        st.write(int(row["AwayTeamScore"]))

                with cols[4]:
                    temp_away_result = st.checkbox(row["AwayTeam"],value=away_win_bool, disabled=disable_bool ,help=help_str, key=str(row["AwayTeam"])+str(row["MatchNumber"]))

                with cols[5]:
                    get_image_for_country(row["AwayTeam"],st)

            if(disable_bool):
                records_dict[row["AwayTeam"]]["goals_for"] += row["AwayTeamScore"]
                records_dict[row["AwayTeam"]]["goals_against"] += row["HomeTeamScore"]

                records_dict[row["HomeTeam"]]["goals_for"] += row["HomeTeamScore"]
                records_dict[row["HomeTeam"]]["goals_against"] += row["AwayTeamScore"]

            if(temp_home_result and temp_away_result):
                records_dict[row["AwayTeam"]]["points"] += 1
                records_dict[row["HomeTeam"]]["points"] += 1
            elif(temp_home_result):
                records_dict[row["HomeTeam"]]["points"] += 3
            elif(temp_away_result):
                records_dict[row["AwayTeam"]]["points"] += 3


            counter += 1

        final_df_for_group = pd.DataFrame.from_dict(records_dict, orient='index')
        final_df_for_group = final_df_for_group[final_df_for_group.Group == selected_group]
        final_two_seeds = get_first_two_seeds(final_df_for_group)

        if(is_mobile):
            st.header("2 - Final Results")
            st.subheader("🥇 First Seed ")
            st.write(final_two_seeds[0])
            st.subheader("🥈 Second Seed ")
            st.write(final_two_seeds[1])
        else:

            st.header("3 - Final Results")
            st.subheader("🥇 First Seed ")
            cols = st.columns(6)
            with cols[0]:
                get_image_for_country(final_two_seeds[0],st)
            with cols[1]:
                st.write(final_two_seeds[0])

            st.subheader("🥈 Second Seed ")
            cols = st.columns(6)
            with cols[0]:
                get_image_for_country(final_two_seeds[1],st)
            with cols[1]:
                st.write(final_two_seeds[1])

initialize_home_session_state_vars()


# SPLITTING UP DF INTO PLAYED VS NON PLAYED MATCHES
currently_played_matches = st.session_state.world_cup_data[st.session_state.world_cup_data.PlayedMatch == 0]
yet_to_be_played_matches = st.session_state.world_cup_data[st.session_state.world_cup_data.PlayedMatch == 1]


records_dict = {}

# MAKE STRUCUTURE FOR HOLDING INFORMATION ON EACH TEAM
for index, row in currently_played_matches.iterrows():
    if(row["HomeTeam"] not in records_dict.keys()):
        records_dict[row["HomeTeam"]] = {"points" : 0, "goals_for" : 0 , "goals_against" : 0, "Group" : row["Group"]}
    if(row["AwayTeam"] not in records_dict.keys()):
        records_dict[row["AwayTeam"]] = {"points" : 0, "goals_for" : 0 , "goals_against" : 0, "Group" : row["Group"]}

tab1, tab2, tab3 = st.tabs(["Game Simulator","Game Schedule", "Choose Team"])

with tab1:
    game_pick_format(records_dict)

with tab2:
    with st.expander("Matches Already Played"):
        for index, row in currently_played_matches.iterrows():
            template_str = "{0}: {1} {2} against {3}"
            if(row["HomeTeamScore"] > row["AwayTeamScore"]):
                join_str = "Wins"
            elif(row["HomeTeamScore"] < row["AwayTeamScore"]):
                join_str = "Loses"
            elif(row["HomeTeamScore"] == row["AwayTeamScore"]):
                join_str = "Ties"

            template_str = template_str.format(row["Group"], row["HomeTeam"],join_str,row["AwayTeam"])
            st.write(template_str)

    with st.expander("Matches Still Yet to happen"):
        for index, row in yet_to_be_played_matches.iterrows():
            st.write(row["HomeTeam"]," VS ",row["AwayTeam"]," :",row["DateUtc"])


with tab3:
    st.info("Coming soon")
