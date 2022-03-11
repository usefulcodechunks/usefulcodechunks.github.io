import streamlit as st
import pandas as pd
import random

emoji_list='''🎧🥇🕋🗼🎨💎🛷🏥💾📎🏢🏩🎣🚃🔦🎠📯🏉📔🏋️⚱️🎮🎳🏬🧗‍♂️💳🚓💊🛒🚦⚽️⚖️🏺🔏🏋️‍♀️🏓🚝🧯🚢🎢🎀📜⌛️🧗🥅💻🪕✉️🚇⏲🗓🛳🧿🤼‍♀️🏠🛥🪧⌚️🧩🧘‍♂️📚🏄‍♀️🔒⛳️🛻🤼‍♂️🌆🎐💈🧻🖊🎊🏡🚣‍♀️🖨⛲️📨🧭🚒🔖💷🚚🎤🚡🛸🏗📱🎟📹📤🛤🚣🕹🧺🏣🏇🚁✈️🗝🏸🏞🏖🚛📐📌🪜🧴🛫📫🤽🚧🗡🚎🏌️‍♂️🛌🏪🪠⛸🤹‍♂️🪂☎️♟💡📻🥉🪔📙🏹🪆🛴🖥🌁🗾📁🤺🚤🖇⚗️🏀🔮🌃🌄🚉📡🧨🛹📬🌉🗿🚆🛠✂️🎙✒️🚙🪟🚟🏨🪝🛵🎯🥁🤸‍♀️🚵🧽🤾‍♀️🏐🛀🤽‍♂️🚕🚘🏰🚈🎞🩹⛹️⏳🔫🗂🏆🎾🏋️‍♂️🧰🏏🧷🎗🗄🩰💾🏦🔪🕍🗑📇🪤🚽📞🏥🚖💸🚲🪁🎨🪄🎖🤼🎹🖲🏊🛰📧⚙️🪒🏄‍♂️🧮🚋🥊💵🛶🥈💰🪃🚜🖼🥌🏊‍♂️🛡🌅⏰🌋🎆🤽‍♀️🛁🚨📺🎑💿🥎🏟🤿🎇🌇⚒🏘🗻🪑📗🤸🔭🕌⌨️⛏🎫🧹📍🏤🔨🏊‍♀️⚔️🏭🚌🧫🧗‍♀️📃🖱💴🧲🎛🕰🚴‍♀️🎥🎎🚂📋🛬📆📰🧾🏜🔑🦼📉🏅🕋🏄🚥🏌️‍♀️📿💽📷🛍🏯⛩⛵️🏌️🧼📀⏱🔓📲🛺🎁🕳🪗🤹🏔📸📒💉⚾️📄🚊🎏⛹️‍♀️🚴🧪📼✏️🌡⛽️📩🔋🎬🏵🎪💶🪙🪦🪣🤸‍♂️🏚🛼⛹️‍♂️🔍🎼🔩⛺️🏒🦠🚠📅🔐🚗🏙📂🎧🪓📦📠🚣‍♂️🔬🏷💌🎸🔎🚏📘🎚🧘‍♀️🔗🎷🚅📈🚞🖍🚿🤾‍♂️📊🛖🦯🎻🪅📮🚍🛏🎺🏈🗳🎡🖌🚀📓🎿🏮🤹‍♀️📑🦽💣📥⛴⛪️🚬🎽⛷🚄🪘🔌📪🩺🪀🤾💺🚐🚰🛩🚑🖋🏫🧬🎉⚓️🎱🧱🔧🚵‍♀️📭🎈🧸🏂🧘🥏🪛🏑🥍📖📟🚴‍♂️🏎🎭🌠🧧🌌🛕📏⛰💒🎰🎲🚔🛋📕🗜📝🗽🏕🥋🩸🚵‍♂️'''

st.title("due diligence dashboard")
query_params = st.experimental_get_query_params()
# st.write(query_params)

