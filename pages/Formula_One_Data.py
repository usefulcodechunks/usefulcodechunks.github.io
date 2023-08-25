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


current_path = os.getcwd()

st.set_page_config(
    page_title="Formula 1 Data App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Formula 1 Data Viewer")

TEAM_COLORS ={'Alfa Romeo': '#900000', 'AlphaTauri': '#2b4562', 'Alpine': '#0090ff', 'Aston Martin': '#006f62', 
            'Ferrari': '#dc0000', 'Haas F1 Team': 'grey', 'McLaren': '#ff8700', 'Mercedes': '#00d2be', 'Red Bull Racing': '#0600ef', 
            'Williams': '#005aff'}

def declare_session_states():
    if "cache" not in st.session_state:
        st.session_state.cache = {}
    if "loaded" not in st.session_state:
        st.session_state.loaded = False
    if "iteration" not in st.session_state:
        st.session_state.iteration = 0

declare_session_states()

def side_bar_cache_display():
    st.sidebar.title("Loaded Data Cache")
    for key in st.session_state.cache:
        st.sidebar.write(key," : ",st.session_state.cache[key])

def lap_deviation_for_session_chart(session_laps,render_object=st):
    # DATA FOR DOT PLOT

    filter_session_laps = session_laps[session_laps.Driver.isin(st.session_state.cache["drivers"])]


    drivers = list(filter_session_laps.Driver.unique())*3
    drivers.sort()
    minmaxes_str = (["fast","avg","slow"]*len(filter_session_laps.Driver.unique()))
    minmaxes_laptimes = []
    id_order = []
    seen = []
    for driver in drivers:
        if(driver not in seen):
            temp_df = filter_session_laps.pick_driver(driver)
        
            quantiles_for_driver = temp_df.LapTime.dt.total_seconds().quantile([.25,.50,.75])
            minmaxes_laptimes += [quantiles_for_driver[.25],quantiles_for_driver[.50],quantiles_for_driver[.75]]
            id_order += [2,1,3]
            seen.append(driver)


    df = pd.DataFrame([])
    df["drivers"] = drivers
    df["minmaxtype"] = minmaxes_str
    df["laptime"] = minmaxes_laptimes
    df["id_order"] = id_order

    df.sort_values(["id_order", "laptime"], ascending=True, inplace=True)    

    #lowess', 'rolling', 'ewm', 'expanding', 'ols']
    fig = px.scatter(df, x="laptime", y="drivers", color="minmaxtype",
                    title="Lap Time Curve",color_discrete_map={"fast": 'green',"avg": 'orange',"slow": 'red'}
                    )
    
    race_data = st.session_state["cache"]["Session"].results
    temp_order = df["drivers"].unique()
    print(temp_order)

    for driver in temp_order:
        color_temp = TEAM_COLORS[list(race_data[race_data["Abbreviation"]==driver]["TeamName"].unique())[0]]

        y_val = list(temp_order).index(driver)

        temp_df = df[df["drivers"]==driver]
        temp_dict = temp_df.to_dict('index')
        temp_res = {"fast" : None , "avg" : None, "slow" : None}
        # render_object.write(temp_dict)
        for key in temp_dict:
            temp_res[temp_dict[key]["minmaxtype"]] = temp_dict[key]["laptime"]

        fig.add_shape(type="line",
                        x0=temp_res["slow"], 
                        y0=y_val, 
                        x1=temp_res["fast"], 
                        y1=y_val, line_color=color_temp,opacity=.5)



        
    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)

def driver_avg_diff_chart(session_laps,render_object):

    filter_session_laps = session_laps[session_laps.Driver.isin(st.session_state.cache["drivers"])]

    avg_lap_all = session_laps.LapTime.dt.total_seconds().mean()
    avg_laptimes = filter_session_laps.groupby('Driver')['LapTime'].apply(lambda x: x.dt.total_seconds().mean())
    avg_laptimes = avg_laptimes - avg_lap_all

    
    df = pd.DataFrame([])
    df["Drivers"] = avg_laptimes.index
    df["Lap Delta"] = list(avg_laptimes)
    df["SlowerOnAvg"] = df["Lap Delta"] >= 0

    df = df.sort_values('Lap Delta',ascending=False)


    fig = px.bar(df, title="Avg Delta Pace", x="Lap Delta", y="Drivers", color="SlowerOnAvg", orientation='h',color_discrete_map={False: 'green',True: 'red'})
    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)

