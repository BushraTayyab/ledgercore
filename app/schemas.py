from enum import Enum
from decimal import Decimal

from pydantic import BaseModel, Field

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

class TransactionRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    
class TransactionCreateRequest(BaseModel):
    type: TransactionType
    amount: Decimal = Field(gt=0)