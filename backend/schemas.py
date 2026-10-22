from pydantic import BaseModel, ConfigDict


# Base schema with common attributes
class ItemBase(BaseModel):
    name: str
    description: str = None


# Schema for creating a new item
class ItemCreate(ItemBase):
    pass


# Schema for reading/returning an item (includes id)
class Item(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class OperationBase(BaseModel):
    num1: float
    opt: str
    num2: float
    result: float | None = None


class OperationCreate(OperationBase):
    pass


class Operation(OperationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
