import pytest

from app.model_predict import model_predict
from app.schemas import InputFeatures, ModelPrediction

from typing import Literal


@pytest.mark.parametrize(
    "input_features, expected_label",
    [
        (
            InputFeatures(
                sepal_length=0,
                sepal_width=0,
                petal_length=0,
                petal_width=0
            ),
            0
        ),
        (
            InputFeatures(
                sepal_length=5.1,
                sepal_width=3.5,
                petal_length=1.4,
                petal_width=0.2
            ),
            0
        ),
        (
            InputFeatures(
                sepal_length=5.7,
                sepal_width=2.8,
                petal_length=4.5,
                petal_width=1.3
            ),
            1
        ),
        (
            InputFeatures(
                sepal_length=6.7,
                sepal_width=3.3,
                petal_length=5.7,
                petal_width=2.1
            ),
            2
        ),
    ]
)
def test_prediction(
        input_features: InputFeatures,
        expected_label: Literal[0, 1, 2]
):
    prediction = model_predict(input_features)
    assert isinstance(prediction, ModelPrediction)
    assert prediction.result == expected_label
