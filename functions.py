# import des librairies
import requests
import pandas as pd
from shapely import Point
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import st_folium

# load dataset
def load_velomag(method='api'):
    if method == 'api':
        # declare server adress
        adr_serv = "https://portail-api-data.montpellier3m.fr"
        # declare end point
        end_point = "/bikestation?limit=1000"
        # get dataset
        response = requests.get(adr_serv+end_point)
        if response.status_code == 200 :
            # return dataset to df
            return pd.DataFrame(response.json())
        else :
            mess = f"Code erreur du serveur API {response.status_code, adr_serv}: le dataset ne peut pas être chargé !"
            return mess
    elif method == 'local':
        df = pd.read_json("data/velomag_demo.json")
        return df
    else :
        print ("Le dataset n'a pas pu être chargé, vérifier le paramètre method de la fonction load_velomag()")



# transform velomag dataset
def processed_velomag(dataset, method='api'):
  # build interest columns
    if method=='api':
        dataset['commune'] = dataset['address'].map(lambda x: x['value']['addressLocality'])
        dataset['lieu'] = dataset['address'].map(lambda x: x['value']['streetAddress'])
        dataset['xy'] = dataset['location'].map(lambda x: x['value']['coordinates'])
        dataset['freeSlot'] = dataset['freeSlotNumber'].map(lambda x: x['value'])
        dataset['availableBike'] = dataset['availableBikeNumber'].map(lambda x: x['value'])
        dataset['status'] = dataset['status'].map(lambda x: x['value'])
        dataset['totalSlot'] = dataset['totalSlotNumber'].map(lambda x: x['value'])
        dataset['geometry'] = dataset['xy'].map(lambda x: Point(x))
        # eliminate useless columns
        del dataset['address'], dataset['location'], dataset['freeSlotNumber']
        del dataset['availableBikeNumber'], dataset['totalSlotNumber'], dataset['xy']
    elif method == 'local':
        dataset['commune'] = dataset['address'].map(lambda x: x['addressLocality'])
        dataset['lieu'] = dataset['address'].map(lambda x: x['streetAddress'])
        dataset['xy'] = dataset['location'].map(lambda x: x['coordinates'])
        dataset['freeSlot'] = dataset['freeSlotNumber']
        dataset['availableBike'] = dataset['availableBikeNumber']
        dataset['totalSlot'] = dataset['totalSlotNumber']
        dataset['geometry'] = dataset['xy'].map(lambda x: Point(x))
        # eliminate useless columns
        del dataset['address'], dataset['location'], dataset['freeSlotNumber']
        del dataset['availableBikeNumber'], dataset['totalSlotNumber'], dataset['xy']
    else :
        print('erreur de paramètre !')
    # return gdf
    return gpd.GeoDataFrame(dataset, geometry='geometry',crs='wgs84')

# get velomag
def get_velomag(method='api'):
    if method == 'api':
        velomag = load_velomag(method=method)
        if type(velomag)==str:
            # print(velomag)
            return velomag
        else:
            velomag = processed_velomag(dataset=velomag,method=method)
            return velomag
    elif method == 'local':
        velomag = load_velomag(method=method)
        velomag = processed_velomag(dataset=velomag,method=method)
        return velomag


# map velomag
def mapped_velomag(dataset):
    map = folium.Map(location=[43.6079, 3.8790], tiles="CartoDB Positron", zoom_start=12)
    folium.GeoJson(
        dataset,
        name="Velomagg Stations",
        zoom_on_click=True,
        marker=folium.Marker(icon=folium.Icon(icon='bicycle',prefix='fa')),
        tooltip=folium.GeoJsonTooltip(fields=["lieu", "freeSlot", "availableBike"],aliases=['Lieu','Places dispo', 'Vélos dispo']),
        popup=folium.GeoJsonPopup(fields=["lieu", "freeSlot", "availableBike"]),
    ).add_to(map)
    return map

# get indicators
def get_indicators(dataset,indicator):
    '''
    4 indicators : totalSlot, freeSlot, availableBike, totalStation

    '''
    if indicator == 'totalSlot':
        number = dataset['totalSlot'].sum()
    elif indicator == 'freeSlot':
        number = dataset['freeSlot'].sum()
    elif indicator == 'availableBike':
        number = dataset['availableBike'].sum()
    elif indicator =='totalStation':
       number = dataset.shape[0]
    else :
        number = "4 indicators available : totalSlot, freeSlot, availableBike, totalStation"
    return number

def display_indicators(dataset):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.metric('Vélostations',value=get_indicators(dataset=dataset,indicator='totalStation'))
        with col2:
            st.metric('Places disponibles ',value=get_indicators(dataset=dataset,indicator='freeSlot'))
        with col3:
            st.metric('Vélos disponibles',value=get_indicators(dataset=dataset,indicator='availableBike'))

def display_map(dataset):
    col1,col2,col3 = st.columns([0.3,0.7,0.15])
    with col2:
        st_folium(fig=mapped_velomag(dataset=dataset),height=500)



### FUNCTIONS PAGE 1
def load_historic(idStation, start_date, end_date):
    # declare server adress
    adr_serv = "https://portail-api-data.montpellier3m.fr"
    # declare end point
    end_point = "/bikestation_timeseries/"
    # param
    params = idStation + "/attrs/availableBikeNumber?fromDate="+start_date.strftime(format="%Y-%m-%dT%H:%M:%S")+"&toDate="+end_date.strftime(format="%Y-%m-%dT%H:%M:%S")
    response = requests.get(adr_serv+end_point+params)
    if response.status_code == 200 :
    # return dataset to df
        return pd.DataFrame(response.json())
    else :
        mess = "Impossible d'accéder au serveur, le dataset ne peut pas être chargé"
        return mess