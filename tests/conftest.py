# tests/conftest.py
import pytest
from fastapi.testclient import TestClient

from main import app
from db import get_db, initialize_db
from utils import populate_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
