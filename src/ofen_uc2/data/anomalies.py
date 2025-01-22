import pandas as pd

from ofen_uc2.config import RAW_DATA_DIR, PREPARED_DATA_DIR, ANOMALY_SUPPORTED_COLS


def prepare_data(
    in_file: str = RAW_DATA_DIR / "Testdaten_Vollzugsresultate_LNF_2021 - 2023.csv",
    out_file: str = PREPARED_DATA_DIR / "anomalies.csv",
    columns: list[str] = ANOMALY_SUPPORTED_COLS
):
    """Daten vorbereiten

    :param in_file: Input CSV Datei, defaults to RAW_DATA_DIR/"Testdaten_Vollzugsresultate_LNF_2021 - 2023.csv"
    :param out_file: Wo Ergebnisse gespeichert werden sollen, defaults to PREPARED_DATA_DIR/"anomalies.csv"
    :param columns: Spalten, für welche man den prozentuellen Unterschied zum Vorjahr messen sollte,
                    defaults to ANOMALY_SUPPORTED_COLS
    """

    df_vzr = pd.read_csv(in_file, delimiter=";")

    # Wir können keine Entwicklug messen für Importeure mit Daten zu nur einem Jahr
    n_jahre_pro_importeur = (
        df_vzr
        .groupby("nameeg")
        ["jahr"]
        .nunique()
    )
    mask = (n_jahre_pro_importeur > 1).index
    df_vzr = df_vzr.loc[lambda x: x["nameeg"].isin(mask)].copy()

    # Prozentuelle Veränderung zum Vorjahr
    for col in columns:
        df_vzr[f"{col}_prev"] = df_vzr.groupby("nameeg")[col].shift(1)
        df_vzr[f"{col}_prct_diff"] = ((df_vzr[col] - df_vzr[f"{col}_prev"]) / df_vzr[f"{col}_prev"]) * 100

    # Daten-attribute die wir visualisieren möchten
    df_vzr.sort_values(by=["nameeg", "jahr"], inplace=True)
    df_vzr.to_csv(out_file, index=False)
