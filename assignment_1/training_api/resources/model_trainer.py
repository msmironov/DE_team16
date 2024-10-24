import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
import joblib
import os

def train(dataset):
    # split into input (X) and output (Y) variables
    y = dataset['Diagnosis']
    X = dataset.drop(columns=['Patient_ID', 'Diagnosis', 'Severity', 'Treatment_Plan'])

    # Transform Blood Pressure 
    systolic_bp = X["Blood_Pressure_mmHg"].apply(lambda x: float(x.split('/')[0]))
    diastolic_bp = X["Blood_Pressure_mmHg"].apply(lambda x: float(x.split('/')[1]))
    X["Systolic_BP"] = systolic_bp
    X["Diastolic_BP"] = diastolic_bp

    X=X.drop(columns='Blood_Pressure_mmHg')

#Encode Categorical Variables 
    category_map={'Fatigue': 0, 'Sore throat': 1, 'Body ache': 2, 'Shortness of breath': 3,
               'Runny nose': 4, 'Cough': 5, 'Fever': 6, 'Headache': 7}

    category_map_gender={'Male': 1, 'Female': 0}

    X['Symptom_1']=X['Symptom_1'].map(category_map)
    X['Symptom_2']=X['Symptom_2'].map(category_map)
    X['Symptom_3']=X['Symptom_3'].map(category_map)

    X['Gender']=X['Gender'].map(category_map_gender)
    X['Gender_Male']=X['Gender']

    ohe=OneHotEncoder(drop='if_binary', sparse_output=False)
    X_ohe=X[['Symptom_1', 'Symptom_2', 'Symptom_3']]
    X_ohe=pd.DataFrame(ohe.fit_transform(X_ohe), columns=ohe.get_feature_names_out())

    X=X.drop(columns=['Gender', 'Symptom_1', 'Symptom_2', 'Symptom_3'])
    X=pd.merge(X, X_ohe, how='inner', left_index=True, right_index=True)

  # Train a Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    y_pred=model.predict(X)
    
    scores = accuracy_score(y, y_pred)
    text_out = {
        "accuracy:": scores
    }

    # Saving model in a given location provided as an env. variable
    model_repo = os.environ['MODEL_REPO']
    if model_repo:
        file_path = os.path.join(model_repo, "model.joblib")
        joblib.dump(file_path)
        logging.info("Saved the model to the location : " + model_repo)
        return jsonify(text_out), 200
    else:
        joblib.dump("model.joblib")
        return jsonify({'message': 'The model was saved locally.'}), 200
