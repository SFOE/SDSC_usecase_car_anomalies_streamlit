"""Definiert die Anomalie Seite des Dashboards."""
import streamlit as st
import streamlit.components.v1 as components
import holoviews as hv

from ofen_uc2.config import PATH_ANOMALY_VIZ
from ofen_uc2.dashboard.config import ANOMALY_SUPPORTED_COLS, ANOMALIES_DF
from ofen_uc2.visualisations.anomalies import create_visualisation


renderer = hv.renderer('bokeh')

st.set_page_config(
    page_title="Anomalien",
    page_icon="📡",
    layout="wide",
)
st.title("Anomalien")
st.markdown("""
Das Dashboard zeigt Veränderungen in den Zeitreihen einzelner Importeure.\n
Grössere Veränderungen können Mittels einem Grenzwert auf sich aufmerksam gemacht werden.
Die Definition von «grössere Veränderungen» unterscheidet sich je nach ausgewählten Attribut.
""")
st.divider()
auswahl_spalte = st.selectbox(
    label="Attribut zu analysieren",
    options=ANOMALY_SUPPORTED_COLS,
    index=0
)
threshold = st.number_input("Grenzwert für prozentuelle Veränderung des Attributes (Definition von Anomalien)", min_value=0, value=0)
# Wir können nicht das erste Jahr auswählen (keine % diff) => also [1:]
available_years = list(sorted(ANOMALIES_DF["jahr"].unique()))[1:]
year = st.selectbox("Jahr", options=["Alle"] + available_years)

# Datensatz
df_to_show = (
    ANOMALIES_DF
    .loc[
        lambda x:
        (x["jahr"] >= available_years[0]) &
        (x[f"{auswahl_spalte}_prct_diff"].notna())
    ]
    .copy()
)

# Grafik muss immer wieder generiert werden weil gewisse Optionen
# nicht gespeichert werden, wenn die Grafik von der Disk gelesen wird.
hv_plot = create_visualisation(df_to_show, auswahl_spalte, threshold, year)
df_for_table = df_to_show.copy()

if threshold != 0:
    df_for_table = (
        df_for_table
        .loc[lambda x: x[f"{auswahl_spalte}_prct_diff"].abs() > threshold]
        .copy()
    )
if year != "Alle":
    df_for_table = (
        df_for_table
        .loc[lambda x: x["jahr"] == year]
        .copy()
    )

st.divider()
st.subheader("Grafik")
renderer.save(
    hv_plot,
    # Already adds HTML to filename
    PATH_ANOMALY_VIZ.replace(".html", "").format(auswahl_spalte)
)
content = open(PATH_ANOMALY_VIZ.format(auswahl_spalte), "r").read()
components.html(content, width=1400, height=700)
with st.expander("Info"):
    st.info(
        """
        Die x-Achse zeigt die letzten zwei Jahre des Datensatzes.
        Pro Jahr werden des Weiteren die einzelnen Fahrzeughändler aufgelistet.
        Ihre Reihenfolge ist pro Jahr immer die selbe.

        Die y-Achse zeigt die prozentuelle Veränderung zum Vorjahr, welche als Balken dargestellt wird.
        Jeder Fahrzeughändler hat eine eigene Farbe für den jeweiligen Balken.
        Die jeweilige Farbe bleibt über die Jahre hinweg die selbe.

        Wird ein Grenzwert gewählt, so werden zusätzlich zu den Balken zwei horizontale, rote Linien gezeigt.
        """,
        icon="ℹ️"
    )


st.divider()
st.subheader("Der gefilterte Datensatz")
st.dataframe(df_for_table)