def animated_gap_chart(render_object):

    session_laps = st.session_state.cache["SessionLaps"]

    filter_session_laps = session_laps[session_laps.Driver.isin(st.session_state.cache["drivers"])]
    filter_session_laps["LapTimeNum"] = filter_session_laps.LapTime.dt.total_seconds()
    filter_session_laps["TotalLapTimeNum"] = filter_session_laps.Time.dt.total_seconds()

    filter_session_laps['running_total'] = filter_session_laps.groupby('Driver')['LapTimeNum'].cumsum()
    # filter_session_laps = filter_session_laps.dropna(subset=['LapTimeNum'])
    filter_session_laps = filter_session_laps.sort_values(['LapNumber'])

    df = px.data.gapminder()
    tabs = render_object.tabs(["Gap to First","Gap to Front"])
    with tabs[0]:
        fig1 = px.scatter(filter_session_laps, x="position_end", y="gap_to_first", animation_frame="LapNumber", animation_group="Driver",
                        color="Team", hover_name="Driver",
                        range_x=[-1,21], color_discrete_map=TEAM_COLORS,
                        range_y=[min(filter_session_laps['gap_to_first']),max(filter_session_laps['gap_to_first'])])
        st.plotly_chart(fig1, theme="streamlit",use_container_width=True)

    with tabs[1]:
        fig2 = px.scatter(filter_session_laps, x="position_end", y="gap_to_front", animation_frame="LapNumber", animation_group="Driver",
                        color="Team", hover_name="Driver",
                        range_x=[-1,21], color_discrete_map=TEAM_COLORS,
                        range_y=[min(filter_session_laps['gap_to_front']),max(filter_session_laps['gap_to_front'])])


        st.plotly_chart(fig2, theme="streamlit",use_container_width=True)

def drivers_laptimes(session_laps,render_object):

    filter_session_laps = session_laps[session_laps.Driver.isin(st.session_state.cache["drivers"])]
    avg_laptimes = session_laps.groupby('LapNumber')['LapTime'].apply(lambda x: x.dt.total_seconds().mean())

    filter_session_laps["LapTimeNum"] = filter_session_laps.LapTime.dt.total_seconds()
    filter_session_laps["Avg Delta"] = filter_session_laps["LapTimeNum"] - avg_laptimes.iloc[:len(filter_session_laps.LapNumber)]
    filter_session_laps['Avg Deltapositive_column'] = filter_session_laps['Avg Delta'].apply(lambda x: x if x > 0 else 0)
    filter_session_laps['Avg Deltanegative_column'] = filter_session_laps['Avg Delta'].apply(lambda x: x if x < 0 else 0)

    filter_session_laps["avg_laptimes"] = avg_laptimes
    filter_session_laps['running_total'] = filter_session_laps.groupby('Driver')['LapTimeNum'].cumsum()

    subfig = make_subplots(specs=[[{"secondary_y": True}]],x_title="Driver Lap Times")
    subfig2 = make_subplots(specs=[[{"secondary_y": True}]],x_title="Driver Lap Times")

    tabs = render_object.tabs(["Lap Times","Delta Pace"])

    with tabs[0]:
        # ,error_y="Avg Deltapositive_column",error_y_minus="Avg Deltanegative_column"
        fig = px.line(filter_session_laps,x="LapNumber",y="LapTimeNum",color="Driver")
        # fig = px.line(filter_session_laps,x="LapNumber",y="running_total",color="Driver")

        # fig = px.line(filter_session_laps,x="LapNumber",y="avg_laptimes")



        # fig = px.line(temp_data[(temp_data.Type != "tire life") & (temp_data.Type != "pace delta")], x="LapNumber", y="Datav",color="Type",line_dash ="Type")
        # fig2 = px.line(temp_data[temp_data.Type == "tire life"], x="LapNumber", y="Datav",color="Type",line_dash ="Type")
        # fig2.update_traces(yaxis="y2")
        # subfig.add_traces(fig.data + fig2.data)
        # subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        st.plotly_chart(fig, theme="streamlit",use_container_width=True)
    # with tabs[1]:
    #     fig3 = px.line(temp_data[temp_data.Type == "pace delta"], x="LapNumber", y="Datav",color="Positive",line_dash ="Type")
    #     fig4 = px.line(temp_data[temp_data.Type == "tire life"], x="LapNumber", y="Datav",line_dash ="Type")
    #     fig4.update_traces(yaxis="y2")
    #     subfig2.add_traces(fig3.data + fig4.data)
    #     subfig2.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    #     st.plotly_chart(subfig2, theme="streamlit",use_container_width=True)

