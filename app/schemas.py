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
    
class UserCreateRequest(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    email: str
    password: str = Field(min_length=8, max_length=100)
    
class UserLoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=100)