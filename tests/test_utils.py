# tests/test_utils.py

import pytest
from db import get_db, initialize_db
from utils import populate_db


@pytest.mark.anyio
async def test_check_account_exists(client):  # Use the client fixture
    db  = await  get_db()
    populate_db(db)
    print ('xxxxx populate_db()')

    print('>>>>>>>>>>>>>><')
    print(db)

    assert 'users' in db, "Users should be populated"
    assert 'accounts' in db, "Accounts should be populated"
    assert len(db['users']) > 0, "Users list should not be empty"
    assert len(db['accounts']) > 0, "Accounts list should not be empty"
    assert False  # This is to inspect the printed database content
