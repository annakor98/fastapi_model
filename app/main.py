"""Module contains API endpoints"""

from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .model_predict import model_predict
from .model_train import train_clf
from .database import SessionLocal, engine


app = FastAPI()


@app.get("/")
async def root():
    """Returns welcome message"""
    return {"message": "Hello! This is the Iris predictor."}


@app.get("/classes/{class_n}")
async def get_class_name(class_n: schemas.IrisSpecies):
    """Returns the name of the class with the label class_n"""
    return {"species_name": class_n.name}


@app.get("/train")
async def train():
    """Trains model and returns accuracy values for train and test samples"""
    metrics = train_clf()
    return metrics
