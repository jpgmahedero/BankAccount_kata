# db.py

import string
from datetime import datetime
from typing import Dict, List, Any, Optional

from fastapi import HTTPException

from schemas import DepositRequest, WithdrawRequest, Transaction, AccountCreateRequest, TransferRequest, \
    TransferResponse

global db

db: Dict[str, List[Any]] = {}


def initialize_db() -> None:
    global db  # Ensure you're modifying the global db variable
    db = {

        'accounts': [],
        'transactions': []
    }
    return get_db()


def get_db() -> Dict[str, List[Any]]:
    return db


def db_create_account(request: AccountCreateRequest):
    db = get_db()
    account_number = request.account
    isIBAN = 'true'
    if not is_IBAN(account_number):
        isIBAN = 'false'
    account = {
        "user_id": "U1",
        "balance": 0,
        "number": account_number,
        "isIBAN": isIBAN
    }
    db['accounts'].append(account)


def db_transfer(request: TransferRequest):
    db = get_db()
    # Check if the account exists
    src_account = next((acc for acc in db["accounts"] if acc["number"] == request.src_account), None)
    if not src_account:
        raise HTTPException(status_code=404, detail=f"Src Account {src_account} does not exist")

    dest_account = next((acc for acc in db["accounts"] if acc["number"] == request.dest_account), None)
    if not dest_account:
        raise HTTPException(status_code=404, detail=f"Dest Account {dest_account} does not exist")

    # Only update balances if EVERYTHIGN was OK
    src_account["balance"] -= request.amount
    dest_account["balance"] += request.amount
    return TransferResponse(
        src_account=src_account['number'],
        dest_account=dest_account['number'],
        src_new_balance=src_account["balance"],
        dest_new_balance=dest_account["balance"])


def db_deposit(request: DepositRequest):
    db = get_db()
    # Check if the account exists
    account = next((acc for acc in db["accounts"] if acc["number"] == request.account), None)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {request.account} does not exist")

    # Update the balance
    account["balance"] += request.amount

    return account


def db_withdraw(request: WithdrawRequest):
    db = get_db()
    # Check if the account exists
    account = next((acc for acc in db["accounts"] if acc["number"] == request.account), None)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {request.account} does not exist")

    # operartion not permitted
    if account["balance"] - request.amount < 0:
        raise HTTPException(status_code=400, detail="Invalid amount. Not enough balance available")

    # Update the balance
    account["balance"] -= request.amount

    return account


def log_transaction(type: str, account_number: str, amount: float, balance: float,
                    dest_account: Optional[str] = None):  # Create a transaction
    transaction = Transaction(
        src_account=account_number,
        dest_account=dest_account,
        type=type,
        amount=amount,
        balance=balance
    )

    # Store the transaction in the database
    db["transactions"].append(transaction.dict())


def get_sorted_transactions(account_number: str, sort_order: str) -> List[Dict]:
    db = get_db()
    transactions = db.get('transactions', [])

    # Filter transactions for the specified account number
    filtered_transactions = [
        transaction for transaction in transactions
        if transaction['src_account'] == account_number or transaction.get('dest_account') == account_number
    ]

    # Sort the filtered transactions by timestamp in the specified order
    reverse_order = sort_order == "desc"
    sorted_transactions = sorted(
        filtered_transactions,
        key=lambda transaction: datetime.fromisoformat(str(transaction['timestamp'])),
        reverse=reverse_order
    )

    return sorted_transactions


def is_IBAN(account_number: str) -> bool:
    """
    Validates whether the provided account number is a valid IBAN.

    :param account_number: The account number to validate.
    :return: True if the account number is a valid IBAN, False otherwise.
    """
    # Remove spaces
    account_number = account_number.replace(' ', '').upper()

    # Basic checks
    if len(account_number) < 15 or len(account_number) > 34:
        return False

    if not account_number[:2].isalpha() or not account_number[2:4].isdigit():
        return False

    # Rearrange the IBAN: move the first four characters to the end of the string
    rearranged_iban = account_number[4:] + account_number[:4]

    # Convert letters to numbers (A=10, B=11, ..., Z=35)
    numeric_iban = ''
    for char in rearranged_iban:
        if char.isdigit():
            numeric_iban += char
        elif char.isalpha():
            numeric_iban += str(string.ascii_uppercase.index(char) + 10)

    # Perform mod-97 operation
    iban_number = int(numeric_iban)
    return iban_number % 97 == 1
