# model/model_utils.py
import mlflow

def load_model(model_uri):
    """Loads a pre-trained model from MLflow."""
    model = mlflow.pyfunc.load_model(model_uri)
    return model

def predict(model, input_data):
    """Runs prediction on input data using the pre-trained model."""
    prediction = model.predict(input_data)
    return prediction