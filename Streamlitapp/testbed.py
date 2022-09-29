import streamlit as st
import pandas as pd

import json


jdata = json.loads(jsondata)
df = pd.DataFrame(jdata)
