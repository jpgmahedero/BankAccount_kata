from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from itertools import count

class DepositRequest(BaseModel):
    account: str = Field(..., json_schema_extra={"example": "DE000000000000000000000"})
    amount: float = Field(...,  json_schema_extra={"example": 50.0})

class DepositResponse(BaseModel):
    account: str
    new_balance: float

# Initialize a global counter for auto-incrementing the ID
transaction_id_counter = count(1)

class Transaction(BaseModel):
    id: int = Field(default_factory=lambda: next(transaction_id_counter), example=1)
    src_account: str = Field(..., example="A1")
    type: Literal["deposit", "withdraw", "transfer"] = Field(..., example="deposit")
    amount: float = Field(..., example=100.0)
    dest_account: Optional[str] = Field(None, example="B1")  # Nullable, relevant only for transfers
    timestamp: datetime = Field(default_factory=datetime.utcnow, example="2024-01-01T12:00:00Z")

    @field_validator('dest_account', mode='before')
    def validate_dest_account(cls, v, values):
        if values.get('type') == 'transfer' and not v:
            raise ValueError('dest_account must be provided for transfer transactions')
        return v

    class Config:
        orm_mode = True
