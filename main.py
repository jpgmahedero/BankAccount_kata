# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.params import Depends

from db import initialize_db, get_db
from utils import populate_db,check_account_exists


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
async def index( db: dict = Depends(get_db)):

    return {"message": 'Hello World'}

@app.get("/check_account/{account_number}")
async def exception(account_number):

    await check_account_exists(account_number)

@app.get("/a")




@app.get("/deposit/{account}/{")
async def deposit(account: str):
    print(f'account: {account}')
    return {"message": "Hello World"}
