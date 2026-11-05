import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    database_path = tmp_path_factory.mktemp("database") / "test.db"
    previous_database_url = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = f"sqlite:///{database_path}"

    try:
        from backend.main import app

        with TestClient(app) as test_client:
            yield test_client
    finally:
        if previous_database_url is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = previous_database_url


# call root
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Microservice!"}


# call create user
def test_create_user(client):
    user_data = {
        "email": "user@gmail.com",
        "username": "create-user",
        "picture": None,
        "is_admin": False,
        "password": "password",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


# call read user by id
def test_read_users(client):
    response = client.post(
        "/users/",
        json={
            "email": "read-user@example.com",
            "username": "read-user",
            "picture": None,
            "is_admin": False,
            "password": "password",
        },
    )
    assert response.status_code == 200

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# call update user by id
def test_update_user(client):
    # First, create a user to update
    user_data = {
        "email": "user@gmail.com",
        "username": "update-user",
        "picture": None,
        "is_admin": False,
        "password": "password",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200

    # Get the user ID from the response
    user_id = response.json()["id"]

    # Update the user
    updated_user_data = {"email": "updated_user@gmail.com"}
    response = client.put(f"/users/{user_id}", json=updated_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == updated_user_data["email"]
    assert data["username"] == user_data["username"]


# call delete user by id
def test_delete_user(client):
    # First, create a user to delete
    user_data = {
        "email": "user@gmail.com",
        "username": "delete-user",
        "picture": None,
        "is_admin": False,
        "password": "password",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200

    # Get the user ID from the response
    user_id = response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200


def test_blog_crud(client):
    response = client.post(
        "/blogs/",
        json={"title": "First title", "text": "Blog body"},
    )
    assert response.status_code == 200
    blog_id = response.json()["id"]

    response = client.get(f"/blogs/{blog_id}")
    assert response.status_code == 200
    assert response.json()["text"] == "Blog body"

    response = client.put(
        f"/blogs/{blog_id}",
        json={"title": "Updated title"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["text"] == "Blog body"

    response = client.delete(f"/blogs/{blog_id}")
    assert response.status_code == 200
