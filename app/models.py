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