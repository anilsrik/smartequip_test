from fastapi.testclient import TestClient
from unittest import mock
import random

from main import app

client = TestClient(app)

def test_get_challenge():
    response = client.get("/sumchallenge")
    assert response.status_code == 200
    res = response.json()
    assert "challenge" in res
    assert res["challenge"].find("Please sum numbers") == 0

def test_challenge_rand():
    mocked_random_randint = lambda x, y : 10
    with mock.patch('random.randint', mocked_random_randint):
        response = client.get("/sumchallenge?count=2")
        assert response.status_code == 200
        res = response.json()
        print(res)
        assert res["challenge"].find("Please sum numbers 10,10") == 0

def test_challenge_exp():
        response = client.get("/sumchallenge?count=101")
        assert response.status_code == 400
        res = response.json()
        assert res["detail"].find("Count Value must be within range (2,100) both included") == 0


def test_challenge_exp():
        response = client.get("/sumchallenge?count=101")
        assert response.status_code == 400
        res = response.json()
        assert res["detail"].find("Count Value must be within range (2,100) both included") == 0
    

def test_validation_sum():
    data = {
        "input": [ 20, 10],
        "ans": 30
        }
    response = client.post("/validatesum", json=data)
    print(response)
    assert response.status_code == 200
    

def test_validation_sum_exp():
    data = {
        "input": [ 20, 10],
        "ans": 40
        }
    response = client.post("/validatesum", json=data)
    print(response)
    assert response.status_code == 400
    