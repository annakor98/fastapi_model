"""Model training and evaluation"""

import pickle

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.schemas import ModelMetrics

from dotenv import load_dotenv
from pathlib import Path
import os


def train_clf():
    """Trains model and returns accuracy values for train and test samples"""
    iris = datasets.load_iris()

    x_train, x_test, y_train, y_test = train_test_split(
        iris['data'],
        iris['target'],
        random_state=0
    )

    clf = DecisionTreeClassifier(random_state=0)

    clf.fit(x_train, y_train)

    accuracy_train = clf.score(x_train, y_train)
    accuracy_test = clf.score(x_test, y_test)

    load_dotenv()

    with open(
            Path(__file__).parent / os.getenv("MODEL_PATH"),
            "wb"
    ) as model_file:
        pickle.dump(clf, model_file)

    return ModelMetrics(
        accuracy_train=accuracy_train,
        accuracy_test=accuracy_test,
    )
