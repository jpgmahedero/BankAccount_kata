# tests/test_main.py

import pytest
from fastapi import HTTPException
from utils import check_account_exists

@pytest.mark.anyio
async def test_index(init_db, client):  # Ensure init_db is called before the test
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.anyio
async def test_account_does_not_exists(init_db, client):  # Ensure init_db is called before the test
    response = await client.get("/check_account/ACCOUNT_DOES_NOT_EXISTS")

    assert response.status_code == 404
    assert response.json() == {"detail": "Account does not exist"}

"""
#async def test_index( db: dict = Depends(get_db)):
async def test_index2(init_db, db: dict = Depends(get_db)):


    await populate_db(db)
    print('1 ===========')
    print(db)
    print('2 ===========')
    populate_db(db)
    print('3 ===========')
    assert  False
    response = client.get('/')

    assert  response.status_code == 200


def test_deposit():
    with pytest.raises(HTTPException, match='Account does not exist'):
        response = client.get('/deposit/DE89370400440532013000/9.99')
    '''
        response = client.post(s
            "/deposit/",
            json={"account": 'DE89370400440532013000', "amount": 9.99},
        )
        '''
    assert response.status_code == 200

"""