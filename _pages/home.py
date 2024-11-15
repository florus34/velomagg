import streamlit as st
from functions import *
from streamlit_autorefresh import st_autorefresh
from streamlit_folium import st_folium

#### CONFIG DE LA PAGE
st.set_page_config(page_title="Velomagg",page_icon=":v:",layout="wide")

#### TITRE DE LA PAGE
st.title("Vélomagg libre-service, pour la location de vélos")

#### SIDEBAR
# activate real time
real_time = st.sidebar.toggle("Activate real time")
if real_time:
    interval = st.sidebar.slider("Select a refreshing interval (s)",2,60)
    # define autorefresh
    count = st_autorefresh(interval=interval*1000, limit=100, key="refresh")
# insertion d'une image
st.sidebar.image("img/Velomagg.jpg")
# insertion expander
with st.sidebar.expander(label='A propos ...',icon="🔦"):
    code_html ='''
        <p style = 'font-size:12px'>
        Localisation des vélostations et disponibilité des vélos.
        </p>
                '''
    st.html(code_html)

#### DECLARE SESSION STATE
if 'idStation' not in st.session_state:
    st.session_state['idStation'] = None


#### GET DATASET BY API
velomag = get_velomag(method='api')

if type(velomag) == gpd.GeoDataFrame:
    ### build idStation session state for page 2
    st.session_state['idStation'] = dict (zip(velomag['id'].to_list(), velomag['lieu'].to_list()))
    # st.session_state['idStation'] = velomag['id'].to_list()

    #### DISPLAY INDICATORS
    display_indicators(dataset=velomag)
    #### DISPLAY MAP
    # st_data = st_folium(fig=mapped_velomag(dataset=velomag),height=500)
    display_map(dataset=velomag)

else :
    st.warning(velomag)
    data_demo = st.toggle("Charger donnée de démonstration")
    if data_demo:
        #### GET LOCAL DATASET
        velomag_local = get_velomag(method='local')

        display_indicators(dataset=velomag_local)
        #### DISPLAY MAP
        st_data = st_folium(fig=mapped_velomag(dataset=velomag_local),height=500)
