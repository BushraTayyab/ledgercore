from fastapi import FastAPI, HTTPException
from app.schemas import (
    TransactionCreateRequest, 
    TransactionType, 
    UserCreateRequest,
    UserLoginRequest,
)
from app.exceptions import (
    InsufficientBalanceError,
    InvalidAmountError,
    WalletNotFoundError,
    UserNotFoundError,
    UnauthorizedUserAccessError,
    
)

from app.services import deposit, withdraw, create_user, create_wallet, authenticate_user

app = FastAPI(title="LedgerCore")


@app.post("/wallets/{wallet_id}/transactions")
def create_transaction(
    wallet_id: str,
    request: TransactionCreateRequest,
):
    try:
        if request.type == TransactionType.DEPOSIT:
            return deposit(wallet_id, request.amount)

        return withdraw(wallet_id, request.amount)

    except WalletNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except (InvalidAmountError, InsufficientBalanceError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

@app.post("/users")
def create_user_endpoint(request: UserCreateRequest):
    return create_user(
        request.user_name,
        request.email,
        request.password,
    )
    
    
@app.post("/users/{user_id}/wallets")
def create_wallet_endpoint(user_id: str):
    try:
        return create_wallet(user_id)
    
    except UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
        
@app.post("/login")
def login(request: UserLoginRequest):
    try:
        return authenticate_user(
            request.email,
            request.password,
        )

    except UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )
    except UnauthorizedUserAccessError as error:
        raise HTTPException(
            status_code=401,
            detail=str(error),
        )