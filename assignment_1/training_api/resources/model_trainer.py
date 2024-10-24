import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
import joblib

def train(dataset):
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:8]
    y = dataset[:, 8]

  # Train a Random Forest Classifier
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    y_pred=model.predict(X)
    
    scores = accuracy_score(y, y_pred)
    text_out = {
        "accuracy:": scores[0]
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
