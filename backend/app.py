from flask import Flask, request, jsonify
import pickle
import pandas as pd
from flask_cors import CORS
from abc import ABC, abstractmethod

app = Flask(__name__)
CORS(app)

def loadModel(filePath: str) -> object:
    with open(filePath, "rb") as file:
        return pickle.load(file)

heart_model = loadModel('Heart_health_module/heart_disease_predictor.pkl')
sleep_model = loadModel('Sleep_quality_module/sleep_disorder_predictor.pkl')
metabolism_model = loadModel('Metabolism_module/metabolic_syndrome_predictor.pkl')

# Classes for making prediction
class PredictionModel(ABC):
    @abstractmethod
    def predict(data: pd.DataFrame) -> int:
        pass

class HeartPredictionModel(PredictionModel):
    def predict(data: pd.DataFrame) -> int:
        prediction = heart_model.predict(data)
        return prediction[0]

class SleepPredictionModel(PredictionModel):
    def predict(data: pd.DataFrame) -> int:
        prediction = sleep_model.predict(data)
        return prediction[0]

class MetabolismPredictionModel(PredictionModel):
    def predict(data: pd.DataFrame) -> int:
        prediction = metabolism_model.predict(data)
        return prediction[0]

# class to preprocess data
class Preprocessor(ABC):
    @abstractmethod
    def process(data: dict) -> pd.DataFrame:
        pass

class HeartPreprocessor(Preprocessor):
    def process(data: dict) -> pd.DataFrame:
        cols = ["BMI","Smoking","AlcoholDrinking","Stroke","PhysicalHealth","MentalHealth",
            "DiffWalking","Sex","AgeCategory","Race","Diabetic","PhysicalActivity","GenHealth",
            "SleepTime","Asthma","KidneyDisease", "SkinCancer"]
        
        values = []
        for col in cols:
            values.append(data[col])
        
        return pd.DataFrame([values], columns=cols)
    
class SleepPreprocessor(Preprocessor):
    def process(data: dict) -> pd.DataFrame:
        cols = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep', 
        'Physical Activity Level', 'Stress Level', 'BMI Category', 
        'Blood Pressure', 'Heart Rate', 'Daily Steps']
        
        values = []
        for col in cols:
            values.append(data[col])
        
        return pd.DataFrame([values], columns=cols)

class MetabolismPreprocessor(Preprocessor):
    def process(data: dict) -> pd.DataFrame:
        cols = ['Age', 'Sex', 'Race', 'BMI', 'Albuminuria', 'UrAlbCr', 
        'UricAcidCategory', 'HDLCategory', 'TrigCategory', 'BloodSugarCategory']
        
        values = []
        for col in cols:
            values.append(data[col])
        
        return pd.DataFrame([values], columns=cols)

# class to manage all the flow
class PredictionOrechestrator():
    def __init__(self, models: list, preprocessors: list, names: list):
        self.models = models
        self.preprocessors = preprocessors
        self.names = names
    
    def run(self, data: dict) -> dict:
        output = {}

        for model, preprocessors, module_name in zip(self.models, self.preprocessors, self.names):
            processed_data = preprocessors.process(data)
            prediction = model.predict(processed_data)
            output[module_name] = prediction

        return output
    
model_list = [HeartPredictionModel(), SleepPredictionModel(), MetabolismPredictionModel()]
preprocessors_list = [HeartPreprocessor(), SleepPreprocessor(), MetabolismPreprocessor()]
names_list = ["Heart", "Sleep", "Metabolism"]

predictor = PredictionOrechestrator(models=model_list, preprocessors=preprocessors_list, names=names_list)

@app.route("/predict", methods=["POST"])
def predict():
    if request.is_json:
        data = request.get_json()
        
        return jsonify({
            "heart": float(0)
        }), 200
    else:
        return jsonify("wrong Data")

# routes to test the server only
@app.route("/test", methods=["GET"])
def test():
    return "All ok!"

@app.route("/testpost", methods=["POST"])
def testpost():
    if request.is_json:
        data = request.get_json()
        return jsonify({
            "status": "All good",
            "data": data
        }), 200

    else:
        return jsonify({
            "status": "problem in data",
        }), 400