import pandas as pd

from ofen_uc2.config import RAW_DATA_DIR, PREPARED_DATA_DIR

def prepare_data(
    in_file: str = RAW_DATA_DIR / "Testdaten_Einzelfahrzeugdaten_Q3_2024_LNF_extern_V2.xlsx",
    out_file: str = PREPARED_DATA_DIR / "transactions.csv"
):
    """Daten vorbereiten.

    :param in_file: Input CSV Datei, defaults to RAW_DATA_DIR/"Testdaten_Einzelfahrzeugdaten_Q3_2024_LNF_extern_V2.xlsx"
    :param out_file: Wo Ergebnisse gespeichert werden sollen, defaults to PREPARED_DATA_DIR/"transactions.csv"
    """

    data = pd.read_excel(in_file)

    ds = (
        data
        # Spalten umbenennen
        .rename(columns={"ANAMEABTRP": "Exporteur", "AIMPNAME": "Importeur"})
        # Aggregation auf Exporteur - Importeur level
        .groupby(["Exporteur", "Importeur"], dropna=True, as_index=False)
        .agg(anzahl_autos = ("AMARKE", "count"))
    )
    
    ds["Exporteur"] = ds["Exporteur"].astype(int)
    ds["Importeur"] = ds["Importeur"].astype(int)

    ds.to_csv(out_file, index=False)
