from fastapi import HTTPException

from db import initialize_db,get_db



def populate_db(db):

    """
    Add some fake accounts empty, non-empty, IBAN compliant, and non-compliant.
    """
    user1 = {"id": "U1", "name": "N1"}
    user2 = {"id": "U2", "name": "N2"}

    db["users"].append(user1)
    db["users"].append(user2)

    account1_empty_IBAN_ok = {
        "user_id": "U1",
        "balance": 0,
        "number": "DE000000000000000000000",
        "isIBAN": "true"
    }
    account1_filled_IBAN_ok = {
        "user_id": "U1",
        "balance": 100.05,
        "number": "DE00000000000000000150",
        "isIBAN": "true"
    }

    account2_empty_IBAN_no = {
        "user_id": "U2",
        "balance": 0,
        "number": "NO_IBAN_Number_A3",
        "isIBAN": "false"
    }
    account2_filled_IBAN_no = {
        "user_id": "U2",
        "balance": 100.05,
        "number": "NO_IBAN_Number_A4",
        "isIBAN": "false"
    }

    db['accounts'].append(account1_empty_IBAN_ok)
    db['accounts'].append(account1_filled_IBAN_ok)
    db['accounts'].append(account2_empty_IBAN_no)
    db['accounts'].append(account2_filled_IBAN_no)

    return db

def check_account_exists(account_number):
    db = get_db()
    if not any([acc['number'] == account_number for acc in db['accounts']]):
        raise HTTPException(status_code=404, detail="Account does not exist")


def check_amount_is_positive(amount):

    if amount < 0:
        raise HTTPException(status_code=400, detail="Invalid amount. Amount cannot be negative")


def get_account(account_number: str):
    db = get_db()
    check_account_exists(account_number)
    # Search for the account in the database
    account = next((acc for acc in db["accounts"] if acc["number"] == account_number), None)


    return account


def account_is_IBAN_compliant(account_number, db):
    return account_number.isIBAn == True
