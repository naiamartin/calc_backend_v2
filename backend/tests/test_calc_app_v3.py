import os
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    previous_database_url = os.environ.get("DATABASE_URL")
    with TemporaryDirectory() as db_directory:
        try:
            os.environ["DATABASE_URL"] = f"sqlite:///{db_directory}/test.db"
            from main import app
            from database import engine
        finally:
            if previous_database_url is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = previous_database_url

        try:
            with TestClient(app) as test_client:
                yield test_client
        finally:
            engine.dispose()


# call root
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Microservice!"}


# test multiplication
def test_calculator_multiply(client):
    response = client.post("/operations",
                           json={"num1": 2, "opt": "*", "num2": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 6.0


# check that SwaggerUI is up and runnning
def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200


# addition
def test_calculator_add(client):
    response = client.post("/operations",
                           json={"num1": 2, "opt": "+", "num2": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0


# resta
def test_calculator_substract(client):
    response = client.post("/operations",
                           json={"num1": 2, "opt": "-", "num2": 3})
    assert response.status_code == 200
    assert response.json()["result"] == -1.0


# division
def test_calculator_divide(client):
    response = client.post("/operations",
                           json={"num1": 6, "opt": "/", "num2": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 2.0


# division by zero
def test_calculator_divide_0(client):
    response = client.post("/operations",
                           json={"num1": 2, "opt": "/", "num2": 0})
    assert response.status_code == 200
    assert response.json()["result"] == 0

# system test --> cypress / selenium
