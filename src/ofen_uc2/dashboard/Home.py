"""Definiert das Dashboard"""
import streamlit as st

import sys
import os
sys.path.append(os.path.abspath("D:/Github/car_anomalies/SDSC_usecase_car_anomalies/src"))

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    # layout="wide",
)
# Titel des Dashboards
st.title("Projekt: Fahrzeugdatenbank")
# Info-text: erklärt, was das Dashboard bewirken möchte
st.markdown(
    """
    **Dieses Dashboard unterstützt die Sektion EV im Vollzug der
    CO2-Emissionsvorschriften mit Hilfe von Monitoring und dem Identifizieren allfälliger Anomalien.**
    """
)
st.markdown("""
    Bitte wählen Sie auf der linken Seite eines der folgenden Dashboards:
    - Anomalien
    - Fahrzeughandel    
    """)

