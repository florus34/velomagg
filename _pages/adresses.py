import streamlit as st
import requests


api_adr = "https://api-adresse.data.gouv.fr/search/?q="

def build_url(params, api_adr = api_adr):
    if len(params)==1:
        api_adr = api_adr + params[0]
        url = api_adr
        return url
    else :
        c = 0
        for p in params:
            if c==0:
                c = c+1
                api_adr = api_adr + p
            else :
                 api_adr = api_adr + '+'+ p
        url = api_adr
        return url
    
def display_dropdown(url):
    response = requests.get(url).json()['features']
    if len(response) > 0:
        items = [response[i]['properties']['label'] for i in range (len(response))]
    return st.selectbox("Rues trouvées", items)

# Créer un widget text_input
text_input = st.text_input("Entrez votre texte :")

if text_input :
    user_input = text_input
    params = user_input.split(' ')

    url = build_url(params=params)
    st.write(url)
    display_dropdown(url=url)
    

