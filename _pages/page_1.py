# import des librairies
import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from functions import *

# titre de la page
st.title("Analyse données temporelles ")

if st.session_state['idStation'] != None:

# params
    station = st.sidebar.selectbox('Choose a station', 
                        st.session_state['idStation'].keys(), format_func= (lambda x: st.session_state['idStation'][x])
            )  

    max_value = datetime(datetime.today().date().year,datetime.today().date().month,datetime.today().date().day)
    interval = st.sidebar.slider('Choose an interval',
                        min_value=datetime(2020,1,1),
                        max_value=max_value,
                        value=(datetime(2023,1,1),datetime(2024,1,1)),
                        format="DD/MM/YYYY")

    st.write(interval[0], interval[1])


    load = st.sidebar.button('Load dataset')
    if load:
        st.write(load_historic(idStation=station, start_date=interval[0], end_date=interval[1]))

else:
    st.warning("Pas de données à afficher")