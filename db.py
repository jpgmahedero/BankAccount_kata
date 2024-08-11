# db.py

from typing import Dict, List, Any
from schemas import DepositRequest, WithdrawRequest, Transaction
from fastapi import  HTTPException
from datetime import datetime
global db
db: Dict[str, List[Any]] = {}

def initialize_db() -> None:
    global db  # Ensure you're modifying the global db variable
    db = {

        'accounts': [],
        'transactions': []
    }
    return  get_db()

def get_db() -> Dict[str, List[Any]]:
    return db



def db_deposit(request: DepositRequest):
    db =  get_db()
    # Check if the account exists
    account = next((acc for acc in db["accounts"] if acc["number"] == request.account), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    # Update the balance
    account["balance"] += request.amount

    return account


def db_withdraw(request: WithdrawRequest):
    db =  get_db()
    # Check if the account exists
    account = next((acc for acc in db["accounts"] if acc["number"] == request.account), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    # operartion not permitted
    if account["balance"] - request.amount < 0:
        raise HTTPException(status_code=400, detail= "Invalid amount. Not enough balance available")

    # Update the balance
    account["balance"] -= request.amount

    return account


def log_transaction(type: str, account: str, amount: float, balance:float):
    # Create a transaction
    transaction = Transaction(
        src_account=account,
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
