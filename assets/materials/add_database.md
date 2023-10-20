## Описание новых endpoint'ов

| endpoint      | Тип запроса | Тело запроса                                                                                                 | Действие                                                                                                         |
|---------------|-------------|--------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| /predict      | POST        | Фичи примера для предсказания ``{"sepal_length": 0, "sepal_width": 0, "petal_length": 0, "petal_width": 0}`` | Возвращает предсказание класса для заданного набора фичей и **"запоминает" все вызовы и их время в базу данных** |
| /get_count_db | GET | | Возвращает количество записей в базе данных                                                                      |
|/get_latest_entry|GET| | Возвращает самую новую запись в базе данных |
## Подготовка

Для начала зафиксируем путь к нашей базе данных в ``.env``:

```python
DB_URL = "sqlite:///./iris.db"
```

Теперь создаем движок - "точку входа" в нашу БД:

```python
# app/database.py

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv


load_dotenv()


engine = create_engine(
    os.getenv("DB_URL"),
    connect_args={"check_same_thread": False}
)
```

Создаем класс для создания сессий:

```python
# app/database.py

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
```
Также нам необходим класс ``Base``, который свяжет механизм базы данных с функциональностью ``SQLAlchemy``:

```python
# app/database.py

Base = declarative_base()
```

Теперь объявим, как будут храниться данные в нашей базе:

```python
# app/models.py

from sqlalchemy import Column, Float, Integer, DateTime

from .database import Base


class FLOWER(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True)
    sepal_length = Column(Float, default=0)
    sepal_width = Column(Float, default=0)
    petal_length = Column(Float, default=0)
    petal_width = Column(Float, default=0)
    predicted_target = Column(Integer)
    request_time = Column(DateTime)
```

Ура, мы готовы работать с нашей базой данных :smiley:


## Обновление POST

Для начала создадим нашу БД, если ее еще не существует, и функцию ``get_db``:

```python
# app/main.py

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
Теперь обновим наш /predict endpoint:

```python
# app/main.py

@app.post('/predict')
async def predict(
        features: schemas.InputFeatures,
        db: Session = Depends(get_db)
):
    load_dotenv()
    if (Path(__file__).parent / os.getenv("MODEL_PATH")).is_file():
        prediction = model_predict(features)
        new_flower = models.FLOWER(
            sepal_length=features.sepal_length,
            sepal_width=features.sepal_width,
            petal_length=features.petal_length,
            petal_width=features.petal_width,
            predicted_target=prediction.result,
            request_time=datetime.now(),
        )
        db.add(new_flower)
        db.commit()
        db.refresh(new_flower)

        return prediction
    return {"message": "Please train model first!"}
```

Посмотреть на нашу базу данных в PyCharm можно с помощью плагина SimpleSqliteBrowser (должен автоматически порекомендоваться к установке при первом открытии ``iris.db``).

Добавим нашу базу данных в ``.gitignore``.

## Количество записей в базе данных

```python
# app/main.py

@app.get("/get_count_db")
async def get_count(db: Session = Depends(get_db)):
    return {"count_entries": db.query(models.FLOWER).count()}
```

## Получение самой новой записи в базе данных

```python
# app/main.py

@app.get("/get_latest_entry")
async def get_latest_entry(db: Session = Depends(get_db)):
    return db.query(models.FLOWER).order_by(models.FLOWER.request_time.desc()).first()
```


## Тестирование FastAPI

Для тестирования нам понадобится инстанс класса ``TestClient``:

```python
# tests/test_main.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
```

Тестирование приветственного endpoint'а:

```python
# tests/test_main.py

def test_hello():
    response = client.get('/')
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json()["message"] == "Hello! This is the Iris predictor."
```

Тестирование endpoint'a /predict:
```python
# tests/test_main.py
@app.get("/get_latest_entry")
async def get_latest_entry(db: Session = Depends(get_db)):
    latest = db.query(models.FLOWER) \
        .order_by(models.FLOWER.request_time.desc()) \
        .first()
    return latest
```