from pyvis.network import Network
from IPython.core.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Node Demo",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded",
)

def render_node_app(render_object):
    render_object.title("Demo Node App")

    color_list = ['red','green','blue','yellow','purple']
    alt_color_list = ['#24CCCC','#24C6BC' ,'#24C0AC' ,'#24BA9C' ,'#24B48C' ,'#24847C' ,'#24546C']

    def create_attribute_hash():
        return True


    def generate_random_node(G):
        random_id = random.randint(0, 100)
        random_weight = random.randint(1, 5)
        random_color = random.choice(alt_color_list)
        G.add_node(random_id, size=random_weight, title=str(random_id), color=random_color)

    def generate_random_edge(G):
        random_node_from = random.choice(list(G.nodes))
        random_node_to = random.choice(list(G.nodes))
        while(random_node_from == random_node_to):
            random_node_to = random.choice(list(G.nodes))
        random_weight = random.randint(1, 5)
        G.add_edge(random_node_from, random_node_to, weight=random_weight)


    number_of_nodes = render_object.slider("Number of nodes?",0 , 200, 10)
    number_of_edges = render_object.slider("Number of edges?",1,400, 20)

    G = nx.DiGraph() # initilize the graph bidirectional

    for x in range(number_of_nodes):
        generate_random_node(G)

    for x in range(number_of_edges):
        generate_random_edge(G)

    render_demo = render_object.button("Render Sample Node Network")

    if(render_demo):
        nt = Network('500px', '500px')
        nt.from_nx(G)

        nt.inherit_edge_colors(False)
        for ix in nt.get_edges():
            ix["width"] = ix["weight"]
        nt.write_html('HTMLfileoutputs/demo.html')
        # print(nt)
        # display(HTML('demo.html'))
        HtmlFile = open("HTMLfileoutputs/demo.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height=700)

render_node_app(st)
