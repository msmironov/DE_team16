import os
from flask import Flask, request
from joblib import load

app = Flask(__name__)
app.config["DEBUG"] = True
model = load('model.joblib')


@app.route('/diagnose_disease', methods=["GET", "POST"])

def predict():
    symptoms = request.json
    prediction = model.predict([symptoms.values()])
    return jsonify({'diagnosis': prediction[0]})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
