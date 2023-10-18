"""Module contains API endpoints"""

from pathlib import Path

from fastapi import FastAPI

from app.model_predict import model_predict
from app.schemas import *
from app.model_train import train_clf

import os
from dotenv import load_dotenv

app = FastAPI()


@app.get("/")
async def root():
    """Returns welcome message"""
    return {"message": "Hello! This is the Iris predictor."}


@app.get("/classes/{class_n}")
async def get_class_name(class_n: IrisSpecies):
    """Returns the name of the class with the label class_n"""
    return {"species_name": class_n.name}


@app.get("/train")
async def train():
    """Trains model and returns accuracy values for train and test samples"""
    metrics = train_clf()
    return metrics


@app.post('/predict')
async def predict(features: InputFeatures):
    """Predicts label for a given set of features"""
    load_dotenv()
    if (Path(__file__).parent / os.getenv("MODEL_PATH")).is_file():
        prediction = model_predict(features)
        return prediction
    return {"message": "Please train model first!"}
