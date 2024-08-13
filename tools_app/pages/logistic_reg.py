import streamlit as st

from datetime import datetime, timedelta

from include.logistic_regression import *
from include.app_config import *

if 'start_date' not in st.session_state:
    st.session_state['start_date'] = (datetime.today() - timedelta(days=365*5))
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = datetime.today()
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = 'AAPL'
if 'ticker_name' not in st.session_state:
    st.session_state['ticker_name'] = 'Apple'

with st.sidebar.form("select_ticker", clear_on_submit=True):

    name_ = st.selectbox(
        label="Choix de la Valeur", 
        options=[(lambda x: x['name'])(x) for x in WATCH_LIST], 
        key=[(lambda x: x['ticker'])(x) for x in WATCH_LIST])
    start_date_ = st.date_input("Date début", st.session_state['start_date'])
    end_date_ = st.date_input("Date fin", st.session_state['end_date'] )
    clicked_ = st.form_submit_button(label="Appliquer")
    if clicked_ :
        st.session_state['ticker'] = get_ticker_from_name(name_)
        st.session_state['ticker_name'] = name_
        st.session_state['start_date'] = start_date_
        st.session_state['end_date'] = end_date_
        st.rerun()

st.markdown(f"## {st.session_state['ticker_name']} ({st.session_state['ticker']})")


df = load_ticker_history(st.session_state['ticker'])

# filtre sur la date
df = df.loc[(df.Date > st.session_state['start_date'].strftime('%Y-%m-%d')) & (df.Date < st.session_state['end_date'].strftime('%Y-%m-%d'))]

min_date = df.Date.min()
max_date = df.Date.max()

df=Logarithmic_regression(df)

st.pyplot(plot_chart(df,  st.session_state['ticker'],  st.session_state['ticker_name']), clear_figure=True, use_container_width=True)