"""Define schemas"""

from enum import Enum
from typing import Literal

from pydantic import BaseModel


class IrisSpecies(int, Enum):
    """Names of species for labels"""
    SETOSA = 0
    VERSICOLOR = 1
    VIRGINICA = 2


class ModelMetrics(BaseModel):
    """Model metrics"""
    accuracy_train: float
    accuracy_test: float


class InputFeatures(BaseModel):
    """Input features"""
    sepal_length: float = 0
    sepal_width: float = 0
    petal_length: float = 0
    petal_width: float = 0


class ModelPrediction(BaseModel):
    """Model prediction"""
    result: Literal[0, 1, 2]
