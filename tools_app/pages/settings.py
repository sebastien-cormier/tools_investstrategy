import streamlit as st
import yfinance as yf

from include.tickers_func import *

df_tickers = load_tickers()

st.markdown(f"## Paramétrage")
st.markdown(f"### Gestion des valeurs suivies")

tab1, tab2 = st.tabs(["Ajouter une valeur", "Supprimer une valeur"])

with tab1 :
    with st.form("add_ticker", clear_on_submit=True) :

        ticker_code_ = st.text_input("Ajouter une valeur pas son ticker")

        clicked_ = st.form_submit_button(label="Rechercher")
        if clicked_ :
            if is_ticker_watched(df_tickers, ticker_code_) :
                st.markdown("Vous suivez déjà cette valeur.")
            else :
                yf_ticker_ = yf.Ticker(ticker_code_)
                if yf_ticker_.info['trailingPegRatio'] is None :
                    st.markdown("Aucune valeur trouvée avec ce code.")
                else :
                    st.session_state['selected_ticker'] = yf_ticker_

with tab2 :
    with st.form("remove_ticker", clear_on_submit=True) :
        ticker_to_remove = st.selectbox(
            label = "Choix de la Valeur",
            options = df_tickers['ticker']
        )
        clicked_ = st.form_submit_button(label="Supprimer")
        if clicked_ :
            remove_ticker_to_watch_list(df_tickers, ticker_to_remove)
            st.rerun()

if 'selected_ticker' in st.session_state:
    
    container_ = st.container(border=True)

    container_.markdown(f"#### {st.session_state['selected_ticker'].info['shortName']}")

    col1, coL2 = container_.columns(2)
    col1.markdown(f" - __Nom complet__    : {st.session_state['selected_ticker'].info['longName']}")
    col1.markdown(f" - __Pays__           : {st.session_state['selected_ticker'].info['country']}")
    col1.markdown(f" - __Site Internet__  : {st.session_state['selected_ticker'].info['website']}")
    col1.markdown(f" - __Indutrie__       : {st.session_state['selected_ticker'].info['industry']}")
    coL2.markdown(f" - __Secteur__        : {st.session_state['selected_ticker'].info['sector']}")
    coL2.markdown(f" - __Nb employés__    : {st.session_state['selected_ticker'].info['fullTimeEmployees']}")
    coL2.markdown(f" - __Capitalisation__ : {st.session_state['selected_ticker'].info['marketCap']}")
    coL2.markdown(f" - __Devise__         : {st.session_state['selected_ticker'].info['currency']}")

    
    with st.form("add_ticker_df", clear_on_submit=True) :
        st.markdown(f"Voulez-vous ajouter {st.session_state['selected_ticker'].info['shortName']} aux valeurs suivies ?")
        clicked_add_ticker_ =  st.form_submit_button(label=":thumbsup: Oui !")
        if clicked_add_ticker_ :
            add_ticker_to_watch_list(df_tickers, st.session_state['selected_ticker'])
            st.toast(f'{st.session_state['selected_ticker']} a été ajouté à la liste de suivi !')
            st.rerun()
    clicked_cancel_ = st.button(":thumbsdown: Revenir")
    if clicked_cancel_ :
        del st.session_state['selected_ticker']

st.divider()

st.markdown("### Valeurs suivies :")
if df_tickers.shape[0] == 0 :
    st.markdown("_Aucune valeur suivie_")
else :
    st.dataframe(df_tickers[['ticker', 'shortName']].set_index(df_tickers.columns[0]))