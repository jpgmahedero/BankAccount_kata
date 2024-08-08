# define Future SQL ALchemy models
from typing import Dict, Any
db = {
    'users': [],
    'accounts': [],
    'transactions': []
}


async def init_db():
    """
    Add some fake accounts empty, non empty and IBAN compliant and no compliant
    :return:
    """
    user1 = {'id': 'U1', 'name': 'N1'}
    user2 = {'id': 'U2', 'name': 'N2'}

    db['users'].append(user1)
    db['users'].append(user2)

    account1_empty_IBAN_ok = {
        'id': 'A1',
        'user_id': 'U1',
        'balance': 0,
        'number': 'DE89370400440532013000',
        'isIBAN': True
    }
    account1_filled_IBAN_ok = {
        'id': 'A2',
        'user_id': 'U1',
        'balance': 100.05,
        'number': 'DE89370400440532013000',
        'isIBAN': True
    }

    account2_empty_IBAN_no = {
        'id': 'A3',
        'user_id': 'U2',
        'balance': 0,
        'number': 'NO_IBAN_Number_A3',
        'isIBAN': False
    }
    account2_filled_IBAN_no = {
        'id': 'A4',
        'user_id': 'U2',
        'balance': 100.05,
        'number': 'NO_IBAN_Number_A4',
        'isIBAN': False
    }

    db['accounts'].append(account1_empty_IBAN_ok)
    db['accounts'].append(account1_filled_IBAN_ok)
    db['accounts'].append(account2_empty_IBAN_no)
    db['accounts'].append(account2_filled_IBAN_no)

async def get_db()-> Dict[str, Any]:
    return db


def iban_checksum(iban: str) -> int:
    """Calculates the checksum of the IBAN to verify its validity."""
    # Move the first four characters to the end of the string
    rearranged_iban = iban[4:] + iban[:4]

    # Replace each letter in the string with two digits, expanding the string
    digitized_iban = ''.join(str(int(ch, 36)) for ch in rearranged_iban)

    # Calculate the remainder of the big integer divided by 97
    checksum = int(digitized_iban) % 97

    return checksum

def is_valid_iban(iban: str) -> bool:
    """Validates the IBAN by checking its length, structure, and checksum."""
    iban = iban.replace(' ', '').replace('-', '')  # Remove spaces and dashes
    if not (15 <= len(iban) <= 34):
        return False

    if not (iban[:2].isalpha() and iban[2:4].isdigit()):
        return False

    return iban_checksum(iban) == 1


