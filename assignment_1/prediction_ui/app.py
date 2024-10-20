# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__, template_folder='.')


# A decorator used to tell the application
# which URL is associated with the function
@app.route('/diagnose_disease', methods=["GET", "POST"])
def diagnose():
    if request.method == "GET":
        return render_template("input_form.html")


    elif request.method == "POST":
        try:
            prediction_input = {

                "Gender": request.form.get("Gender"),
                "Age": int(request.form.get("Age")),
                "Symptom_1": request.form.get("Symptom_1"),
                "Symptom_2": request.form.get("Symptom_2"),
                "Symptom_3": request.form.get("Symptom_3"),
                "Heart_Rate_bpm": int(request.form.get("Heart_Rate_bpm")),
                "Body_Temperature_C": float(request.form.get("Body_Temperature_C")),
                "Blood_Pressure_mmHg": request.form.get("Blood_Pressure_mmHg"),
                "Oxygen_Saturation_%": int(request.form.get("Oxygen_Saturation_%"))

            }

            # Handle blood pressure
            bp = prediction_input["Blood_Pressure_mmHg"].split('/')
            if len(bp) == 2:
                systolic_bp = float(bp[0])
                diastolic_bp = float(bp[1])
                prediction_input["Systolic_BP"] = systolic_bp
                prediction_input["Diastolic_BP"] = diastolic_bp

            else:
                return jsonify(message="Invalid blood pressure format. Please enter as 'Systolic/Diastolic'."), 400


        except ValueError as e:
            return jsonify(message=f"Error processing input data: {str(e)}"), 400

        logging.debug("Prediction input : %s", prediction_input)
        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))

        prediction_value = res.json()['result']
        logging.info("Prediction Output : %s", prediction_value)
        return render_template("response_form.html",
                               prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate




# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
