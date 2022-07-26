from pyvis.network import Network
from IPython.core.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
import streamlit as st
import streamlit.components.v1 as components
import os


def initialize_session_state_vars_n():
    if 'node_app_cache' not in st.session_state:
        st.session_state.node_app_cache = {
                    "dataframe":None,
                    "dataframe_type":None,
                    "G" : None,
                    "NT" : None,
                    "viz_settings" : {},
                    "analytics" : {}}
def rgb(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return convert_to_hex([r, g, b])


def convert_to_hex(rgba_color) :
    red = int(rgba_color[0]*1)
    green = int(rgba_color[1]*1)
    blue = int(rgba_color[2]*1)
    return '#%02x%02x%02x' % (red, green, blue)

def generate_attributes_of_users(G):

    most_connected_node = get_most_connected_node(G)
    length_of_distance = dict(nx.all_pairs_shortest_path_length(G))


    for node_i in G.nodes():
        G.nodes[node_i]["Connections"] = list(nx.neighbors(G, node_i))
        G.nodes[node_i]["NumOfConnections"] = len(list(nx.neighbors(G, node_i)))
        G.nodes[node_i]["ClusteringCoeff"] = nx.clustering(G, node_i)

        if(node_i != most_connected_node):
            try:
                G.nodes[node_i]["SeperationToCenter"] = length_of_distance[most_connected_node][node_i] + 1
            except KeyError:
                G.nodes[node_i]["SeperationToCenter"] = 1
        else:
            G.nodes[node_i]["SeperationToCenter"] = 1

    return G

def update_nodes_from_attr_dict(G): #,size_col,color_col,title_col):
    color_max_value = 0
    color_min_value = 9999
    for node_i in G.nodes():
        G.nodes[node_i]["size"] = G.nodes[node_i][st.session_state.node_app_cache["viz_settings"]["size"]] * st.session_state.node_app_cache["viz_settings"]["size_multiplier"]
        temp_color_val = G.nodes[node_i][st.session_state.node_app_cache["viz_settings"]["color"]]
        if(temp_color_val > color_max_value):
            color_max_value = temp_color_val
        if(temp_color_val < color_min_value):
            color_min_value = temp_color_val
    for node_i in G.nodes():
        temp_color_val = G.nodes[node_i][st.session_state.node_app_cache["viz_settings"]["color"]]
        G.nodes[node_i]["color"] = rgb(color_min_value, color_max_value, temp_color_val)

    return G

def get_most_connected_node(G):
    result = max(G.degree(), key = lambda x: x[1])
    st.session_state.node_app_cache["analytics"]["most_connected_node"] = int(result[0])
    return int(result[0])

def generate_dummy_data():
    '''
        Data structure
        Obj_id | Obj_id | Weight
    '''
    sample_size = 50
    from_list = [random.randrange(1, 50, 1) for i in range(sample_size)]
    to_list = [random.randrange(1, 50, 1) for i in range(sample_size)]
    weight_list = [random.randrange(1, 10, 1) for i in range(sample_size)]


    data = pd.DataFrame(
                        {"from" :
                            from_list,
                         "to" :
                            to_list,
                        "weight" :
                            weight_list
                        })
    return data

def create_edge_dict(data, col_with_id_a = "from", col_with_id_b = "to", col_with_weight = "weight"):
    '''
        Generates unique dict of linked objects and summed weights
        As well as unique list of all ids from both id columns
            from col should be INT
            to col should be INT
            weight col should be INT
    '''
    master_dict = {}

    # for loop through the ids
    for index, row in data.iterrows():

        temp_id_a = int(row[col_with_id_a])
        temp_id_b = int(row[col_with_id_b])
        temp_weight= int(row[col_with_weight])
        temp_unique_set_id = set([temp_id_a, temp_id_b])

        if(str(temp_unique_set_id) not in master_dict.keys()):
            master_dict[str(temp_unique_set_id)] = {
                                                        "node_from": temp_id_a,
                                                        "node_to": temp_id_b ,
                                                        "node_weight": temp_weight
                                                    }
        else:
            master_dict[str(temp_unique_set_id)]["node_weight"] += temp_weight

    return {
            "edge_dict" : master_dict,
            "unique_list_of_ids" : list(set(data[col_with_id_a]) | set(data[col_with_id_b]))
            }

def create_node_graph():
    G = nx.DiGraph()
    return G

def add_edge_to_graph(G, node_from, node_to, node_weight):
    G.add_edge(node_from, node_to, weight=node_weight)

def add_node_to_graph(G, id, size=1, title="Default", color="#1c1c1c"):
    G.add_node(int(id), size=size, title=title, color=color)

def add_list_of_nodes(G, list_of_nodes: list):
    for value in list_of_nodes:
        add_node_to_graph(G, id=int(value))

def add_edges_from_dict(G, master_dict: dict):
    for key in master_dict:
        add_edge_to_graph(G,**master_dict[key])

def render_network(G,render_object):
    render_demo = render_object.button("Update Network")

    if(render_demo):
        nt = Network('600px', '600px')
        nt.from_nx(G)
        nt.inherit_edge_colors(st.session_state.node_app_cache["viz_settings"]["inherit_edge_colors"])
        nt.toggle_physics(st.session_state.node_app_cache["viz_settings"]["enable_physics"])
        if(st.session_state.node_app_cache["viz_settings"]["control_panel"]):
            nt.show_buttons(filter_=["physics"])
        for ix in nt.get_edges():
            ix["width"] = ix["weight"]
        nt.write_html('NodeNetworkRender/output.html')
        st.session_state.node_app_cache["NT"] = nt

def open_rendered_network():
    with st.expander("5) View Rendered Network"):
        managen1, managen2, managen3 = st.columns([2,1,1])
        file_list=os.listdir("NodeNetworkRender/")
        file_selection = managen1.selectbox("Select A HTML File",file_list)
        show = managen2.button("Render Here")
        open_in_new_tab = managen2.button("Render In Tab")

        HtmlFile = open("NodeNetworkRender/"+file_selection, 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        if(show):
            st.write("Showing: ","NodeNetworkRender/"+file_selection)
            st.write("Red High Green Med Blue low")

            components.html(source_code, width=670,height=600)

        # if(open_in_new_tab):
        #     st.session_state.node_app_cache["NT"].show("NodeNetworkRender/"+file_selection)

        render_network(st.session_state.node_app_cache["G"],managen3)                                               # Render the network


def set_data_source():
    #  Generate Data
    with st.expander("1) File Upload Or Generate Dummy Data"):
        uploadside, dummydataside = st.columns(2)

        use_uploaded_file = uploadside.button("Use CSV")
        uploaded_file = uploadside.file_uploader("Choose a file")

        use_dummy_data = dummydataside.button("Generate Dummy Data")

        if(use_dummy_data):
            st.session_state.node_app_cache["dataframe"] = generate_dummy_data()
            st.session_state.node_app_cache["dataframe_type"] = "Dummy Data"
        if(use_uploaded_file):
            if(uploaded_file is not None):
                st.session_state.node_app_cache["dataframe"] = pd.read_csv(uploaded_file)
                st.session_state.node_app_cache["dataframe_type"] = uploaded_file.name

            else:
                st.warning("No File Uploaded")

def return_num_df(df):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

    newdf = df.select_dtypes(include=numerics)
    return newdf

def set_network_style_options():
    with st.expander("2) Set the Rules for your node network"):
        network_stylea, network_styleb = st.columns(2)

        if(st.session_state.node_app_cache["G"] is not None):
            tmp = st.session_state.node_app_cache["analytics"]["most_connected_node"]
            selectable_columns = list(st.session_state.node_app_cache["G"].nodes[tmp].keys())
            size_column = network_stylea.selectbox("Select The Num Column for the Node Size",selectable_columns)
            color_column = network_stylea.selectbox("Select The Color Column for the Node Color",selectable_columns)

            size_multiplier = network_styleb.number_input("Size multiplier",value=1)

            st.session_state.node_app_cache["viz_settings"]["size"] = size_column
            st.session_state.node_app_cache["viz_settings"]["color"] = color_column
            st.session_state.node_app_cache["viz_settings"]["size_multiplier"] = size_multiplier

def set_viz_settings():
    with st.expander("4) Settings for rendered network"):
        enable_physics = st.checkbox('Enable Physics')
        control_panel = st.checkbox('Enable Physics Controls')
        inherit_edge_colors = st.checkbox("Edges Inherit Node Colors")

        st.session_state.node_app_cache["viz_settings"]["enable_physics"] = enable_physics
        st.session_state.node_app_cache["viz_settings"]["control_panel"] = control_panel
        st.session_state.node_app_cache["viz_settings"]["inherit_edge_colors"] = inherit_edge_colors


def status_bar(render_object):
    render_object.title("Status Of Env Variables")

    render_object.write("Dataset Connected: ",st.session_state.node_app_cache["dataframe"] is not None)
    render_object.write("Current Data Source: ",st.session_state.node_app_cache["dataframe_type"])
    if(st.session_state.node_app_cache["dataframe"] is not None):
        render_object.write("Network Object: ",st.session_state.node_app_cache["G"] is not None)
        if(st.session_state.node_app_cache["G"] is not None):
            render_object.title("Network Stats")

            render_object.write("Nodes Count: ",len(list(st.session_state.node_app_cache["G"].nodes)))
            render_object.write("Edges Count: ",len(list(st.session_state.node_app_cache["G"].edges)))
            render_object.write("Most Connect Node: ",get_most_connected_node(st.session_state.node_app_cache["G"]))

            node_picker = render_object.selectbox("Select A Node",list(st.session_state.node_app_cache["G"].nodes))
            render_object.title("Node ID {0}".format(node_picker))
            render_object.write(st.session_state.node_app_cache["G"].nodes[node_picker])

def run_node_app():

    set_data_source()
    if(st.session_state.node_app_cache["dataframe"] is not None):
        from_col_inpt = st.selectbox("Choose a from column",st.session_state.node_app_cache["dataframe"].columns)
        to_col_inpt = st.selectbox("Choose a to column",st.session_state.node_app_cache["dataframe"].columns)
        weight_col_inpt = st.selectbox("Choose a weight column",st.session_state.node_app_cache["dataframe"].columns)



        #col_with_id_a = "from", col_with_id_b = "to", col_with_weight = "weight"):

        apply_col = st.checkbox("apply column mappings")
        if(st.session_state.node_app_cache["dataframe"] is not None and apply_col):

            pre_calc_step = create_edge_dict(st.session_state.node_app_cache["dataframe"],from_col_inpt,to_col_inpt,weight_col_inpt)                                 # Pass in the CSV to create a dictonary of all unique node connections
            st.session_state.node_app_cache["G"] = create_node_graph()                                            # initilize the node network object G
            add_list_of_nodes(st.session_state.node_app_cache["G"], pre_calc_step["unique_list_of_ids"])          # Add the List Of Nodes by passing in the G object + unique list of node IDs
            add_edges_from_dict(st.session_state.node_app_cache["G"], pre_calc_step["edge_dict"])                 # Add all of the edges by passing in the G object + dictonary from step1
            node_graph = generate_attributes_of_users(st.session_state.node_app_cache["G"])


            set_network_style_options()
            set_viz_settings()
            node_graph = update_nodes_from_attr_dict(st.session_state.node_app_cache["G"])

            open_rendered_network()
            # st.write(node_attributes)

def run_sub_node_app():
# st.write(node_graph.nodes[78581])
    initialize_session_state_vars_n()
    run_node_app()
    status_bar(st.sidebar)
