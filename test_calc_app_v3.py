from fastapi.testclient import TestClient
from calc_app_v3 import app

client = TestClient(app)

#call root
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Microservice!"}

#test multiplication
def test_calculator_multiply():
    response = client.post("/operations", json={"num1":2, "opt":"*","num2":3})
    assert response.status_code == 200
    assert response.json() == {"result": 6.0}

#check that SwaggerUI is up and runnning
def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200

#addition
def test_calculator_add():
    response = client.post("/operations", json={"num1":2, "opt":"+","num2":3})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}

#resta
def test_calculator_substract():
    response = client.post("/operations", json={"num1":2, "opt":"-","num2":3})
    assert response.status_code == 200
    assert response.json() == {"result": -1.0}

#addition
def test_calculator_divide():
    response = client.post("/operations", json={"num1":6, "opt":"/","num2":3})
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}

#addition
def test_calculator_divide_0():
    response = client.post("/operations", json={"num1":2, "opt":"/","num2":0})
    assert response.status_code == 200
    assert response.json() == {"result": 0}

#system test --> cypress / selenium