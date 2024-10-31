import streamlit as st
from app.config import DATA_PATH, MODEL_URI
from data.data_utils import load_data, preprocess_input_data
from model.model_utils import load_model, predict

def main():
    st.title("Corporación Favorita Sales Forecasting")

    # Load data and model
    df_stores, df_items, df_transactions, df_oil, df_holidays, _ = load_data(DATA_PATH)
    model = load_model(MODEL_URI)

    # UI components for inputs
    store_id = st.selectbox("Store", df_stores['store_nbr'].unique())
    item_id = st.selectbox("Item", df_items['item_nbr'].unique())
    date = st.date_input("Forecast Date")

    # Run prediction when button is clicked
    if st.button("Get Forecast"):
        input_data = preprocess_input_data(store_id, item_id, date, df_stores, df_items)
        prediction = predict(model, input_data)
        st.write(f"Predicted Sales for {date}: {prediction[0]}")

if __name__ == "__main__":
    main()