def turn_dataframe_into_nice_table(df,target_container):
    num_of_cols = len(df.columns)
    column_titles = list(df.columns)


    subdivisions = st.columns(num_of_cols)
    for col_i in range(num_of_cols):
        subdivisions[col_i].subheader(column_titles[col_i])


    for index, row in df.iterrows():            # Iterate over each row
        for cell_i in range(num_of_cols):       # Iterate over each cell in row
            if("http" in str(row[column_titles[cell_i]])):
                link = '['+column_titles[cell_i]+']('+row[column_titles[cell_i]]+')'
                link = link.replace(" ","%20")
                subdivisions[cell_i].markdown(str(link), unsafe_allow_html=True)
            else:
                subdivisions[cell_i].write(row[column_titles[cell_i]])

def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, "Link")


def make_linkedin_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''

    template = "https://www.linkedin.com/search/results/all/?keywords={search_value}"

    return template.format(search_value=search_parameter["input"])

def make_crunchbase_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''

    template = "https://www.crunchbase.com/textsearch?q={search_value}"

    return template.format(search_value=search_parameter["input"])

def make_google_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''

    template = "https://www.google.com/search?q='{search_value}'"

    return template.format(search_value=search_parameter["input"])

def format_search_parameters_with_links(search_parameters):
    for n_i in range(len(search_parameters)):
        if(st.session_state.cache["search_parameters"][n_i]["input"] != ""):
            st.session_state.cache["search_parameters"][n_i]["Linkedin"] = make_linkedin_link(st.session_state.cache["search_parameters"][n_i])
            st.session_state.cache["search_parameters"][n_i]["Crunchbase"] = make_crunchbase_link(st.session_state.cache["search_parameters"][n_i])
            st.session_state.cache["search_parameters"][n_i]["Google"] = make_google_link(st.session_state.cache["search_parameters"][n_i])
        else:
            st.session_state.cache["search_parameters"][n_i]["Linkedin"] = "https://www.linkedin.com/"
            st.session_state.cache["search_parameters"][n_i]["Crunchbase"] = "https://www.crunchbase.com/"
            st.session_state.cache["search_parameters"][n_i]["Google"] = "https://www.google.com/"

def add_blank_search_query(cache_list):
    cache_list.append({"id":""})
    return cache_list

def make_search_inputs(container):
    for n_i in range(len(st.session_state.cache["search_parameters"])):
        display_string = str(n_i)+') '+emoji_list[n_i]
        st.session_state.cache["search_parameters"][n_i]["id"] = display_string
        with container.expander(display_string):
            st.session_state.cache["search_parameters"][n_i]["input"] = st.text_input(display_string+"Input Search")

def initialize_session_state_vars():
    if 'cycle' not in st.session_state:
        st.session_state.cycle = 0
    if 'change_log' not in st.session_state:
        st.session_state.change_log = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    if 'cache' not in st.session_state:
        st.session_state.cache = {}
    if("search_parameters" not in st.session_state.cache.keys()):
        st.session_state.cache["search_parameters"] = []
        st.session_state.cache["search_parameters"] = add_blank_search_query(st.session_state.cache["search_parameters"])

initialize_session_state_vars()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# format_url = st.sidebar.button("Format URL")
#
# if(format_url):
#     compound_string = "https://share.streamlit.io/usefulcodechunks/usefulcodechunks.github.io/Streamlitapp/master.py?queries="
#     with st.sidebar.info("Copy the URL in your browser and share with your view!"):
#         for n_i in range(len(st.session_state.cache["search_parameters"])):
#             if(st.session_state.cache["search_parameters"][n_i]["input"] != ""):
#                 compound_string += st.session_state.cache["search_parameters"][n_i]["input"]
#                 compound_string += ","
#     st.code(compound_string)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Control Buttons at the top of the page
add_side, remove_side = st.sidebar.columns([1,1])

add_input = add_side.button("+ Add input")
remove_input = remove_side.button("- Remove input")

if(add_input):
    st.session_state.cycle += 1
    st.session_state.cache["search_parameters"] = add_blank_search_query(st.session_state.cache["search_parameters"])

if(remove_input):
    st.session_state.cycle += 1
    st.session_state.cache["search_parameters"].pop()
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<




make_search_inputs(st.sidebar)

# side_b.write(st.session_state.cache["search_parameters"])

your_df_from_dict=pd.DataFrame(st.session_state.cache["search_parameters"])
# st.write(your_df_from_dict)
turn_dataframe_into_nice_table(your_df_from_dict,st)

link = '[GitHub](http://github.com)'
format_search_parameters_with_links(st.session_state.cache["search_parameters"])
