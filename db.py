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
        'users': [],
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


def get_sorted_transactions(account_number: str) -> List[str]:
    db = get_db()
    transactions = db.get('transactions', [])

    # Filter transactions for the  account
    filtered_transactions = [transaction for transaction in transactions if transaction['src_account'] == account_number ]

    # Sort the filtered transactions by timestamp
    sorted_transactions = sorted(filtered_transactions,
                                 key=lambda transaction: datetime.fromisoformat(str(transaction['timestamp'])))

    # Format each transaction into the desired string format
    formatted_transactions = []
    for transaction in sorted_transactions:
        date_str = datetime.fromisoformat(str(transaction['timestamp'])).strftime(
            "%d.%m.%Y")  # Format date as DD.MM.YYYY
        amount_str = f"+{transaction['amount']}" if transaction['type']=='deposit'  else f"-{abs(transaction['amount'])}"
        balance_str = f"{transaction['balance']}"  # Get the balance for the transaction
        formatted_transactions.append(f"{date_str} {amount_str} {balance_str}")
    return formatted_transactions