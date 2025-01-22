from typing import Union

from colorcet import cm
import holoviews as hv
from holoviews import opts
import pandas as pd
import numpy as np


hv.extension('bokeh')
hv.output(size=200)


def create_visualisation(
    df: pd.DataFrame,
    col: str,
    threshold: float,
    year: Union[int, str] = "Alle"
) -> hv.core.overlay.Overlay:
    """
    Visualisiert ein Leistendiagramm der verschiedenen Fahrzeughändler.

    :param df: Dataframe mit relevanten Datenpunkten die wir visualisieren möchten.
    :param col: Attribute zu visualisieren (Spalte in Dataframe).
    :param threshold: Grenzwert, welcher Anomalien definiert
    :param year: Jahr, welches man visualisieren möchte, default ist "Alle" (also alle Jahre)
    :return: Visualisation
    """
    
    # Das Jahr filtern, falls nicht alle gezeigt werden sollen
    if year != "Alle":
        df = df.query(f"jahr == {year}").copy()
    
    # Grenzwert, welcher Anomalien definiert
    condition = threshold != 0
    df["above_threshold"] = None
    if condition:
        df["above_threshold"] = np.where(df[f"{col}_prct_diff"].abs() >= threshold, 1, 0)

    # Spalten-namen und deren besser formulierten Bezeichnungen
    d_map = {
        "anzfz_total": "Importierte Autos",
        "co2": "CO-2 Flotten-Emission",
        "leergewicht": "Leergewicht",
        "co2_massgebend": "Massgebende CO2-Emissionen",
        "ziel": "CO2-Zielvorgabe",
        "ziel_abw": "CO2-Zielabweichung",
        "sanktion_final": "Sanktion",
        "anteil_lev": "Anteil von Low Emission Vehicles"
    }
    assert col in d_map.keys(), "Ausgewähltes Attribute ist nicht in d_map"
    col_name = d_map.get(col)

    # Grafik wird definiert
    hv_bars = hv.Bars(
        df,
        # x-axis
        kdims=['jahr', 'nameeg'],
        # Was auf y-axis in in hover tools gezeigt werden soll
        vdims=[f"{col}_prct_diff", col, f"{col}_prev", "above_threshold"]
    )
    hv_line = hv.HLine(0)
    hv_plot = hv_bars * hv_line
    # Einstellungen
    hv_bars.opts(
    opts.Bars(
        color="above_threshold" if condition else "nameeg",
        cmap="Accent" if condition else cm['bmy'],
        width=600,
        height=300,
        colorbar=False,
        tools=['hover'],  # Default hover tool
        xrotation=90,
        show_legend=False,
    )
)

    """
    hv_bars.opts(
        opts.Bars(
            # Definiert Farbe der Balken
            color="above_threshold" if condition else "nameeg",
            # https://colorcet.holoviz.org/
            # Welche Farbtöne zu verwenden sind
            cmap="Accent" if condition else cm['bmy'],
            width=600,
            height=300,
            colorbar=False,
            tools=['hover'],
            xrotation=90,
            show_legend=False,
            # Welche Informationen im hover tool gezeigt werden sollen
            hover_tooltips=[
                ("Name", "@nameeg"),
                ("Prozentuelle Differenz", "@{" + f"{col}_prct_diff" + "}{0,0} %"),
                (col_name, "@{" + col + "}{0,0}"),
                (f"{col_name} im Vorjahr", "@{" + f"{col}_prev" + "}{0,0}"),
            ]
        )
    )
"""
    hv_plot.opts(opts.HLine(color='black', line_width=2))

    hv_plot.opts(
        fontsize={'title': 16, 'labels': 12, 'xticks': 10, 'yticks': 10},
        xlabel='Jahr und Importeur',
        ylabel=f'Prozentuale Veränderung zum Vorjahr [%]\n{col}',
    )

    # Grenzwerte als horizontale Linien zeigen
    if condition:
        hv_plot = (
            hv_plot *
            hv.HLine(threshold).opts(color="red", line_width=2, line_dash="dotted") *
            hv.HLine(-threshold).opts(color="red", line_width=2, line_dash="dotted")
        )

    return hv_plot
