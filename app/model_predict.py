"""Model prediction"""

import pickle

import os

from pathlib import Path

from dotenv import load_dotenv

import numpy as np

from app.schemas import InputFeatures, ModelPrediction


def model_predict(data: InputFeatures):
    """Predicts a value for a given set of input features"""
    load_dotenv()
    with open(
            Path(__file__).parent / os.getenv("MODEL_PATH"),
            "rb"
    ) as model_file:
        clf = pickle.load(model_file)
    data = np.array(list(dict(data).values())).reshape(1, -1)
    prediction = clf.predict(data)
    return ModelPrediction(result=int(prediction[0]))
