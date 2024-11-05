import pickle  # Import pickle to handle model loading
from app.config import MODEL_PATH, GOOGLE_DRIVE_LINKS_MODELS
from data.data_utils import download_file

def load_model(model_path=MODEL_PATH):
    """Downloads necessary data from Google Drive and loads a pre-trained model."""
    # Define paths to model files
    files = {
        "xgboost_model": f"{model_path}xgboost_model.pkl"
    }

    # Download files if they don’t exist
    for key, file_path in files.items():
        download_file(file_path, GOOGLE_DRIVE_LINKS_MODELS[key])

    # Load the pre-trained model from a pickle file
    with open(files["xgboost_model"], 'rb') as f:
        xgboost_model = pickle.load(f)
        
    return xgboost_model

def predict(model, input_data):
    """Runs prediction on input data using the pre-trained model."""
    prediction = model.predict(input_data)
    return prediction
