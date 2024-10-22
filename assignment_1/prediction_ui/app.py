import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__, template_folder='.')

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# A decorator to define the URL route
@app.route('/diagnose_disease', methods=["GET", "POST"])
def diagnose():
    if request.method == "GET":
        return render_template("input_form.html")

    elif request.method == "POST":
        try:
            # Retrieve form values and provide defaults if not found
            age = request.form.get("Age", "0")
            heart_rate = request.form.get("Heart_Rate_bpm", "0")
            body_temp = request.form.get("Body_Temperature_C", "0.0")
            oxygen_sat = request.form.get("Oxygen_Saturation_%", "0")
            
            # Construct input data
            prediction_input = {
                "Gender": request.form.get("Gender", "Unknown"),
                "Age": int(age) if age.isdigit() else 0,
                "Symptom_1": request.form.get("Symptom_1", "None"),
                "Symptom_2": request.form.get("Symptom_2", "None"),
                "Symptom_3": request.form.get("Symptom_3", "None"),
                "Heart_Rate_bpm": int(heart_rate) if heart_rate.isdigit() else 0,
                "Body_Temperature_C": float(body_temp) if body_temp.replace('.', '', 1).isdigit() else 0.0,
                "Blood_Pressure_mmHg": request.form.get("Blood_Pressure_mmHg", "120/80"),
                "Oxygen_Saturation_%": int(oxygen_sat) if oxygen_sat.isdigit() else 0
            }

            # Handle blood pressure
            bp = prediction_input["Blood_Pressure_mmHg"].split('/')
            if len(bp) == 2:
                prediction_input["Systolic_BP"] = float(bp[0])
                prediction_input["Diastolic_BP"] = float(bp[1])
            else:
                return jsonify(message="Invalid blood pressure format. Please enter as 'Systolic/Diastolic'."), 400

        except ValueError as e:
            logging.error(f"Error processing input data: {str(e)}")
            return jsonify(message=f"Error processing input data: {str(e)}"), 400

        logging.debug("Prediction input: %s", prediction_input)

        # Fetch the prediction API URL from the environment variable
        predictor_api_url = os.getenv('PREDICTOR_API')
        if not predictor_api_url:
            logging.error("PREDICTOR_API environment variable is not set.")
            return jsonify(message="Prediction API URL not set. Contact system admin."), 500

        # Make the API request
        try:
            res = requests.post(predictor_api_url, json=prediction_input, headers={"Content-Type": "application/json"})
            res.raise_for_status()  # Raise an error for bad responses
            prediction_value = res.json().get('result', 'No result available')
        except requests.RequestException as e:
            logging.error(f"Error communicating with prediction API: {str(e)}")
            return jsonify(message="Error communicating with prediction API."), 500
        except (ValueError, KeyError):
            logging.error("Invalid response from prediction API.")
            return jsonify(message="Invalid response from prediction API."), 500

        logging.info("Prediction Output: %s", prediction_value)
        return render_template("response_form.html", prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405

# The app runs if the script is executed directly
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