def position_change_chart(session_results,render_object):

    df = session_results
    df = df[df.Abbreviation.isin(st.session_state.cache["drivers"])]


    df = df.sort_values('Position')
    df['colors'] = df['TeamName'].map(TEAM_COLORS)

    symbols = ['triangle-left', 'circle-dot', 'square', 'circle']

    fig = px.scatter(df, x="Position", y="Abbreviation", color="TeamName",symbol_sequence = symbols,
                    title="Lap Time Curve",color_discrete_map=TEAM_COLORS)

    fig.add_trace(go.Scatter(x=df["GridPosition"],y=df["Abbreviation"],mode="markers",
                             marker=dict(color="white", size=4)))
    

    temp_order = df["Abbreviation"].unique()
    print(df["TeamName"].unique())
    print(temp_order)

    print(df[["DriverNumber","Abbreviation","Position","GridPosition"]])



    ref_drivers = []
    for team_i in list(df["TeamName"].unique()):
        filter_df = df[df["TeamName"]==team_i]
        ref_drivers += list(filter_df["Abbreviation"].unique())

    print(ref_drivers)
    
    for num_i in list(df["DriverNumber"].unique()):
        temp_start_pos = df["GridPosition"][num_i]
        temp_end_pos = df["Position"][num_i]
        temp_color = TEAM_COLORS[df["TeamName"][num_i]]
        temp_driver =  df["Abbreviation"][num_i]
        y_val = list(ref_drivers).index(temp_driver)

        print("ADDING LINE")
        print("DRIVER ",temp_driver," Start ",temp_start_pos, " END ",temp_end_pos, "y val ",y_val)


        fig.add_shape(type="line",
                        x0=temp_start_pos, 
                        y0=y_val, 
                        x1=temp_end_pos, 
                        y1=y_val, line_color=temp_color,opacity=.5)
    # render_object.write(trace2.to_dict())
    # fig.add_trace(trace2.to_dict())
    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)
    



def event_standings_overview(render_object):
    temp_session = st.session_state.cache["Session"]
    render_object.title(temp_session)

    cols = render_object.columns([1,2,2])

    with cols[0]:
        st.header("Final Results")
        for driver_number in list(temp_session.results.DriverNumber.unique()):
            temp_driver = temp_session.results["Abbreviation"][driver_number]
            temp_team = temp_session.results["TeamName"][driver_number]

            temp_position = temp_session.results["Position"][driver_number]
            temp_grid_start = temp_session.results["GridPosition"][driver_number]
            temp_change = temp_grid_start - temp_position

            st.write(temp_driver," ",temp_grid_start," --> ",temp_position, "(",temp_change,")")

    st.write(temp_session.results)
    position_change_chart(temp_session.results,render_object)



           
