from fastapi import FastAPI

import models
from db import get_db
from utils import populate_db

app = FastAPI()

@app.on_event('startup')
async def startup():
    """
    Create in-memory db
    :return:
    """
    print('startup')
    await populate_db()
    db = await get_db()
    print(db)

@app.get("/status/{account}")
async def status(account:str):
    print(f'account: {account}')
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
