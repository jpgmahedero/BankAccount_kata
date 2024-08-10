# tests/test_main.py

import pytest

from main import  app
from fastapi.testclient import TestClient
from schemas import  Transaction
from datetime import datetime
from db import get_db


def test_index( client):
    response =  client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_account_does_not_exists( client):
    response = client.get("/check_account/ACCOUNT_DOES_NOT_EXISTS")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account does not exist"}

def test_amount_deposit_is_positive( client):
    # 'DE000000000000000000000' is an existing account in your db with an initial balance of 0
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": -50.0})

    print('oooooooooooooooooooooooooooo')
    print(response.status_code)
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {"detail":"Invalid amount. Amount cannot be negative"}

def test_deposit_success(client):

    # 'DE000000000000000000000' is an existing account in your db with an initial balance of 0
    response =  client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 50.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE000000000000000000000", "new_balance": 50.0}

    # 'DE000000000000000000000' has now a balance of 50.0 let's add 22.0
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 22.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE000000000000000000000", "new_balance": 72.0}


def test_withdraw_success(client):

    assert False
    # 'DE000000000000000000000' is an existing account in your db with an initial balance of 0
    client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 50.0})

    # 'DE000000000000000000000' has noww a balance of 50.0 let's add 22.0
    response = client.post("/withdraw", json={"account": "DE000000000000000000000", "amount": 100.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE000000000000000000000", "new_balance": 72.0}


def test_transaction_creation():
    transaction = Transaction(
        id=27,
        src_account="DE000000000000000000000",
        amount=66.6,
        type="deposit",
        timestamp=datetime.utcnow(),
    )

    assert transaction.id == 27
    assert transaction.src_account == "DE000000000000000000000"
    assert transaction.dest_account == None
    assert transaction.amount == 66.6
    assert transaction.type == "deposit"
    assert isinstance(transaction.timestamp, datetime)

def test_perform_deposit_creates_transaction(client):
    # Perform a deposit operation
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 60.0})


    # Verify that the transaction was recorded in the database
    db  =   client.get("/status_all").json()['message']

    transactions = db['transactions']

    print(transactions)
    assert len(transactions) > 0
    transaction = transactions[-1]  # Get the last transaction

    assert transaction["src_account"] == "DE000000000000000000000"
    assert transaction["amount"] == 60.0
    assert transaction["type"] == "deposit"


