# data/data_utils.py
import pandas as pd

def load_data(data_path):
    """Loads CSV files from the specified path and returns DataFrames."""
    df_stores = pd.read_csv(f"{data_path}stores.csv")
    df_items = pd.read_csv(f"{data_path}items.csv")
    df_transactions = pd.read_csv(f"{data_path}transactions.csv")
    df_oil = pd.read_csv(f"{data_path}oil.csv")
    df_holidays = pd.read_csv(f"{data_path}holidays_events.csv")
    df_train = pd.read_csv(f"{data_path}train.csv", nrows=2.5e7)
    return df_stores, df_items, df_transactions, df_oil, df_holidays, df_train

def preprocess_input_data(store_id, item_id, date, df_stores, df_items):
    """Preprocesses input data into a format suitable for model prediction."""
    input_data = {
        "store_nbr": store_id,
        "item_nbr": item_id,
        "date": date,
        # Additional features can be added here
    }
    return pd.DataFrame([input_data])