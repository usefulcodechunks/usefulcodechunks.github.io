import streamlit as st

from helperfunctions.helperfunctions import (
    make_linkedin_link,
    make_crunchbase_link,
    make_google_link,
    make_clickable,
    generate_random_emoji
    )

def default_home_view(render_object):
    render_object.write("home .....")


# def generate_links_demo(render_object):
