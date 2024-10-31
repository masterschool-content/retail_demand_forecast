# data/data_utils.py
import pandas as pd
import os
import gdown
from app.config import DATA_PATH, GOOGLE_DRIVE_LINKS

def download_file(file_path, url):
    """Downloads a file from Google Drive if it doesn't exist locally."""
    if not os.path.exists(file_path):
        gdown.download(url, file_path, quiet=False)
    else:
        print(f"{file_path} already exists.")

def load_data(data_path=DATA_PATH):
    """Downloads necessary data from Google Drive and loads CSV files into DataFrames."""
    files = {
        "stores": f"{data_path}stores.csv",
        "items": f"{data_path}items.csv",
        "transactions": f"{data_path}transactions.csv",
        "oil": f"{data_path}oil.csv",
        "holidays_events": f"{data_path}holidays_events.csv",
        "train": f"{data_path}train.csv"
    }

    # Download files if they don’t exist
    for key, file_path in files.items():
        download_file(file_path, GOOGLE_DRIVE_LINKS[key])

    # Load CSV files into DataFrames
    df_stores = pd.read_csv(files["stores"])
    df_items = pd.read_csv(files["items"])
    df_transactions = pd.read_csv(files["transactions"])
    df_oil = pd.read_csv(files["oil"])
    df_holidays = pd.read_csv(files["holidays_events"])
    df_train = pd.read_csv(files["train"], nrows=2.5e7)  # Load a partial dataset for memory efficiency
    
    return df_stores, df_items, df_transactions, df_oil, df_holidays, df_train

def preprocess_input_data(store_id, item_id, date, df_stores, df_items):
    """Preprocesses input data into a format suitable for model prediction."""
    input_data = {
        "store_nbr": store_id,
        "item_nbr": item_id,
        "date": date,
        # Add other necessary preprocessing steps if needed
    }
    return pd.DataFrame([input_data])