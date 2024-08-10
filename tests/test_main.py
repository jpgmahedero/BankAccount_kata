# tests/test_main.py

import pytest

from main import  app
from fastapi.testclient import TestClient



def test_index( client):
    response =  client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_account_does_not_exists( client):

    response = client.get("/check_account/ACCOUNT_DOES_NOT_EXISTS")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account does not exist"}


def test_deposit_success(client):


    # 'DE000000000000000000000' is an existing account in your db with an initial balance of 0
    response =  client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 50.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE000000000000000000000", "new_balance": 50.0}

    # 'DE000000000000000000000' has noww a balance of 50.0 let's add 22.0
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 22.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE000000000000000000000", "new_balance": 72.0}


