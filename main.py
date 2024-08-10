# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.params import Depends
from typing import Dict
from fastapi import HTTPException



from db import initialize_db, get_db, db_deposit
from utils import populate_db,check_account_exists,get_account

from schemas import DepositRequest, DepositResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('## startup')
    await initialize_db()  # Initialize the db structure

    db   = await get_db()
    await populate_db(db)  # Populate the db with data
    print('Database after population:', db)

    yield  # This runs the application

    print('## shutdown')


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index( ):

    return {"message": 'Hello World'}

@app.get("/status/")
async def status_all( ):
    db: Dict = await get_db()
    return {"message": db}



@app.get("/check_account/{account_number}")
async def check_account(account_number):

    await check_account_exists(account_number)
    account = await get_account(account_number)
    return {"message": account}

@app.post("/deposit", response_model=DepositResponse)
async def deposit(request: DepositRequest, db: Dict = Depends(get_db)):

    # call the db
    account = await db_deposit(request)


    return DepositResponse(account=request.account, new_balance=account["balance"])
