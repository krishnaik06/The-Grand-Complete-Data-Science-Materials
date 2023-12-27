import pandas as pd
from src.logger import get_console_logger
from typing import Optional

logger = get_console_logger('Data-ingestion')

## The data import from API is also imported here if there is any..
def ingest_data()-> pd.DataFrame:
    data = pd.read_csv("E:\dl\Breast-Cancer-Survival-Prediction\data\data.csv")
    return data