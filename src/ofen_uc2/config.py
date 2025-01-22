import os
import pathlib

# Ordner
ROOT_DIR = pathlib.Path(
    os.path.split(pathlib.Path(__file__).parent.parent.resolve())[0]
)
#ROOT_DIR = pathlib.Path("D:\Github\car_anomalies\SDSC_usecase_car_anomalies")
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PREPARED_DATA_DIR = DATA_DIR / "prepared"
RESULTS_DIR = ROOT_DIR / "results"

# Dataframes
PATH_ANOMALIES_DF = PREPARED_DATA_DIR / "anomalies.csv"
PATH_TRANSACTIONS_DF = PREPARED_DATA_DIR / "transactions.csv"

# Visualisationen
PATH_TRANSACTION_VIZ = str(RESULTS_DIR / "grafik_transaktionen.html")
PATH_ANOMALY_VIZ = str(RESULTS_DIR / "grafik_anomalien_{}.html")

# Spalten für welche Anomalien gemessen werden sollen
ANOMALY_SUPPORTED_COLS = [
    "co2",
    "anzfz_total",
    "leergewicht",
    "co2_massgebend",
    "ziel",
    "ziel_abw",
    "sanktion_final",
    "anteil_lev"
]
