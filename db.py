# db.py

from typing import Dict, List, Any
from fastapi.params import Depends
from schemas import DepositRequest, DepositResponse


global db
db: Dict[str, List[Any]] = {}

async def initialize_db() -> None:
    global db  # Ensure you're modifying the global db variable
    db = {
        'users': [],
        'accounts': [],
        'transactions': []
    }
    return await get_db()

async def get_db() -> Dict[str, List[Any]]:
    return db

async def db_deposit(request: DepositRequest):
    db = await get_db()
    # Check if the account exists
    account = next((acc for acc in db["accounts"] if acc["number"] == request.account), None)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist")

    # Update the balance
    account["balance"] += request.amount

    return account
