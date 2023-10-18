"""Module contains API endpoints"""

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
models.Base.metadata.create_all(bind=engine)


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


def get_db():
    """Launches and closes session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/predict')
async def predict(
        features: schemas.InputFeatures,
        db: Session = Depends(get_db)
):
    """Predicts label for a given set of features"""
    load_dotenv()
    if (Path(__file__).parent / os.getenv("MODEL_PATH")).is_file():
        prediction = model_predict(features)
        new_flower = models.FLOWER(
            sepal_length=features.sepal_length,
            sepal_width=features.sepal_width,
            petal_length=features.petal_length,
            petal_width=features.petal_width,
            predicted_target=prediction.result,
        )
        db.add(new_flower)
        db.commit()
        db.refresh(new_flower)

        return prediction
    return {"message": "Please train model first!"}


@app.get("/get_count")
async def get_last(db: Session = Depends(get_db)):
    """Get number of entries in the database"""
    return {"count_entries": db.query(models.FLOWER).count()}
