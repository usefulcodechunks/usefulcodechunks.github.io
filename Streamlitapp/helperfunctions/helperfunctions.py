import streamlit as st
import pandas as pd
import random

def make_clickable(link, text_to_display="Link"):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(link, text_to_display)

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
    return template.format(search_value=search_value)

def make_google_link(search_parameter):
    '''
        search_parameter: dictionary of type search paramter
    '''
    template = "https://www.google.com/search?q='{search_value}'"
    return template.format(search_value=search_value)

def generate_random_emoji(id=None):
    emoji_list='''🎧🥇🕋🗼🎨💎🛷🏥💾📎🏢🏩🎣🚃🔦🎠📯🏉📔🏋️⚱️🎮🎳🏬🧗‍♂️💳🚓💊🛒🚦⚽️⚖️🏺🔏🏋️‍♀️🏓🚝🧯🚢🎢🎀📜⌛️🧗🥅💻🪕✉️🚇⏲🗓🛳🧿🤼‍♀️🏠🛥🪧⌚️🧩🧘‍♂️📚🏄‍♀️🔒⛳️🛻🤼‍♂️🌆🎐💈🧻🖊🎊🏡🚣‍♀️🖨⛲️📨🧭🚒🔖💷🚚🎤🚡🛸🏗📱🎟📹📤🛤🚣🕹🧺🏣🏇🚁✈️🗝🏸🏞🏖🚛📐📌🪜🧴🛫📫🤽🚧🗡🚎🏌️‍♂️🛌🏪🪠⛸🤹‍♂️🪂☎️♟💡📻🥉🪔📙🏹🪆🛴🖥🌁🗾📁🤺🚤🖇⚗️🏀🔮🌃🌄🚉📡🧨🛹📬🌉🗿🚆🛠✂️🎙✒️🚙🪟🚟🏨🪝🛵🎯🥁🤸‍♀️🚵🧽🤾‍♀️🏐🛀🤽‍♂️🚕🚘🏰🚈🎞🩹⛹️⏳🔫🗂🏆🎾🏋️‍♂️🧰🏏🧷🎗🗄🩰💾🏦🔪🕍🗑📇🪤🚽📞🏥🚖💸🚲🪁🎨🪄🎖🤼🎹🖲🏊🛰📧⚙️🪒🏄‍♂️🧮🚋🥊💵🛶🥈💰🪃🚜🖼🥌🏊‍♂️🛡🌅⏰🌋🎆🤽‍♀️🛁🚨📺🎑💿🥎🏟🤿🎇🌇⚒🏘🗻🪑📗🤸🔭🕌⌨️⛏🎫🧹📍🏤🔨🏊‍♀️⚔️🏭🚌🧫🧗‍♀️📃🖱💴🧲🎛🕰🚴‍♀️🎥🎎🚂📋🛬📆📰🧾🏜🔑🦼📉🏅🕋🏄🚥🏌️‍♀️📿💽📷🛍🏯⛩⛵️🏌️🧼📀⏱🔓📲🛺🎁🕳🪗🤹🏔📸📒💉⚾️📄🚊🎏⛹️‍♀️🚴🧪📼✏️🌡⛽️📩🔋🎬🏵🎪💶🪙🪦🪣🤸‍♂️🏚🛼⛹️‍♂️🔍🎼🔩⛺️🏒🦠🚠📅🔐🚗🏙📂🎧🪓📦📠🚣‍♂️🔬🏷💌🎸🔎🚏📘🎚🧘‍♀️🔗🎷🚅📈🚞🖍🚿🤾‍♂️📊🛖🦯🎻🪅📮🚍🛏🎺🏈🗳🎡🖌🚀📓🎿🏮🤹‍♀️📑🦽💣📥⛴⛪️🚬🎽⛷🚄🪘🔌📪🩺🪀🤾💺🚐🚰🛩🚑🖋🏫🧬🎉⚓️🎱🧱🔧🚵‍♀️📭🎈🧸🏂🧘🥏🪛🏑🥍📖📟🚴‍♂️🏎🎭🌠🧧🌌🛕📏⛰💒🎰🎲🚔🛋📕🗜📝🗽🏕🥋🩸🚵‍♂️'''
    if(id is not None):
        return emoji_list[id]
    else:
        return random.choice(list(emoji_list))
