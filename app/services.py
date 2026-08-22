from decimal import Decimal
from sqlalchemy import select

from app.database import get_session
from app.models import Wallet, Transaction, User

from app.utils import generate_transaction_id, generate_user_id, generate_wallet_id

from app.exceptions import (
    WalletNotFoundError,
    InvalidAmountError,
    InsufficientBalanceError,
    UserNotFoundError,
)

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
        
def create_user(user_name: str):

    with get_session() as session:
        user = User(
            user_id=generate_user_id(),
            user_name=user_name,
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        

        return {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "date_joined" : user.date_joined,
        }

def create_wallet(user_id: str):
    with get_session() as session:
        user = session.get(User, user_id)

        if user is None:
            raise UserNotFoundError("User does not exist")
        
        wallet = Wallet(
            wallet_id=generate_wallet_id(),
            user_id=user_id,
        )
        
        session.add(wallet)
        session.commit()
        session.refresh(wallet)
        
        return {
            "wallet_id": wallet.wallet_id,
            "user_id": wallet.user_id,
            "balance": wallet.balance,
            "status": wallet.status,
            "date_created": wallet.date_created,
        }        