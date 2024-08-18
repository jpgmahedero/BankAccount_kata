# main.py

from contextlib import asynccontextmanager  # used for setup in lifespan

from fastapi import FastAPI, Query, Request

import db
from db import log_transaction, initialize_db, get_db, db_deposit, db_withdraw, get_sorted_transactions, \
    db_create_account
from decorators import account_is_new, account_exists, transfer_is_IBAN_compliant
from schemas import AccountCreateRequest
from schemas import DepositRequest, DepositResponse
from schemas import TransferRequest, TransferResponse
from schemas import WithdrawRequest, WithdrawResponse
from settings import PRODUCTION_MODE
from utils import populate_db, check_amount_is_positive


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('## startup')
    initialize_db()  # Initialize the db structure

    db = get_db()
    if not PRODUCTION_MODE:
        populate_db(db)  # Populate the db with data
    print('Database after population:', db)

    yield  # This runs the application

    print('## shutdown')


app = FastAPI(lifespan=lifespan)


@app.post("/create_account/")
@account_is_new
async def create_account(request: AccountCreateRequest):
    db_create_account(request)
    return {"detail": "Account created"}


@app.post("/deposit", response_model=DepositResponse)
@account_exists
async def deposit(request: DepositRequest):
    check_amount_is_positive(request.amount)

    # call the db
    account = db_deposit(request)
    log_transaction(type='deposit', account_number=request.account, amount=request.amount, balance=account["balance"])

    return DepositResponse(account=request.account, new_balance=account["balance"])


@app.post("/withdraw", response_model=WithdrawResponse)
@account_exists
async def withdraw(request: WithdrawRequest):
    check_amount_is_positive(request.amount)

    print(f'-- withdraw ENDPOINT request:{request}')
    # call the db
    account = db_withdraw(request)
    log_transaction(type='withdraw', account_number=request.account, amount=request.amount, balance=account["balance"])

    return WithdrawResponse(account=request.account, new_balance=account["balance"])


@app.post("/transfer", response_model=TransferResponse)
# no need to check since it's done inseid db_transfer()
# @account_exists
@transfer_is_IBAN_compliant
async def transfer(request: TransferRequest):
    result = db.db_transfer(request)
    log_transaction(type='withdraw', account_number=result.src_account, amount=request.amount,
                    balance=result.src_new_balance)

    log_transaction(type='deposit', account_number=result.dest_account, amount=request.amount,
                    balance=result.dest_new_balance)

    # Return a summary of the transfer
    return result


@app.get("/account_statement/{account}")
@account_exists
async def account_statement(request: Request, sort_order: str = Query("asc", patter="^(asc|desc)$")):
    """
    Get the account statement for a specific account number, sorted by date.

    Parameters:
    - account_number: The account number to fetch transactions for.
    - sort_order: The order to sort the transactions by date. Either 'asc' for ascending or 'desc' for descending.
    """

    # Get sorted transactions for the specific account number
    account_number = request.path_params.get('account')
    transactions = get_sorted_transactions(account_number, sort_order)

    return {"detail": transactions}
