import csv

from fastapi import FastAPI, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
import models
import schemas
from ArithmeticCalculator import calculate
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(filename="server.log",
                    encoding="utf-8",
                    level=logging.DEBUG)

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI application
app = FastAPI()

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, Microservice!"}


# populate db with test.csv data calculating
# the result field with the random data from test.csv
@app.post("/populate_db/")
def populate_db(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the CSV file
    csv_data = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(csv_data)

    for row in reader:
        # Calculate the result using the
        # ArithmeticCalculator before validation passes
        calculated_result = calculate({"num1": float(row['num1']),
                                       "opt": row['opt'],
                                       "num2": float(row['num2'])})
        logging.info("POPULATE: %s = %f", row, calculated_result)
        db_operation = models.Operation(
            num1=float(row['num1']),
            opt=row['opt'],
            num2=float(row['num2']),
            result=calculated_result,
        )
        db.add(db_operation)
    db.commit()
    return {"message": "Database populated successfully"}


# CREATE - Add a new item
@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# READ - Get all items
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items


# READ - Get a single item by ID
@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# UPDATE - Update an existing item
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int,
                item: schemas.ItemCreate,
                db: Session = Depends(get_db)):

    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in item.model_dump().items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


# DELETE - Remove an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

# OPERATIONS


# create operation that calculates the result from num1,
# operation and num2 input(using calculate from ArithmeticCalculator)
# and saves it to the database
@app.post("/operations/", response_model=schemas.Operation)
def create_operation(operation: schemas.OperationCreate,
                     db: Session = Depends(get_db)):
    calculated_result = calculate({"num1": operation.num1,
                                   "opt": operation.opt,
                                   "num2": operation.num2})
    logging.info("CREATE: %s = %f", operation, calculated_result)
    db_operation = models.Operation(
        num1=operation.num1,
        opt=operation.opt,
        num2=operation.num2,
        result=calculated_result,
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


# get all
@app.get("/operations/", response_model=list[schemas.Operation])
def read_operations(db: Session = Depends(get_db)):
    operations = db.query(models.Operation).all()
    return operations


# get one
@app.get("/operations/{operation_id}", response_model=schemas.Operation)
def read_operation(operation_id: int, db: Session = Depends(get_db)):
    operation = db.query(models.Operation).filter(models.Operation.id ==
                                                  operation_id).first()
    if operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return operation


# update an existing operation
@app.put("/operations/{operation_id}", response_model=schemas.Operation)
def update_operation(operation_id: int,
                     operation: schemas.OperationCreate,
                     db: Session = Depends(get_db)):
    logging.info("UPDATE: %s", operation)
    db_operation = db.query(models.Operation).filter(models.Operation.id ==
                                                     operation_id).first()
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")

    db_operation.num1 = operation.num1
    db_operation.opt = operation.opt
    db_operation.num2 = operation.num2
    db_operation.result = calculate({"num1": operation.num1,
                                     "opt": operation.opt,
                                     "num2": operation.num2})

    db.commit()
    db.refresh(db_operation)
    return db_operation


# delete an operation
@app.delete("/operations/{operation_id}")
def delete_operation(operation_id: int, db: Session = Depends(get_db)):
    operation = db.query(models.Operation).filter(models.Operation.id ==
                                                  operation_id).first()
    logging.info("DELETE: %s", operation)
    if operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")

    db.delete(operation)
    db.commit()
    return {"message": "Operation deleted successfully"}
