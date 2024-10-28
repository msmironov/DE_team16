import os
from flask import Flask, request, jsonify
from disease_predictor import DiseasePredictor
from google.cloud import storage
import joblib

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/diabetes_predictor/model', methods=['PUT'])  # trigger updating the model
def refresh_model():
    return dp.download_model()

@app.route('/predict_disease/', methods=['POST'])
def predict():
    prediction_input=request.get_json()
    return dp.predict_single_record(prediction_input)

# Instantiate the predictor
dp = DiseasePredictor()

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
