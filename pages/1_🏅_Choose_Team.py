import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Choose a group",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title("How can my team make out of the group stage?")

def get_group_for_team(team_name):
    temp_df = st.session_state.world_cup_data[st.session_state.world_cup_data.RoundNumber <= 3]
    temp_df = temp_df[temp_df.HomeTeam == team_name]
    groups = list(temp_df.Group.unique())

    return groups[0]

def determine_winner(row_of_df):
    if(not row_of_df['PlayedMatch']): # GAME HAS ALREADY BEEN PLAYED

        if(row_of_df["HomeTeamScore"] == row_of_df["AwayTeamScore"]):
            return "Tie"
        elif(row_of_df["HomeTeamScore"] > row_of_df["AwayTeamScore"]):
            return row_of_df["HomeTeam"]
        elif(row_of_df["HomeTeamScore"] < row_of_df["AwayTeamScore"]):
            return row_of_df["AwayTeam"]

def build_records_dict(filtered_df):
    records_dict = {}
    for index, row in filtered_df.iterrows():
        if(row["HomeTeam"] not in records_dict.keys()):
            records_dict[row["HomeTeam"]] = {"points" : 0, "goals_for" : 0 , "goals_against" : 0, "Group" : row["Group"]}
        if(row["AwayTeam"] not in records_dict.keys()):
            records_dict[row["AwayTeam"]] = {"points" : 0, "goals_for" : 0 , "goals_against" : 0, "Group" : row["Group"]}

        if(not row['PlayedMatch']):
            winner = determine_winner(row)

            if(winner == "Tie"):
                records_dict[row["HomeTeam"]]["points"] += 1
                records_dict[row["AwayTeam"]]["points"] += 1
            else:
                records_dict[winner]["points"] += 3

            records_dict[row["HomeTeam"]]["goals_for"] += row["HomeTeamScore"]
            records_dict[row["HomeTeam"]]["goals_against"] += row["AwayTeamScore"]

            records_dict[row["AwayTeam"]]["goals_for"] += row["AwayTeamScore"]
            records_dict[row["AwayTeam"]]["goals_against"] += row["HomeTeamScore"]

    return records_dict

def determine_top_two_winners(df_of_data):
    df_of_data["goal_diffrential"] = df_of_data["goals_for"] - df_of_data["goals_against"]
    warning_string_message = None
    unique_points_score = len(df_of_data.points.unique())
    if(unique_points_score <= 3):
        tie_breaker = True


    df_of_data = df_of_data.sort_values(by=['goals_for'], ascending=False)
    df_of_data = df_of_data.sort_values(by=['goal_diffrential'], ascending=False)
    df_of_data = df_of_data.sort_values(by=['points'], ascending=False)

    return df_of_data

group_stages_only_df = st.session_state.world_cup_data[st.session_state.world_cup_data.RoundNumber <= 3]


selected_team = st.selectbox("Pick a Team",group_stages_only_df.HomeTeam.unique())

selected_teams_group = get_group_for_team(selected_team)

group_stages_only_df = group_stages_only_df[group_stages_only_df.Group == selected_teams_group]

records_dict = build_records_dict(group_stages_only_df)
df_of_records = pd.DataFrame.from_dict(records_dict, orient='index')

winners = determine_top_two_winners(df_of_records)

st.write(winners)

for index, row in group_stages_only_df[group_stages_only_df.PlayedMatch == True].iterrows():

    st.write(row)
