from typing import Dict, Any

db = {
    'users': [],
    'accounts': [],
    'transactions': []
}


async def get_db() -> Dict[str, Any]:
    return db
