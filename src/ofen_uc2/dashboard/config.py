import os
import pandas as pd

from ofen_uc2.config import PATH_ANOMALIES_DF, PATH_TRANSACTIONS_DF, ANOMALY_SUPPORTED_COLS
from ofen_uc2.data import anomalies, transactions

if not os.path.exists(PATH_ANOMALIES_DF):
    anomalies.prepare_data(out_file=PATH_ANOMALIES_DF, columns=ANOMALY_SUPPORTED_COLS)
ANOMALIES_DF = pd.read_csv(PATH_ANOMALIES_DF)

if not os.path.exists(PATH_TRANSACTIONS_DF):
    transactions.prepare_data(out_file=PATH_TRANSACTIONS_DF)
TRANSACTIONS_DF = pd.read_csv(PATH_TRANSACTIONS_DF)
