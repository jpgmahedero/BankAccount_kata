from pydantic import BaseModel, Field

class DepositRequest(BaseModel):
    account: str = Field(..., json_schema_extra={"example": "A1"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 50.0})

class DepositResponse(BaseModel):
    account: str
    new_balance: float
