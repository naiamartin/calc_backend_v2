from sqlalchemy import Column, Float, Integer, String
from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    num1 = Column(Float, index=True)
    opt = Column(String, index=True)
    num2 = Column(Float, index=True)
    result = Column(Float, index=True)
