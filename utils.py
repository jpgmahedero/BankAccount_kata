from fastapi import HTTPException

from db import db


async def populate_db():
    """
    Add some fake accounts empty, non-empty, IBAN compliant, and non-compliant.
    """
    user1 = {'id': 'U1', 'name': 'N1'}
    user2 = {'id': 'U2', 'name': 'N2'}

    db['users'].append(user1)
    db['users'].append(user2)

    account1_empty_IBAN_ok = {
        'user_id': 'U1',
        'balance': 0,
        'number': 'DE89370400440532013000',
        'isIBAN': True
    }
    account1_filled_IBAN_ok = {
        'user_id': 'U1',
        'balance': 100.05,
        'number': 'DE89370400440532013000',
        'isIBAN': True
    }

    account2_empty_IBAN_no = {
        'user_id': 'U2',
        'balance': 0,
        'number': 'NO_IBAN_Number_A3',
        'isIBAN': False
    }
    account2_filled_IBAN_no = {
        'user_id': 'U2',
        'balance': 100.05,
        'number': 'NO_IBAN_Number_A4',
        'isIBAN': False
    }

    db['accounts'].append(account1_empty_IBAN_ok)
    db['accounts'].append(account1_filled_IBAN_ok)
    db['accounts'].append(account2_empty_IBAN_no)
    db['accounts'].append(account2_filled_IBAN_no)



def check_account_exists(account_number, db):
    if not any([acc['number'] == account_number for acc in db['accounts']]):
        raise HTTPException(status_code=404, detail="Account does not exist")

def account_is_IBAN_compliant(account_number, db):
    return account_number.isIBAn == True
