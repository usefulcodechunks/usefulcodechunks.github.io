import streamlit as st
import numpy as np
import pandas as pd
import os
import time 


# Formula 1 Data Imports
import fastf1
import fastf1.plotting

# Importing Packages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.collections import LineCollection
import matplotlib as mpl
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.subplots import make_subplots








current_path = os.getcwd()

st.set_page_config(
    page_title="Formula 1 Data App",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Formula 1 Data Viewer")

def declare_session_states():
    if "sessions_cache" not in st.session_state:
        st.session_state.sessions_cache = {0 : {}}
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

declare_session_states()

# HELPER FUNCTIONS FOR GETTING CACHE DATA can be chained with the attribute needed ex: ["attr"]
def get_current_sessions_cache(attr=None,selected_id=st.session_state.current_index):
    if attr is None:
        return st.session_state.sessions_cache[selected_id]
    else:
        return st.session_state.sessions_cache[selected_id][attr]
# USED TO CHECK IF A VARIABLE EXISTS
def step_completed(attr):
    if attr not in st.session_state.sessions_cache[st.session_state.current_index]:
        return False
    else:
        return True
# USED TO UPDATE A SESSIONS CACHE ATTR
def update_attr_on_sessions_cache(attr,value):
    st.session_state.sessions_cache[st.session_state.current_index][attr] = value

# OLD PLOTTING CODE
def plot_driver(render_object):
    laptimedata = get_current_sessions_cache("fastest_lap")


    colormap = mpl.cm.plasma

    # Get telemetry data
    x = laptimedata.telemetry['X']              # values for x-axis
    y = laptimedata.telemetry['Y']              # values for y-axis
    color = laptimedata.telemetry['Speed']      # value to base color gradient on

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # We create a plot with title and adjust some setting to make it look good.
    fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
    # fig.suptitle(f'{weekend.name} {year} - {driver} - Speed', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')


    # After this, we plot the data itself.
    # Create background track line
    ax.plot(laptimedata.telemetry['X'], laptimedata.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(color.min(), color.max())
    lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

    # Set the values used for colormapping
    lc.set_array(color)

    # Merge all line segments together
    line = ax.add_collection(lc)


    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")


    # Show the plot
    the_plot = render_object.pyplot(plt)   

# HELPER FUNCTION TO ROUND NUMBERS
def pretty_number(number):
    return round(number,2)

def lap_deviation_for_session_chart(temp_race_data,render_object):
    # DATA FOR DOT PLOT

        

    drivers = list(temp_race_data.Driver.unique())*3
    drivers.sort()
    minmaxes_str = (["25%","50%","75%"]*len(temp_race_data.Driver.unique()))
    minmaxes_laptimes = []
    id_order = []
    seen = []
    for driver in drivers:
        if(driver not in seen):
            temp_df = temp_race_data.pick_driver(driver)
            print(driver)
        
            quantiles_for_driver = temp_df.LapTime.dt.total_seconds().quantile([.25,.50,.75])
            print(quantiles_for_driver)
            minmaxes_laptimes += [quantiles_for_driver[.25],quantiles_for_driver[.50],quantiles_for_driver[.75]]
            print(minmaxes_laptimes)
            id_order += [2,1,3]
            seen.append(driver)


    df = pd.DataFrame([])
    df["drivers"] = drivers
    df["minmaxtype"] = minmaxes_str
    df["laptime"] = minmaxes_laptimes
    df["id_order"] = id_order
    print("before==========")
    print(df)

    df.sort_values(["id_order", "laptime"], ascending=True, inplace=True)
    print("after=========")
    
    print(df)

    

    #lowess', 'rolling', 'ewm', 'expanding', 'ols']
    fig = px.scatter(df, x="laptime", y="drivers", color="minmaxtype",
                    title="Lap Time Curve",color_discrete_map={"25%": 'red',"50%": 'orange',"75%": 'green'}
                    )
    
    temp_order = df["drivers"].unique()
    print(df)
    for driver in temp_order:
        y_val = list(temp_order).index(driver)

        temp_df = df[df["drivers"]==driver]
        temp_dict = temp_df.to_dict('index')
        temp_res = {"25%" : None , "50%" : None, "75%" : None}
        # render_object.write(temp_dict)
        for key in temp_dict:
            temp_res[temp_dict[key]["minmaxtype"]] = temp_dict[key]["laptime"]

        fig.add_shape(type="line",
                        x0=temp_res["25%"], 
                        y0=y_val, 
                        x1=temp_res["75%"], 
                        y1=y_val, line_color="grey",opacity=.5)



        
    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)

def driver_avg_diff_chart(temp_race_data,render_object):
    avg_lap_all = temp_race_data.LapTime.dt.total_seconds().mean()
    avg_laptimes = temp_race_data.groupby('Driver')['LapTime'].apply(lambda x: x.dt.total_seconds().mean())
    avg_laptimes = avg_laptimes - avg_lap_all

    
    df = pd.DataFrame([])
    df["Drivers"] = avg_laptimes.index
    df["Lap Delta"] = list(avg_laptimes)
    df["SlowerOnAvg"] = df["Lap Delta"] >= 0

    df = df.sort_values('Lap Delta',ascending=False)


    fig = px.bar(df, title="Avg Delta Pace", x="Lap Delta", y="Drivers", color="SlowerOnAvg", orientation='h',color_discrete_map={False: 'green',True: 'red'})
    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)

