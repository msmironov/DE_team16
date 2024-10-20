from flask import Flask, request, jsonify
from joblib import load

app = Flask(__name__)
model = load('model.joblib')  # Make sure the path is correct depending on where you deploy this

@app.route('/diagnose_disease', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.json
        prediction = model.predict([symptoms.values()])
        return jsonify({'diagnosis': prediction[0]})
    return jsonify({"message": "Method not allowed"}), 405

if __name__ == "__main__":
    app.run(port=5000, debug=True)
