import streamlit as st


# define pages
pg = st.navigation([
    st.Page("_pages/home.py", title="Home", icon="🌎"),
    st.Page("_pages/page_1.py", title="Analyse temporelle", icon="💹"),
    st.Page("_pages/adresses.py", title="API adresses", icon="🌎"),
])

# pour lancer le sous-processus
pg.run()
