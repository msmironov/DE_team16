# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

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
            # Retrieve values and provide defaults if not found
            age = request.form.get("Age", "0")
            heart_rate = request.form.get("Heart_Rate_bpm", "0")
            body_temp = request.form.get("Body_Temperature_C", "0.0")
            oxygen_sat = request.form.get("Oxygen_Saturation_%", "0")
            
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
                systolic_bp = float(bp[0])
                diastolic_bp = float(bp[1])
                prediction_input["Systolic_BP"] = systolic_bp
                prediction_input["Diastolic_BP"] = diastolic_bp

            else:
                return jsonify(message="Invalid blood pressure format. Please enter as 'Systolic/Diastolic'."), 400


        except ValueError as e:
            return jsonify(message=f"Error processing input data: {str(e)}"), 400
                
            
            #Encode Categorical Variables 

        X=pd.DataFrame(columns=['Age', 'Heart_Rate_bpm', 'Body_Temperature_C', 'Oxygen_Saturation_%',
           'Systolic_BP', 'Diastolic_BP', 'Gender_Male', 'Symptom_1_0',
           'Symptom_1_1', 'Symptom_1_2', 'Symptom_1_3', 'Symptom_1_4',
           'Symptom_1_5', 'Symptom_1_6', 'Symptom_1_7', 'Symptom_2_0',
           'Symptom_2_1', 'Symptom_2_2', 'Symptom_2_3', 'Symptom_2_4',
           'Symptom_2_5', 'Symptom_2_6', 'Symptom_2_7', 'Symptom_3_0',
           'Symptom_3_1', 'Symptom_3_2', 'Symptom_3_3', 'Symptom_3_4',
           'Symptom_3_5', 'Symptom_3_6', 'Symptom_3_7'])

        X.loc[0]=0
            
        pred_df=pd.DataFrame([prediction_input])
            
        category_map={'Fatigue': 0, 'Sore throat': 1, 'Body ache': 2, 'Shortness of breath': 3,
               'Runny nose': 4, 'Cough': 5, 'Fever': 6, 'Headache': 7}

        category_map_gender={'Male': 1, 'Female': 0}

        pred_df['Symptom_1']=pred_df['Symptom_1'].map(category_map)
        pred_df['Symptom_2']=pred_df['Symptom_2'].map(category_map)
        pred_df['Symptom_3']=pred_df['Symptom_3'].map(category_map)

        pred_df['Gender']=pred_df['Gender'].map(category_map_gender)

        pred_df['Gender_Male']=pred_df['Gender']

        ohe=OneHotEncoder(drop='if_binary', sparse_output=False)

        pred_df_ohe=pred_df[['Symptom_1', 'Symptom_2', 'Symptom_3']]

        pred_df_ohe=pd.DataFrame(ohe.fit_transform(pred_df_ohe), columns=ohe.get_feature_names_out())

        pred_df=pred_df.drop(columns=['Symptom_1', 'Symptom_2', 'Symptom_3', 'Gender'])

        pred_df=pd.merge(pred_df, pred_df_ohe, how='inner', left_index=True, right_index=True)

        for col in X.columns:
            if col in pred_df.columns:
                X[col]=pred_df[col]
                    
        df_json = X.to_json(orient='records')

        logging.debug("Prediction input : %s", df_json)
        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(df_json))

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
