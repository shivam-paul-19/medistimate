from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

with open('Heart_health_module/heart_disease_predictor.pkl', 'rb') as file:
    heart_model = pickle.load(file)

def makeDF(data):
    '''
    Takes raw Json data and converts it into a Pandas Dataframe
    parameters:
        data: raw json data
    returns:
        df: pandas dataframe
    '''
    df = pd.DataFrame([dict(data)])
    return df

def getPrediction(data, model):
    '''
    Takes raw data and make prediction for respective models
    paramaters:
        data: raw json data
        model: prediction model
    returns:
        pred: prediction done by model as output value 
    '''
    df = makeDF(data)   # converts into pandas dataframe
    pred = model.predict(df)
    return pred[0]

@app.route("/predict", methods=["POST"])
def post():
    if request.is_json:
        data = request.get_json()
        heart = getPrediction(data, model=heart_model)
        return jsonify({
            "heart": float(heart)
        }), 200
    else:
        return jsonify("wrong Data")
    

# test_instance = pd.DataFrame([{
#   "BMI": 19.2,
#   "Smoking": "No",
#   "AlcoholDrinking": "No",
#   "Stroke": "No",
#   "PhysicalHealth": 7,
#   "MentalHealth": 2,
#   "DiffWalking": "No",
#   "Sex": "Male",
#   "AgeCategory": "18-24",
#   "Race": "Asian",
#   "Diabetic": "No",
#   "PhysicalActivity": "Yes",
#   "GenHealth": "Good",
#   "SleepTime": 6,
#   "Asthma": "Yes",
#   "KidneyDisease": "No",
#   "SkinCancer": "No"
# }])