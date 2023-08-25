import streamlit as st
import numpy as np
import pandas as pd
import os
import time 


# Formula 1 Data Imports
import fastf1
import fastf1.plotting

#PLOTTING 
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


if "iteration" not in st.session_state:
    st.session_state["iteration"] = 0

st.session_state["iteration"] += 1
print("===========================================================")
print("===========================================================")
print("===========================================================")
print("===========================================================")
print(st.session_state["iteration"])
print("===========================================================")
print("===========================================================")
print("===========================================================")
print("===========================================================")
print("===========================================================")
print("===========================================================")
print("===========================================================")



if "cache" not in st.session_state:
    print("LOADING DATA")
    session = fastf1.get_session(2022, "Barcelona", 'R')
    session.load()
    laps = session.laps
    print("ADDING TO CACHE")
    st.session_state["cache"] = laps
    st.session_state["telemetry"] = {}

    print("DONE ADDING TO CACHE + TELEMETRY")


DRIVER_NAME_DICT = {'ALB': 'alexander albon', 'ALO': 'fernando alonso', 'BOT': 'valtteri bottas', 
                   'DEV': 'nyck de vries', 'DRU': 'felipe drugovich', 'GAS': 'pierre gasly', 
                   'HAM': 'lewis hamilton', 'HUL': 'nico hulkenberg', 'LEC': 'charles leclerc', 
                   'MAG': 'kevin magnussen', 'NOR': 'lando norris', 'OCO': 'esteban ocon', 'PER': 'sergio perez', 
                   'PIA': 'oscar piastri', 'RIC': 'daniel ricciardo', 'RUS': 'george russell', 'SAI': 'carlos sainz', 
                   'SAR': 'logan sargeant', 'STR': 'lance stroll', 'TSU': 'yuki tsunoda', 'VER': 'max verstappen', 
                   'ZHO': 'zhou guanyu'}
DRIVER_COLOR_DICT = {'alexander albon': '#005aff', 'carlos sainz': '#ff8181', 'charles leclerc': '#dc0000', 
              'daniel ricciardo': '#2b4562', 'esteban ocon': '#70c2ff', 'felipe drugovich': '#2f9b90', 
              'fernando alonso': '#006f62', 'george russell': '#24ffff', 'kevin magnussen': '#ffffff', 
              'lance stroll': '#25a617', 'lando norris': '#eeb370', 'lewis hamilton': '#00d2be', 'logan sargeant': '#012564', 
              'max verstappen': '#0600ef', 'nico hulkenberg': '#cacaca', 'nyck de vries': '#1e3d61', 'oscar piastri': '#ff8700', 
              'pierre gasly': '#0090ff', 'sergio perez': '#716de2', 'valtteri bottas': '#900000', 'yuki tsunoda': '#356cac', 
              'zhou guanyu': '#500000'}







# LOADING THE DATA FROM THE CACHE
laps = st.session_state["cache"]
# LOADING A DRIVERS LIST
drivers_list = laps['Driver'].unique().tolist()

# GETTING THE 1st DRIVER
selected_driver = drivers_list[0]

# IF DRIVER DATA NOT LOADED
if selected_driver not in st.session_state["telemetry"]:
    pick_first = laps.pick_driver(selected_driver)
    st.session_state["telemetry"][selected_driver] = pick_first.get_telemetry()
    st.session_state["telemetry"][selected_driver]["SessionTimeNum"] = st.session_state["telemetry"][selected_driver]["SessionTime"].dt.total_seconds()

print(st.session_state["cache"])
print(st.session_state["telemetry"])



# print("Max Session: ",max(tel_first["SessionTimeNum"]))
# print("Min Session: ",min(tel_first["SessionTimeNum"]))
# print("Unique Drivers: ",list(tel_first["Driver"].unique()))
# print("Min Session: ",min(tel_first["SessionTimeNum"]))




# # DATA TRANSFROMATIONS
# # -- CONVERTING LAPSTARTTIME TO NUM TO USE
# pick_first["LapStartTimeNum"] = pick_first["LapStartTime"].dt.total_seconds()












# tel_first_head = tel_first.head(0)
# df = pd.DataFrame(tel_first_head)       # FORMATTING FROM DUMMY DF
# df["Driver"] = selected_driver

# #ITERATE FROM HERE
# dfi = pd.DataFrame(tel_first)
# dfi["Driver"] = selected_driver
# print("HEREEEEE")
# print(dfi["Driver"])
# dfi['colors'] = dfi['Driver'].apply(lambda x: DRIVER_COLOR_DICT[DRIVER_NAME_DICT[x]])


# df = df.append(dfi)

# #######################################################
# # print("OLD LENGHT ",len(df))
# # df["SessionTimeNum"] = df["SessionTime"].dt.total_seconds()
# # df = df.head(200)

# # print("NEW ROWS ",len(df))
# # print(df.columns)

# # fig = px.scatter(df, x="X", y="Y", animation_frame="SessionTimeNum", animation_group="Driver",
# #             color="Driver", hover_name="Driver",
# #            range_x=[min(df["X"]), max(df["X"])], range_y=[min(df["Y"]), max(df["Y"])])
# # fig.add_traces(px.line(x=df["X"], y=df["Y"], color_discrete_sequence=["grey"]).data)
# # fig.update_layout(transition = {'duration': .001})

# ####################################
# df = df.head(100)




# # Create figure

# fig = go.Figure(
#     data=[go.Scatter(x=df["X"], y=df["Y"],
#                      mode="lines",
#                      line=dict(width=2, color="blue")),
#           go.Scatter(x=df["X"], y=df["Y"],
#                      mode="lines",
#                      line=dict(width=2, color="blue"))],
#     layout=go.Layout(
#         xaxis=dict(range=[min(df["X"]), max(df["X"])], autorange=False, zeroline=False),
#         yaxis=dict(range=[min(df["Y"]), max(df["Y"])], autorange=False, zeroline=False),
#         title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
#         updatemenus=[dict(type="buttons",
#                           buttons=[dict(label="Play",
#                                         method="animate",
#                                         args=[None, {"frame": {"duration": 20, "redraw": False},}])])]
#     ),
#     frames=[go.Frame(
#         data=[go.Scatter(
#             name=str("Lap"+str(df["SessionTimeNum"][k])),
#             x=[df["X"][k]],
#             y=[df["Y"][k]],
#             hovertext  = [df["Driver"][k]],
#             mode="markers",
#             marker_color = [df["colors"][k]]
#             )]) #marker=dict(color="red", size=10)

#         for k in range(2,2+len(df))]
# )




# # fig.show()
# st.plotly_chart(fig, theme="streamlit",use_container_width=True)

# # for i in drivers_list:
# pick_driver = laps.pick_driver(i)
# tel = pick_driver.get_telemetry()
# tel['DriverNumber'] = i
# dfi = pd.DataFrame(tel)
# df = df.append(dfi)
    
# print(df)