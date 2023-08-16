import nfl_data_py as nfl
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="NFL Data App",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded",
)

years = [2019,2020,2021,2018]

def filter_table(df,selected_col,values):
    if(df[selected_col].dtype == 'object'):
        filter_df = df[df[selected_col].isin(values)]
    else:
        filter_df = df[df[selected_col] >= values[0]]
        filter_df = filter_df[filter_df[selected_col] <= values[1]]
    return filter_df

def display_table_and_filters(df,render_canvas):
    # with render_canvas:
    

    filter_df = df
    cols = render_canvas.columns([2,2,1])

    filter_col = cols[0].selectbox("Select a column to filter",df.columns)
    
    if(df[filter_col].dtype == 'object'):
        values = cols[1].multiselect('Select objects',df[filter_col].unique())

    else:
        if(df[filter_col].dtype == 'float64'):
            min_val = float(df[filter_col].min())
            max_val = float(df[filter_col].max())
        if(df[filter_col].dtype == 'int32'):
            min_val = int(df[filter_col].min())
            max_val = int(df[filter_col].max())

        if(min_val != max_val):
            values = cols[1].slider('Select a range of values',min_val, max_val,(min_val, max_val))

    if cols[2].button("Add Filter"):

        filter_meta_data = {"filter_col":filter_col,"values":values}

        st.session_state.filter_cache.append(filter_meta_data)

    if cols[2].button("Clear Filters"):
        st.session_state.filter_cache = []
            
            
    for filter_layer in st.session_state.filter_cache:
        filter_df = filter_table(filter_df,filter_layer["filter_col"],["values"])

    render_canvas.write(filter_df)


def initialize_nfl_app_session_state_vars():

    if "nfl_injuries" not in st.session_state:
        st.session_state.nfl_injuries = {"data":None, "years": None}
    if "filter_cache" not in st.session_state:
        st.session_state.filter_cache = []

def injury_data_loader_widget(render_canvas,selected_years):
    with render_canvas.expander("Load Injury Data"):
        button_string = "Load data for "+str(selected_years)
        if st.button(button_string):
            temp_data = nfl.import_injuries(selected_years)
            st.session_state.nfl_injuries = {"data": temp_data, "years": selected_years}


def year_selector_and_loaders(render_canvas):
    selected_years = render_canvas.multiselect('Select years you wish to view', years)
    injury_data_loader_widget(render_canvas,selected_years)

initialize_nfl_app_session_state_vars()
year_selector_and_loaders(st.sidebar)


if(st.session_state.nfl_injuries["data"] is not None):
    
    display_table_and_filters(st.session_state.nfl_injuries["data"],st)
    st.write(st.session_state.nfl_injuries["data"].columns)
    st.write(st.session_state.nfl_injuries["data"].dtypes)
    st.write(st.session_state.nfl_injuries["data"].dtypes["team"])

st.write(st.session_state.filter_cache)

# data = nfl.import_pbp_data([2021])


# st.write(list(nfl.see_pbp_cols()))


# data = data[data.game_id == "2021_01_ARI_TEN"]
# st.write(data)


# tempd = tempd[tempd.full_name == "Jimmy Garoppolo"]
# st.write(tempd)

# temp2 = nfl.import_snap_counts([2021])
# st.write(temp2)
