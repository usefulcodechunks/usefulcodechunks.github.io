import streamlit as st
import pandas as pd

from helperfunctions.helperfunctions import (
    make_linkedin_link,
    make_crunchbase_link,
    make_google_link,
    make_clickable,
    generate_random_emoji
    )

st.set_page_config(
    page_title="Due Diligence",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

def due_dill_app(render_object):

    def turn_dataframe_into_nice_table(df,target_container):
        num_of_cols = len(df.columns)
        column_titles = list(df.columns)


        subdivisions = render_object.columns(num_of_cols)
        for col_i in range(num_of_cols):
            subdivisions[col_i].subheader(column_titles[col_i])


        for index, row in df.iterrows():            # Iterate over each row
            for cell_i in range(num_of_cols):       # Iterate over each cell in row
                if("http" in str(row[column_titles[cell_i]])):
                    link = '['+column_titles[cell_i]+']('+row[column_titles[cell_i]]+')'
                    link = link.replace(" ","%20")
                    make_clickable(subdivisions[cell_i],row[column_titles[cell_i]],column_titles[cell_i])
                    # subdivisions[cell_i].write(str(link))
                else:
                    subdivisions[cell_i].write(row[column_titles[cell_i]])




    def format_search_parameters_with_links(search_parameters):
        for n_i in range(len(search_parameters)):
            if(render_object.session_state.cache["search_parameters"][n_i]["input"] != ""):
                render_object.session_state.cache["search_parameters"][n_i]["Linkedin"] = make_linkedin_link(render_object.session_state.cache["search_parameters"][n_i]["input"])
                render_object.session_state.cache["search_parameters"][n_i]["Crunchbase"] = make_crunchbase_link(render_object.session_state.cache["search_parameters"][n_i]["input"])
                render_object.session_state.cache["search_parameters"][n_i]["Google"] = make_google_link(render_object.session_state.cache["search_parameters"][n_i]["input"])
            else:
                render_object.session_state.cache["search_parameters"][n_i]["Linkedin"] = "https://www.linkedin.com/"
                render_object.session_state.cache["search_parameters"][n_i]["Crunchbase"] = "https://www.crunchbase.com/"
                render_object.session_state.cache["search_parameters"][n_i]["Google"] = "https://www.google.com/"

    def add_blank_search_query(cache_list):
        cache_list.append({"id":""})
        return cache_list

    def make_search_inputs(container):
        for n_i in range(len(render_object.session_state.cache["search_parameters"])):
            display_string = str(n_i)+') '+generate_random_emoji(n_i) #FLAG
            render_object.session_state.cache["search_parameters"][n_i]["id"] = display_string
            with container.expander(display_string):
                if(n_i == 0):
                    render_object.session_state.cache["search_parameters"][n_i]["input"] = render_object.text_input(display_string+"Input Search",value="Streamlit")
                else:
                    render_object.session_state.cache["search_parameters"][n_i]["input"] = render_object.text_input(display_string+"Input Search")

    def initialize_session_state_vars_dueapp():
        if 'cycle' not in render_object.session_state:
            render_object.session_state.cycle = 0
        if 'change_log' not in render_object.session_state:
            render_object.session_state.change_log = {}
        if 'current_page' not in render_object.session_state:
            render_object.session_state.current_page = "Home"
        if 'cache' not in render_object.session_state:
            render_object.session_state.cache = {}
        if("search_parameters" not in render_object.session_state.cache.keys()):
            render_object.session_state.cache["search_parameters"] = []
            render_object.session_state.cache["search_parameters"] = add_blank_search_query(render_object.session_state.cache["search_parameters"])

    initialize_session_state_vars_dueapp()

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # format_url = render_object.sidebar.button("Format URL")
    #
    # if(format_url):
    #     compound_string = "https://share.streamlit.io/usefulcodechunks/usefulcodechunks.github.io/Streamlitapp/master.py?queries="
    #     with render_object.sidebar.info("Copy the URL in your browser and share with your view!"):
    #         for n_i in range(len(render_object.session_state.cache["search_parameters"])):
    #             if(render_object.session_state.cache["search_parameters"][n_i]["input"] != ""):
    #                 compound_string += render_object.session_state.cache["search_parameters"][n_i]["input"]
    #                 compound_string += ","
    #     render_object.code(compound_string)
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Control Buttons at the top of the page
    add_side, remove_side = render_object.sidebar.columns([1,1])

    add_input = add_side.button("+ Add input")
    remove_input = remove_side.button("- Remove input")

    if(add_input):
        render_object.session_state.cycle += 1
        render_object.session_state.cache["search_parameters"] = add_blank_search_query(render_object.session_state.cache["search_parameters"])

    if(remove_input):
        render_object.session_state.cycle += 1
        render_object.session_state.cache["search_parameters"].pop()
    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<




    make_search_inputs(render_object.sidebar)

    # side_b.write(render_object.session_state.cache["search_parameters"])

    your_df_from_dict=pd.DataFrame(render_object.session_state.cache["search_parameters"])
    # render_object.write(your_df_from_dict)
    turn_dataframe_into_nice_table(your_df_from_dict,st)

    link = '[GitHub](http://github.com)'
    format_search_parameters_with_links(render_object.session_state.cache["search_parameters"])

st.title("Due Diligence App")
st.info("Use the sidebar controls to add the names of companies you wish to find on LinkedIn, Crunchbase and Google",icon="❓")
due_dill_app(st)
