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
    UnauthorizedWalletAccessError,
)
from fastapi import Depends
from app.security import get_current_user
from app.services import verify_wallet_ownership
from app.security import get_current_user, create_access_token

from app.services import deposit, withdraw, create_user, create_wallet, authenticate_user

app = FastAPI(title="LedgerCore")


@app.post("/wallets/{wallet_id}/transactions")
def create_transaction(
    wallet_id: str,
    request: TransactionCreateRequest,
    user_id: str = Depends(get_current_user)
):
    try:
        verify_wallet_ownership(user_id, wallet_id)
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
    except UnauthorizedWalletAccessError as error:
        raise HTTPException(status_code=403, detail=str(error))

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
        user = authenticate_user(request.email, request.password)

        access_token = create_access_token(user["user_id"])

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except UserNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except UnauthorizedUserAccessError as error:
        raise HTTPException(status_code=401, detail=str(error))