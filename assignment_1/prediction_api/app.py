import os
from flask import Flask, request, jsonify
from disease_predictor import DiseasePredictor

app = Flask(__name__)

# Instantiate the predictor
dp = DiseasePredictor()

@app.route('/predict_disease/', methods=['POST'])
def predict():
    try:
        res=request.json()
        prediction_input=dict(res)
        if not prediction_input:
            return jsonify({'message': 'No input data provided'}), 400

        prediction = dp.predict_single_record(prediction_input)
        return jsonify({'result': prediction}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
