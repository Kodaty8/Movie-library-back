from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_movies():
    response = client.get("/movies/list")

    assert response.status_code == 200
    assert response.json()["page"] == 1
    assert response.json()["movies"][1]["id"] > 0
    assert len(response.json()["movies"][1]["lang"]) < 6
    assert len(response.json()["movies"][1]["lang"]) > 0


def test_movie():
    response = client.get("/movies/76600?lang=fr")

    assert response.status_code == 200
    assert response.json()["title"] == "Avatar : La voie de l'eau"
    assert response.json()["lang"] == "en"
    assert response.json()["genres"][0] == "Science-Fiction"
    assert response.json()["release"] == "2022-12-14"


def test_signup():
    already_used = client.post("/users/signup", data={"username": "username", "password": "password"})
    assert already_used.status_code == 409

    empty = client.post("/users/signup")
    assert empty.status_code == 422


def test_login():
    valid = client.post("/users/login", data={"username": "username", "password": "password"})
    assert valid.status_code == 200
    assert valid.json()["token_type"] == "bearer"

    wrong_password = client.post("/users/login", data={"username": "username", "password": "pw"})
    assert wrong_password.status_code == 401


def test_user():
    token = client.post("/users/login", data={"username": "username", "password": "password"}).json()["access_token"]
    print(token)

    valid = client.get("/users/me", headers={'Authorization': 'Bearer ' + token})
    assert valid.status_code == 200
    assert valid.json() == {
        "username": "username",
        "lang": "en-US",
        "id": 1
    }

    bad_token = client.get("/users/me", headers={'Authorization': 'wrong token'})
    assert bad_token.status_code == 401
