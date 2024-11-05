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
    df_train = pd.read_csv(files["train"], nrows=2e7)  # Load a partial dataset for memory efficiency
    
    return df_stores, df_items, df_transactions, df_oil, df_holidays, df_train

def preprocess_input_data(store_id, item_id, split_date, df_stores, df_items, df_train):
    """Preprocesses input data into a format suitable for model prediction."""
    store_id = df_stores['store_nbr'].unique()
    item_id = [564533,838216,582865,364606]
    df_filtered = df_train[(df_train['store_nbr'].isin(store_id)) & (df_train['item_nbr'].isin(item_id))]
    # Convert 'date' column to datetime format
    df_filtered['date'] = pd.to_datetime(df_filtered['date'])
    split_date = pd.to_datetime(split_date) 
     # Get the minimum and maximum dates in the dataset to create a full date range
    min_date = df_filtered['date'].min()
    max_date = df_filtered['date'].max()
    print("Before filtering",min_date.date(), max_date.date())

    df_filtered = df_filtered[df_filtered['date'] >= split_date] #generate forecast only after split-date
    
    # Group by date and aggregate sales
    df_filtered = df_filtered.groupby(['store_nbr','item_nbr','date']).sum()['unit_sales'].reset_index()
    del df_train #clean-up memory, we don't need this dataframe

   

    # Create a full date range covering all days between the min and max dates
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')

    # Create an empty DataFrame to store the final result
    df_filled = pd.DataFrame()

    # Iterate through each store and item combination
    for (store, item), group in df_filtered.groupby(['store_nbr', 'item_nbr']):
        # Set 'date' as index and sort by date
        group.set_index('date', inplace=True)
        group = group.sort_index()

        # Reindex to fill missing dates with 0 sales
        group = group.reindex(full_date_range, fill_value=0)

        # Keep track of the store and item number for each row
        group['store_nbr'] = store
        group['item_nbr'] = item

        # Ensure that missing sales values are filled with 0
        group['unit_sales'] = group['unit_sales'].fillna(0)

        # Append the group to the final DataFrame
        df_filled = pd.concat([df_filled, group])

    # Reset the index to get 'date' back as a column
    df_filled.reset_index(inplace=True)
    df_filled.rename(columns={'index': 'date'}, inplace=True)
    
    df_filled['month'] = df_filled['date'].dt.month
    df_filled['day'] = df_filled['date'].dt.day
    df_filled['weekofyear'] = df_filled['date'].dt.isocalendar().week
    df_filled['dayofweek'] = df_filled['date'].dt.dayofweek
    df_filled['rolling_mean'] = df_filled['unit_sales'].rolling(window=7).mean()
    df_filled['rolling_std'] = df_filled['unit_sales'].rolling(window=7).std()


    # Create lag features (e.g., sales from the previous day, previous week)
    df_filled['lag_1'] = df_filled['unit_sales'].shift(1)
    df_filled['lag_7'] = df_filled['unit_sales'].shift(7)
    df_filled['lag_30'] = df_filled['unit_sales'].shift(30)

    # Drop any rows with NaN values after creating lag features
    df_filled.dropna(inplace=True)

    # Merge df_filtered with df_store and df_item on store_nbr and item_nbr, respectively
    df_filled = df_filled.merge(df_stores, on='store_nbr', how='left').merge(df_items, on='item_nbr', how='left')
    categorical_columns = ['city', 'state', 'type', 'family', 'class']
    for col in categorical_columns:
        df_filled[col] = df_filled[col].astype('category')
    df_filled = df_filled.sort_values(by=['store_nbr', 'item_nbr', 'date'])

    return df_filled