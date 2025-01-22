import matplotlib
import matplotlib.cm as cm
import networkx as nx
import numpy as np
import pandas as pd
from pyvis.network import Network

from ofen_uc2.config import RESULTS_DIR


def create_visualisation(
    df: pd.DataFrame,
    out_file: str = str(RESULTS_DIR / "grafik_transaktionen.html")
):
    """
    Visualisiert einen Graphen, welche Transaktionen zwischen Fahrzeughändler aufzeigt.

    :param data: Dataframe mit relevanten Datenpunkten die wir visualisieren möchten.
    :param out_file: Wo der Graph als HTML Datei gespeichert werden soll,
                     defaults to str(RESULTS_DIR / "grafik_transaktionen.html")
    """
    # Definiere Graphen
    G = nx.from_pandas_edgelist(
        df,
        source="Exporteur",
        target="Importeur",
        edge_attr="anzahl_autos",
        create_using=nx.DiGraph()
    )

    # Visualisiere Graphen
    net = Network(
        '570px',
        '1400px',
        directed=True,
        notebook=True,
    )
    net.barnes_hut()
    net.from_nx(G)

    # Remove white-ish Blues from cmap
    orig_cmap = cm.Blues
    colors = orig_cmap(np.linspace(0.1, 1, 40))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)

    # Metadaten der Edges
    for edge in net.get_edges():
        v = edge["anzahl_autos"]
        rgba = cmap(v)
        hex = matplotlib.colors.rgb2hex(rgba)
        edge["color"] = hex
        edge["width"] = 35
        edge["title"] = f"Autos: {int(v):,}"
        edge["label"] = f"{int(v):,}"
        edge["font"] = {"size": 100}
        edge["arrowStrikethrough"] = False

    # Metadaten der Nodes
    for node_idx in net.get_nodes():
        node = net.get_node(node_idx)
        node["size"] = 50
        node["color"] = "#191970"
        node["title"] = f"Autohändler: {int(node_idx)}"
        node["label"] = str(node_idx)
        node["font"] = {"size": 100}

    # Speichere den Graphen
    net.show(out_file)
