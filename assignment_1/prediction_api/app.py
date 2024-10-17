import os

from flask import Flask, request


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/diagnose_disease', methods=["GET", "POST"])

#This code still needs to change
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_inout = request.get_json()
    return dp.predict_single_record(prediction_inout)


# dp = DiabetesPredictor()
# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)