![Iris Species](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*7bnLKsChXq94QjtAiRn40w.png)

| sepal length (cm) | sepal width (cm) | petal length (cm) | petal width (cm) | target |
|:-----------------:|:----------------:|:-----------------:|:----------------:|:------:|
|        5.1        |       3.5        |        1.4        |       0.2        |   0    |
|        5.7        |       2.8        |        4.5        |       1.3        |   1    |
|        6.7        |       3.3        |        5.7        |       2.1        |   2    |

## Создание проекта

* Создать проект с новым окружением с помощью poetry
* В терминале:

```commandline
poetry add fastapi uvicorn[standard] scikit-learn
```

## API endpoints

| endpoint         | Тип запроса | Тело запроса                                                                                                 | Действие                                                                            |
|------------------|-------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| /                | GET         |                                                                                                              | Возвращает сообщение ``Hello! This is the Iris predictor.``                         |
| /class/{class_n} | GET         |                                                                                                              | Возвращает вид, соответствующий n-ому классу                                        |
| /train           | GET         |                                                                                                              | Обучает модель, и возвращает точность предсказания для обучающей и тестовой выборки |
| /predict         | POST        | Фичи примера для предсказания ``{"sepal_length": 0, "sepal_width": 0, "petal_length": 0, "petal_width": 0}`` | Возвращает предсказание класса для заданного набора фичей                           |

## Приветственный endpoint

В файле ``main.py``

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello! This is the Iris predictor."}
```

## Запуск

```commandline
uvicorn main:app --reload
```

## Enpoint c видами ирисов

```python
@app.get("/classes/{class_n}")
async def get_class_name(class_n: int):
    species = {
        0: "setosa",
        1: "versicolor",
        2: "virginica",
    }
    return {"species_name": species[class_n]}
```

Делаем красиво:

Выносим в ``schemas.py``:

```python
from enum import Enum


class IrisSpecies(int, Enum):
    setosa = 0
    versicolor = 1
    virginica = 2
```

Новый метод:

```python

from app import schemas


@app.get("/classes/{class_n}")
async def get_class_name(class_n: schemas.IrisSpecies):
    return {"species_name": class_n.name}
```

## Автодокументация (Swagger)

```commandline
http://127.0.0.1:8000/docs
```

## Endpoint с обучением модели:

В ``schemas.py``:

```python
from pydantic import BaseModel


class ModelMetrics(BaseModel):
    accuracy_train: float
    accuracy_test: float


class InputFeatures(BaseModel):
    sepal_length: float = 0
    sepal_width: float = 0
    petal_length: float = 0
    petal_width: float = 0
```

Теперь пишем обучение модели (``model_train.py``):

```python
import pickle
from app.schemas import ModelMetrics
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


def train_clf():
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

    with open("app/model.pkl", "wb") as model_file:
        pickle.dump(clf, model_file)

    return ModelMetrics(
        accuracy_train=accuracy_train,
        accuracy_test=accuracy_test,
    )

```

И добавляем метод в ``main.py``:

```python
from app.model_train import train_clf


@app.get("/train")
async def train():
    metrics = train_clf()
    return metrics
```

## Endpoint для предсказания:

Добавляем формат предсказания в ``schemas.py``:

```python
from pydantic import BaseModel
from typing import Literal


class ModelPrediction(BaseModel):
    result: Literal[0, 1, 2]
```

Реализуем предсказание (``model_predict.py``):

```python
import numpy as np
import pickle
from app import schemas


def predict(data: schemas.InputFeatures):
    with open("app/model.pkl", "rb") as model_file:
        clf = pickle.load(model_file)
    data = np.array(list(dict(data).values())).reshape(1, -1)
    prediction = clf.predict(data)
    return schemas.ModelPrediction(result=int(prediction[0]))

```

И метод:

```python

from app import model_predict


@app.post('/predict')
async def predict(features: schemas.InputFeatures):
    prediction = model_predict.predict(features)
    return prediction
```

Добавляем проверку того, что существует файл с моделью:

```python

from app import model_predict
from pathlib import Path


@app.post('/predict')
async def predict(features: schemas.InputFeatures):
    if Path("app/model.pkl").is_file():
        prediction = model_predict.predict(features)
        return prediction
    else:
        return {"message": "Please train model first!"}
```