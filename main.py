# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.params import Depends
from typing import Dict
from db import  log_transaction



from db import initialize_db, get_db, db_deposit
from utils import populate_db,check_account_exists,get_account, check_amount_is_positive

from schemas import DepositRequest, DepositResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('## startup')
    initialize_db()  # Initialize the db structure

    db   =  get_db()
    populate_db(db)  # Populate the db with data
    print('Database after population:', db)

    yield  # This runs the application

    print('## shutdown')


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index( ):

    return {"message": 'Hello World'}

@app.get("/status_all/")
async def status_all( ):
    db: Dict =  get_db()
    return {"message": db}



@app.get("/check_account/{account_number}")
async def check_account(account_number):

    check_account_exists(account_number)
    account =  get_account(account_number)
    return {"message": account}



@app.post("/deposit", response_model=DepositResponse)
async def deposit(request: DepositRequest):
    check_account_exists(request.account)
    check_amount_is_positive(request.amount)

    # call the db
    account =  db_deposit(request)
    log_transaction(type='deposit',account=request.account, amount=request.amount)


    return DepositResponse(account=request.account, new_balance=account["balance"])