def session_dashboard():
    year_selector, track_and_type, driver_lap_select, view_data = st.tabs(["📅 Year", "🏁 Track","🏎️ Driver(s)","🔍 Session Control"])


    with year_selector:
        selected_year = st.selectbox("Select a year",[2019,2020,2021,2022,2023])
        if st.button("Update Year"):
            st.session_state.cache = {}
            st.session_state.cache["Year"]=selected_year

    with track_and_type:
        if("Year" in st.session_state.cache):
            current_year_schedule = fastf1.get_event_schedule(st.session_state.cache["Year"])
            selected_track = st.selectbox("Select a track",current_year_schedule.Location)
            selected_type = st.selectbox("Select a type",['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R'])
            if st.button("Update Track & Type"):
                st.session_state.cache["Track"]=selected_track
                st.session_state.cache["Type"]=selected_type
        else:
            st.write("Select a year in the previous step")

    with driver_lap_select:
        if("Session" in st.session_state.cache):
            selected_teams = st.multiselect("Select Drivers by team",st.session_state.cache["Session"].laps.Team.unique(),default=st.session_state.cache["teams"])
            drivers = st.multiselect("Driver Select",st.session_state.cache["Session"].laps.Driver.unique(),default=st.session_state.cache["drivers"])
            if st.button("Update driver selection"):
                st.session_state.cache["drivers"] = drivers
                st.experimental_rerun()

            if st.button("Update driver selection by team"):
                temp_df = st.session_state.cache["Session"].laps
                temp_df = temp_df[temp_df['Team'].isin(selected_teams)]
                st.session_state.cache["drivers"] = temp_df.Driver.unique()
                st.session_state.cache["teams"] = selected_teams
                st.experimental_rerun()


        else:
            st.warning("Load a session in the view data section")


    with view_data:

        cols = st.columns(2)

        if cols[0].button("New Session Load"):
            st.session_state.cache={}
            st.experimental_rerun()

        if("Track" in st.session_state.cache):
            # IF SESSION NOT LOADED YET
            if("Session" not in st.session_state.cache):
                if(cols[1].button("Load Data")):
                    temp_session = fastf1.get_session(st.session_state.cache["Year"],st.session_state.cache["Track"],st.session_state.cache["Type"])
                    with st.spinner():
                        temp_session.load()
                        st.session_state.cache["Session"] = temp_session
                        st.session_state.cache["drivers"] = st.session_state.cache["Session"].laps.Driver.unique()
                        st.session_state.cache["teams"] = st.session_state.cache["Session"].laps.Team.unique()
                        st.session_state.cache["SessionLaps"] = temp_session.laps
                        st.session_state.cache["SessionLaps"]["LapTimeNum"] = st.session_state.cache["SessionLaps"].LapTime.dt.total_seconds()
                        st.session_state.cache["SessionLaps"]["TotalLapTimeNum"] = st.session_state.cache["SessionLaps"].Time.dt.total_seconds()

                        st.session_state.cache["SessionLaps"] = st.session_state.cache["SessionLaps"].sort_values(['LapNumber', 'TotalLapTimeNum'])


                        # Calculate position at the end of the lap
                        st.session_state.cache["SessionLaps"]['position_end'] = st.session_state.cache["SessionLaps"].groupby('LapNumber')['TotalLapTimeNum'].rank().astype(int)

                        # Calculate gap to the driver in front
                        st.session_state.cache["SessionLaps"]['gap_to_front'] = st.session_state.cache["SessionLaps"].groupby('LapNumber')['TotalLapTimeNum'].diff().fillna(0)

                        # Calculate gap to the driver in first
                        st.session_state.cache["SessionLaps"]['gap_to_first'] = st.session_state.cache["SessionLaps"].groupby('LapNumber')['TotalLapTimeNum'].transform(lambda x: x - x.min())
                    st.experimental_rerun()


            else:
                # IF SESSION EXISTS
                with st.expander("Lap Times Summary"):
                    st.header("Lap Time Distributions")
                    cols = st.columns([2,2])
                    # if("drivers" not in st.session_state.cache):

                    lap_deviation_for_session_chart(st.session_state.cache["Session"].laps,cols[0])
                    driver_avg_diff_chart(st.session_state.cache["Session"].laps,cols[1])
                    st.header("Animated Pace Charts")

                    animated_gap_chart(st)
                    
                        


                with st.expander("View Raw Laps Data"):
                    st.write(st.session_state.cache["Session"].laps)

                if("drivers" in st.session_state.cache):
                    drivers = st.session_state.cache["drivers"]
                    with view_data.expander(str(drivers)):
                        st.title(drivers)
                        drivers_laptimes(st.session_state.cache["Session"].laps,st)

                        cols = st.columns(2)
                    



        else:
            # TRACK AND TYPE INPUT NEEDED
            st.write("Select a track and type in the previous step")


st.session_state.iteration += 1
print("======================")
print("Iteration ",st.session_state.iteration)




session_dashboard()

side_bar_cache_display()

if("Session" in st.session_state.cache):
    event_standings_overview(st)