"""Definiert die Fahrzeughandel-Seite."""
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from ofen_uc2.config import PATH_TRANSACTION_VIZ
from ofen_uc2.dashboard.config import TRANSACTIONS_DF
from ofen_uc2.visualisations.transactions import create_visualisation


st.set_page_config(
    page_title="Fahrzeughandel",
    page_icon="🚗",
    layout="wide",
)
st.title("Fahrzeughandel zwischen Importeuren")
st.markdown("""
Dieses Dashboard visualisiert die absolute Anzahl der gehandelter Fahrzeuge zwischen Importeuren um aufzuzeugen, wie sie interagieren.
""")
st.divider()
st.subheader("Grafik")

if not os.path.exists(PATH_TRANSACTION_VIZ):
    create_visualisation(data=TRANSACTIONS_DF, out_file=PATH_TRANSACTION_VIZ)

content = open(PATH_TRANSACTION_VIZ, "r").read()
components.html(content, width=1400, height=600)
with st.expander("Info"):
    st.info(
        """
        Punkte representieren einzelne Fahrzeughändler (Importeure) und die Verknüpfungen wie sie interagieren.\n
        Die Art der Interaktion (Ankauf vs Verkauf) wird mit der Richtung der Pfeile dargestellt.\n
        Pfeile, welche zu einem Punkt zeigen, stellen einen Ankauf dar.
                
        Jeder Punkt ist mit der ID des Fahrzeughändlers beschriftet und jede Verknüpfung mit der Anzahl der gehandelten Autos.
        
        Je mehr Autos gehandelt werden, desto dunkel-blauer die Verbindung.
        """,
        icon="ℹ️"
    )

st.divider()
st.subheader("Datensatz")
st.dataframe(TRANSACTIONS_DF)
