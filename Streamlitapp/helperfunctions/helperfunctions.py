import streamlit as st
import pandas as pd
import random

def make_clickable(render_object, link, text_to_display="Link"):
    # target _blank to open new window
    HTML_STRING = '<a class="css-wq85zr" style="text-decoration: none;" target="_blank" href="{0}">{1}</a>'.format(link, text_to_display)
    render_object.markdown(HTML_STRING, unsafe_allow_html=True)



def make_linkedin_link(search_value):
    '''
        search_parameter: dictionary of type search paramter
    '''
    template = "https://www.linkedin.com/search/results/all/?keywords={search_value}"
    return template.format(search_value=search_value)

def make_crunchbase_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''
    template = "https://www.crunchbase.com/textsearch?q={search_value}"
    return template.format(search_value=search_parameter)

def make_google_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''
    template = "https://www.google.com/search?q='{search_value}'"
    return template.format(search_value=search_parameter)

def generate_random_emoji(id=None):
    emoji_list='''🎧🥇🕋🗼🎨💎🛷🏥💾📎🏢🏩🎣🚃🔦🎠📯🏉📔🏋️⚱️🎮🎳🏬🧗‍♂️💳🚓💊🛒🚦⚽️⚖️🏺🔏🏋️‍♀️🏓🚝🧯🚢🎢🎀📜⌛️🧗🥅💻🪕✉️🚇⏲🗓🛳🧿🤼‍♀️🏠🛥🪧⌚️🧩🧘‍♂️📚🏄‍♀️🔒⛳️🛻🤼‍♂️🌆🎐💈🧻🖊🎊🏡🚣‍♀️🖨⛲️📨🧭🚒🔖💷🚚🎤🚡🛸🏗📱🎟📹📤🛤🚣🕹🧺🏣🏇🚁✈️🗝🏸🏞🏖🚛📐📌🪜🧴🛫📫🤽🚧🗡🚎🏌️‍♂️🛌🏪🪠⛸🤹‍♂️🪂☎️♟💡📻🥉🪔📙🏹🪆🛴🖥🌁🗾📁🤺🚤🖇⚗️🏀🔮🌃🌄🚉📡🧨🛹📬🌉🗿🚆🛠✂️🎙✒️🚙🪟🚟🏨🪝🛵🎯🥁🤸‍♀️🚵🧽🤾‍♀️🏐🛀🤽‍♂️🚕🚘🏰🚈🎞🩹⛹️⏳🔫🗂🏆🎾🏋️‍♂️🧰🏏🧷🎗🗄🩰💾🏦🔪🕍🗑📇🪤🚽📞🏥🚖💸🚲🪁🎨🪄🎖🤼🎹🖲🏊🛰📧⚙️🪒🏄‍♂️🧮🚋🥊💵🛶🥈💰🪃🚜🖼🥌🏊‍♂️🛡🌅⏰🌋🎆🤽‍♀️🛁🚨📺🎑💿🥎🏟🤿🎇🌇⚒🏘🗻🪑📗🤸🔭🕌⌨️⛏🎫🧹📍🏤🔨🏊‍♀️⚔️🏭🚌🧫🧗‍♀️📃🖱💴🧲🎛🕰🚴‍♀️🎥🎎🚂📋🛬📆📰🧾🏜🔑🦼📉🏅🕋🏄🚥🏌️‍♀️📿💽📷🛍🏯⛩⛵️🏌️🧼📀⏱🔓📲🛺🎁🕳🪗🤹🏔📸📒💉⚾️📄🚊🎏⛹️‍♀️🚴🧪📼✏️🌡⛽️📩🔋🎬🏵🎪💶🪙🪦🪣🤸‍♂️🏚🛼⛹️‍♂️🔍🎼🔩⛺️🏒🦠🚠📅🔐🚗🏙📂🎧🪓📦📠🚣‍♂️🔬🏷💌🎸🔎🚏📘🎚🧘‍♀️🔗🎷🚅📈🚞🖍🚿🤾‍♂️📊🛖🦯🎻🪅📮🚍🛏🎺🏈🗳🎡🖌🚀📓🎿🏮🤹‍♀️📑🦽💣📥⛴⛪️🚬🎽⛷🚄🪘🔌📪🩺🪀🤾💺🚐🚰🛩🚑🖋🏫🧬🎉⚓️🎱🧱🔧🚵‍♀️📭🎈🧸🏂🧘🥏🪛🏑🥍📖📟🚴‍♂️🏎🎭🌠🧧🌌🛕📏⛰💒🎰🎲🚔🛋📕🗜📝🗽🏕🥋🩸🚵‍♂️'''
    if(id is not None):
        return emoji_list[id]
    else:
        return random.choice(list(emoji_list))
