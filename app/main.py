from fastapi import FastAPI, HTTPException
from app.schemas import TransactionCreateRequest, TransactionType
from app.exceptions import (
    InsufficientBalanceError,
    InvalidAmountError,
    WalletNotFoundError,
)

from app.services import deposit, withdraw

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