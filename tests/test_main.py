# tests/test_main.py

from datetime import datetime

from schemas import Transaction


def test_index( client):
    response =  client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_account_does_not_exists( client):
    response = client.get("/check_account/ACCOUNT_DOES_NOT_EXISTS")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account does not exist"}

def test_amount_deposit_is_positive( client):
    # 'DE000000000000000000000' is an existing account in  db with an initial balance of 0
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": -50.0})

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

def test_withdraw_invalid_amounts(client):
    # Given: account with 0 balance
    # 'DE000000000000000000000' is an existing account in  db with an initial balance of 0

    # When: try to widthdraw
    response = client.post("/withdraw", json={"account": "DE000000000000000000000", "amount": 1000.0})

    # Then:
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount. Not enough balance available"}

    # Given:  account with positive balance
    # 'DE00000000000000000150' is an existing account in  db with an initial balance of 150

    # When: try to widthdraw more amount than balance
    response = client.post("/withdraw", json={"account": "DE00000000000000000150", "amount": 10000.0})

    # Then:
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount. Not enough balance available"}



def test_transfer_invalid_between_not_IBAN_accounts(client):
    # Given: account with 0 balance
    # 'DE000000000000000000000' is an existing account in  db with an initial balance of 0

    # When: try to widthdraw
    response = client.post("/withdraw", json={"account": "DE000000000000000000000", "amount": 1000.0})

    # Then:
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount. Not enough balance available"}

    # Given:  account with positive balance
    # 'DE00000000000000000150' is an existing account in  db with an initial balance of 150

    # When: try to widthdraw more amount than balance
    response = client.post("/withdraw", json={"account": "DE00000000000000000150", "amount": 10000.0})

    # Then:
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount. Not enough balance available"}


def test_transfer_with_non_IBAN_accounts(client):
    # Example call to the transfer endpoint
    response = client.post("/transfer", json={
        "src_account":  "DE00000000000000000150",
        "dest_account": "NO_IBAN_Number_A4",
        "amount": 1.0
    })
    assert response.json() == {"detail": "Transfer between non IBAN accounts is not permitted"}
    assert response.status_code == 400


def test_transfer_with_success(client):
    # Example call to the transfer endpoint
    response = client.post("/transfer", json={
        "src_account":  "ES000000000000000000100",
        "dest_account": "ES000000000000000000000",
        "amount": 75.0
    })


    assert response.status_code == 200
    assert response.json() == {
        "src_account": "ES000000000000000000100",
        "src_new_balance": 25.0,

        "dest_account": "ES000000000000000000000",
        "dest_new_balance": 75.0
    }


def test_withdraw_success(client):


    # 'DE000000000000000000000' has now a balance of 150.0 let's withdraw150
    response = client.post("/withdraw", json={"account": "DE00000000000000000150", "amount": 22.0})
    assert response.status_code == 200
    assert response.json() == {"account": "DE00000000000000000150", "new_balance": 128.0}



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
    #initialize_db()
    # Perform a deposit operation
    response = client.post("/deposit", json={"account": "DE000000000000000000000", "amount": 60.0})


    # Verify that the transaction was recorded in the database
    db  =   client.get("/status_all").json()['message']

    transactions = db['transactions']

    assert len(transactions) > 0
    transaction = transactions[-1]  # Get the last transaction

    assert transaction["src_account"] == "DE000000000000000000000"
    assert transaction["amount"] == 60.0
    assert transaction["type"] == "deposit"



def test_get_all_transformations(client):

    response = client.get("/account_statment", params={"account_number": "DE000000000000000000000"})