def plot_x_y(dataframe,xcol,ycol,color,symbol,render_object,meta_data,option="Speed"):
    dataframe["TimeReal"] = dataframe["Time"].dt.total_seconds()

    bins = [0, meta_data["Sector 1"], meta_data["Sector 2"], meta_data["Sector 3"], float('inf')]
    labels = ['sector 1', 'sector 2', 'sector 3', 'other']
    dataframe['sector'] = pd.cut(dataframe['TimeReal'], bins=bins, labels=labels, right=False)
    try:
        fig = px.scatter(dataframe, y=ycol, x=xcol, color=color, symbol=symbol,color_continuous_scale="thermal")
    except:
        fig = px.scatter(dataframe, y=ycol, x=xcol, color=color,color_continuous_scale="thermal")

    render_object.plotly_chart(fig, theme="streamlit",use_container_width=True)


# WIDGET FOR GETTING A SESSION + DRIVER DATA and displaying it
def session_selector():

    year_selector, track_and_type, driver_lap_select, view_data = st.tabs(["📅 Year", "🏁 Track","🏎️ Driver","🔍 View"])


    # STEP 1
    selected_year = year_selector.selectbox("Choose a year",[2019,2020,2021,2023])
    update_attr_on_sessions_cache("year",selected_year)


    # STEP 2
    if step_completed("year"):
        update_attr_on_sessions_cache("event_schedule",fastf1.get_event_schedule(selected_year))

        tracks = update_attr_on_sessions_cache("tracks",get_current_sessions_cache("event_schedule")["Country"].unique())
        
        selected_track = track_and_type.selectbox("Select a track",get_current_sessions_cache("tracks"))

        session_type = track_and_type.selectbox("Session Type",['FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'R'])

        if track_and_type.button("Get Session"):
            update_attr_on_sessions_cache("selected_track",selected_track)
            update_attr_on_sessions_cache("session_type",session_type)
            update_attr_on_sessions_cache("selected_session",fastf1.get_session(
                                                                        get_current_sessions_cache("year"), 
                                                                        get_current_sessions_cache("selected_track"), 
                                                                        get_current_sessions_cache("session_type")))

    # STEP 3
    if step_completed("selected_session"):
        get_current_sessions_cache("selected_session").load()
        if not step_completed("drivers"):
            temp_list = get_current_sessions_cache("selected_session").results["Abbreviation"].unique()
            update_attr_on_sessions_cache("drivers",temp_list)
        if step_completed("drivers"):
            selected_driver = driver_lap_select.selectbox("Choose a driver",get_current_sessions_cache("drivers"))
            update_attr_on_sessions_cache("driver",selected_driver)
    else:
        driver_lap_select.warning("Please Select a session in the previous step")

       
    
    # STEP 4
    if step_completed("driver"):

        temp_race_data = get_current_sessions_cache("selected_session").laps


        with view_data.expander("Lap Time Summary"):
            cols = st.columns([2,2])

            lap_deviation_for_session_chart(temp_race_data,cols[0])
            driver_avg_diff_chart(temp_race_data,cols[1])

        with view_data.expander('VIEW RAW DATA'):
            st.write(temp_race_data)

        #  x column, lap number, y column laptime
        # 


        # x_distribution_plotly(tempds,"Lap Times",view_data)
        
        # view_data.write(temp_race_data.LapTime.dt.total_seconds())
        # view_data.write(temp_race_data.LapTime.dt.total_seconds())
        # view_data.write(temp_race_data["LapNumber"])

        avg_lap_all = temp_race_data.LapTime.dt.total_seconds().mean()
        # view_data.write(temp_race_data.LapTime.dt.total_seconds() - temp_race_data.LapTime.dt.total_seconds().mean())
        

  


        


        # CALCULATING GLOBAL AVERAGES FOR SECTORS
        global_avg_for_s1 = temp_race_data.Sector1Time.dt.total_seconds().mean()
        global_avg_for_s2 = temp_race_data.Sector2Time.dt.total_seconds().mean()
        global_avg_for_s3 = temp_race_data.Sector3Time.dt.total_seconds().mean()

        # DEFINING THE MAX AND MIN LAP TIMES
        max_lap_time = temp_race_data.LapTime.dt.total_seconds().max()
        min_lap_time = temp_race_data.LapTime.dt.total_seconds().min()

        # DEFINING THE MAX AND MIN TIRE LIFE
        max_tire_life  = temp_race_data.TyreLife.max()
        min_tire_life  = temp_race_data.TyreLife.min()

        # DEFINING THE AVERAGE LAP TIME BY LAP NUMBER
        avg_laptimes = temp_race_data.groupby('LapNumber')['LapTime'].apply(lambda x: x.dt.total_seconds().mean())


        driver = get_current_sessions_cache("driver")
        with view_data.expander(driver):
            st.title(driver)            
            
            temp_df = temp_race_data.pick_driver(driver)
            temp_lap_times = temp_df.LapTime.dt.total_seconds()
            temp_tire_life = temp_df.TyreLife
            temp_laps = temp_df.LapNumber    


            st.write(temp_df.LapTime.dt.total_seconds().quantile([.25,.50,.75]))
            # st.write(temp_df.pick_fastest().get_telemetry())
            # st.write(temp_df.pick_fastest().get_car_data())
            # st.write(temp_df.pick_fastest().get_car_data())




            st.write("Starting Order", temp_df.Position.iloc[0])
            st.write("Final Standing", temp_df.Position.iloc[-1])

            for stint_i in temp_df.Stint.unique():
                small_df = temp_df[temp_df.Stint == stint_i]
                st.write(stint_i, " Compound: ",small_df.Compound.iloc[0], " Duration: ",small_df.TyreLife.iloc[-1])



            # Fastest Sector Times

            cols = st.columns(3)

            local_avg_for_s1 = temp_df.Sector1Time.dt.total_seconds().mean()
            local_avg_for_s2 = temp_df.Sector2Time.dt.total_seconds().mean()
            local_avg_for_s3 = temp_df.Sector3Time.dt.total_seconds().mean()  

            cols[0].metric(label="Sector 1 Avg", value=pretty_number(local_avg_for_s1), delta=pretty_number(local_avg_for_s1-global_avg_for_s1), delta_color="inverse")
            cols[1].metric(label="Sector 2 Avg", value=pretty_number(local_avg_for_s2), delta=pretty_number(local_avg_for_s2-global_avg_for_s2), delta_color="inverse")
            cols[2].metric(label="Sector 3 Avg", value=pretty_number(local_avg_for_s3), delta=pretty_number(local_avg_for_s3-global_avg_for_s3), delta_color="inverse")

            second_cols = st.columns(2)
            
            selected_lap = second_cols[1].selectbox("Select a Lap",temp_laps,key=driver+"slp",index=3)

            meta_dict_for_sectors = {"Sector 1" : temp_df[temp_df["LapNumber"]==selected_lap]["Sector1Time"].dt.total_seconds().values[0]}
            meta_dict_for_sectors["Sector 2"] = meta_dict_for_sectors["Sector 1"] + temp_df[temp_df["LapNumber"]==selected_lap]["Sector2Time"].dt.total_seconds().values[0]
            meta_dict_for_sectors["Sector 3"] = meta_dict_for_sectors["Sector 2"] + temp_df[temp_df["LapNumber"]==selected_lap]["Sector3Time"].dt.total_seconds().values[0]
            # meta_dict_for_sectors["S1-S"] = temp_df[temp_df["LapNumber"]==selected_lap]["Sector1Time"].dt.total_seconds().values[0] >





            tabs = second_cols[1].tabs(["Speed Map","Sector Map"])

            with tabs[0]:
                plot_x_y(temp_df[temp_df["LapNumber"]==selected_lap].get_telemetry(),"X","Y","Speed","sector",st,meta_dict_for_sectors)
            with tabs[1]:            
                plot_x_y(temp_df[temp_df["LapNumber"]==selected_lap].get_telemetry(),"X","Y","sector","sector",st,meta_dict_for_sectors)


            


            # fig, ax1 = plt.subplots()
            # ax1.set_ylim([min_lap_time, max_lap_time])
            # ax1.plot(temp_laps,temp_lap_times ,"-",color="blue")
            # ax1.plot(temp_laps,avg_laptimes.iloc[:len(temp_laps)] ,"-.",color="red")

            # ax2 = ax1.twinx()
            # ax2.set_ylim([min_tire_life, max_tire_life])
            # ax2.plot(temp_laps,temp_tire_life ,"-.",color="orange")

            # second_cols[0].pyplot(fig)
            # second_cols[0].info("Orange is Tire Life, Red is Avg Lap Time, Blue is Driver")

            tabs = second_cols[0].tabs(["Lap Times","Delta Pace"])

            driver_laps_label = ["driver lap time"]*len(temp_laps)
            avg_laps_label = ["avg lap time"]*len(temp_laps)
            tire_laps_label = ["tire life"]*len(temp_laps)
            delta_laps_label = ["pace delta"]*len(temp_laps)

            temp_data = pd.DataFrame()  
            temp_data["LapNumber"] = pd.concat([pd.concat([pd.concat([temp_laps, temp_laps],ignore_index=True),temp_laps],ignore_index=True),temp_laps],ignore_index=True)
            avg_delta =  temp_lap_times - avg_laptimes.iloc[:len(temp_laps)]

            temp_data["Type"] = driver_laps_label+avg_laps_label+tire_laps_label+delta_laps_label
            temp_data["Datav"] = pd.concat([pd.concat([pd.concat([temp_lap_times, avg_laptimes.iloc[:len(temp_laps)]],ignore_index=True),temp_tire_life],ignore_index=True),avg_delta],ignore_index=True)
            temp_data["Positive"] = temp_data["Datav"] > 0

            subfig = make_subplots(specs=[[{"secondary_y": True}]],x_title="Driver Lap Times")
            subfig2 = make_subplots(specs=[[{"secondary_y": True}]],x_title="Driver Lap Times")


            with tabs[0]:
                fig = px.line(temp_data[(temp_data.Type != "tire life") & (temp_data.Type != "pace delta")], x="LapNumber", y="Datav",color="Type",line_dash ="Type")
                fig2 = px.line(temp_data[temp_data.Type == "tire life"], x="LapNumber", y="Datav",color="Type",line_dash ="Type")
                fig2.update_traces(yaxis="y2")
                subfig.add_traces(fig.data + fig2.data)
                subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
                st.plotly_chart(subfig, theme="streamlit",use_container_width=True)
            with tabs[1]:
                fig3 = px.line(temp_data[temp_data.Type == "pace delta"], x="LapNumber", y="Datav",color="Positive",line_dash ="Type")
                fig4 = px.line(temp_data[temp_data.Type == "tire life"], x="LapNumber", y="Datav",line_dash ="Type")
                fig4.update_traces(yaxis="y2")
                subfig2.add_traces(fig3.data + fig4.data)
                subfig2.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
                st.plotly_chart(subfig2, theme="streamlit",use_container_width=True)
            
                

            # fig = px.line(temp_data[temp_data.Type != "tire life"], x="LapNumber", y="Datav",color="Type",line_dash ="Type",symbol="Type")
            # fig2 = px.line(temp_data[temp_data.Type == "tire life"], x="LapNumber", y="Datav",color="Type",line_dash ="Type")
            

        
        # plot_driver(view_data)

session_selector()






