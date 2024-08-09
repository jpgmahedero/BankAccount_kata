# db.py

from typing import Dict, List, Any

global db
db: Dict[str, List[Any]] = {}

async def initialize_db() -> None:
    global db  # Ensure you're modifying the global db variable
    db = {
        'users': [],
        'accounts': [],
        'transactions': []
    }
    return await get_db()

async def get_db() -> Dict[str, List[Any]]:
    return db
