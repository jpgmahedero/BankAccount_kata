from typing import List

from fastapi import HTTPException
from typing import Dict
from db import initialize_db, get_db

from schemas import Transaction


def populate_db(db):
    """
    Add some fake accounts empty, non-empty, IBAN compliant, and non-compliant.
    """

    account1_empty_IBAN_ok = {
        "user_id": "U1",
        "balance": 0,
        "number": "DE000000000000000000000",
        "isIBAN": "true"
    }
    account2_filled_IBAN_ok = {
        "user_id": "U1",
        "balance": 150.0,
        "number": "DE00000000000000000150",
        "isIBAN": "true"
    }

    account3_empty_IBAN_no = {
        "user_id": "U2",
        "balance": 0,
        "number": "NO_IBAN_Number_A3",
        "isIBAN": "false"
    }
    account4_filled_IBAN_no = {
        "user_id": "U2",
        "balance": 100.05,
        "number": "NO_IBAN_Number_A4",
        "isIBAN": "false"
    }

    account5_empty_IBAN_ok = {
        "user_id": "U1",
        "balance": 0,
        "number": "ES000000000000000000000",
        "isIBAN": "true"
    }
    account6_filled_IBAN_ok = {
        "user_id": "U1",
        "balance": 100.0,
        "number": "ES000000000000000000100",
        "isIBAN": "true"
    }

    account7_filled_IBAN_ok = {
        "user_id": "U1",
        "balance": 100.0,
        "number": "FR000000000000000000100",
        "isIBAN": "true"
    }

    account8_filled_IBAN_ok = {
        "user_id": "U1",
        "balance": 100.0,
        "number": "ES9121000418450200051332",
        "isIBAN": "true"
    }

    db['accounts'].append(account1_empty_IBAN_ok)
    db['accounts'].append(account2_filled_IBAN_ok)
    db['accounts'].append(account3_empty_IBAN_no)
    db['accounts'].append(account4_filled_IBAN_no)
    db['accounts'].append(account5_empty_IBAN_ok)
    db['accounts'].append(account6_filled_IBAN_ok)
    db['accounts'].append(account7_filled_IBAN_ok)
    db['accounts'].append(account8_filled_IBAN_ok)

    return db


def check_account_exists(account_number):
    db = get_db()
    if not any([acc['number'] == account_number for acc in db['accounts']]):
        raise HTTPException(status_code=404, detail=f"Account does not exist")


def check_account_is_new(account_number):
    db = get_db()
    if any([acc['number'] == account_number for acc in db['accounts']]):
        raise HTTPException(status_code=400, detail=f"Account already exist")


def check_amount_is_positive(amount):
    if amount < 0:
        raise HTTPException(status_code=400, detail="Invalid amount. Amount cannot be negative")


def get_account(account_number: str):
    db = get_db()

    check_account_exists(account_number)
    # Search for the account in the database
    account = next((acc for acc in db["accounts"] if acc["number"] == account_number), None)

    return account


def check_account_is_IBAN_compliant(account_number):
    db = get_db()
    if not any([acc['number'] == account_number for acc in db['accounts']]):
        raise HTTPException(status_code=404, detail=f"Account {account_number} does not exist")

    account = get_account(account_number)
    if account['isIBAN'] != 'true':
        raise HTTPException(status_code=400, detail=f"Transfer between non IBAN accounts is not permitted")
