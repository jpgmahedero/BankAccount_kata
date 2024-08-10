# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from main import  app
from db import get_db, initialize_db
from utils import populate_db




@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

"""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app
from db  import get_db,initialize_db
from utils import  populate_db
@pytest.fixture
async def client():

    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.get("/")        # Trigger lifespan events
        yield client


@pytest_asyncio.fixture(scope="module", autouse=True)
async def init_db():
    print('\n----- conftest')
    db = await get_db()

    return db
"""