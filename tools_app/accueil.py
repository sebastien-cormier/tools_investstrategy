import streamlit as st

from datetime import datetime

import pandas as pd
import numpy as np

from include.app_config import *
from include.es_client import get_es_client
from include.es_queries import get_leaderboard, get_games

es_client = get_es_client()

st.markdown("# Accueil")
st.sidebar.markdown("# Accueil")
