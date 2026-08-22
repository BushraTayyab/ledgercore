from decimal import Decimal
from sqlalchemy import select

from app.database import get_session
from app.models import Wallet, Transaction

from uuid import uuid4

from app.exceptions import (
    WalletNotFoundError,
    InvalidAmountError,
    InsufficientBalanceError,
)

def generate_transaction_id() -> str:
    return uuid4().hex[:10].upper()

def withdraw(wallet_id: str, amount: Decimal):
    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than zero")

    with get_session() as session:
        try:
            stmt = (
                select(Wallet)
                .where(Wallet.wallet_id == wallet_id)
                .with_for_update()
            )

            wallet = session.execute(stmt).scalar_one_or_none()

            if wallet is None:
                raise WalletNotFoundError("Wallet does not exist")

            if wallet.balance < amount:
                raise InsufficientBalanceError("Insufficient balance")

            wallet.balance -= amount

            transaction = Transaction(
                transaction_id=generate_transaction_id(),
                wallet_id=wallet_id,
                type="withdraw",
                amount=amount,
            )

            session.add(transaction)
            session.commit()

            return {
                "wallet_id": wallet.wallet_id,
                "new_balance": wallet.balance,
                "transaction_id": transaction.transaction_id,
            }

        except:
            session.rollback()
            raise

def deposit(wallet_id: str, amount: Decimal):
    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than zero")

    with get_session() as session:
        try:
            stmt = (
                select(Wallet)
                .where(Wallet.wallet_id == wallet_id)
                .with_for_update()
            )

            wallet = session.execute(stmt).scalar_one_or_none()

            if wallet is None:
                raise WalletNotFoundError("Wallet does not exist")

            wallet.balance += amount

            transaction = Transaction(
                transaction_id=generate_transaction_id(),
                wallet_id=wallet_id,
                type="deposit",
                amount=amount,
            )

            session.add(transaction)
            session.commit()

            return {
                "wallet_id": wallet.wallet_id,
                "new_balance": wallet.balance,
                "transaction_id": transaction.transaction_id,
            }

        except:
            session.rollback()
            raise