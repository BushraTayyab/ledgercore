from decimal import Decimal
from sqlalchemy import select

from app.database import get_session
from app.models import Wallet, Transaction, User

from app.utils import ( 
    generate_transaction_id, 
    generate_user_id, 
    generate_wallet_id, 
    password_hasher,
)


from app.exceptions import (
    WalletNotFoundError,
    InvalidAmountError,
    InsufficientBalanceError,
    UserNotFoundError,
    UnauthorizedWalletAccessError,
    UnauthorizedUserAccessError,
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
        
def create_user(user_name: str, email: str, password: str):

    with get_session() as session:
        user = User(
            user_id=generate_user_id(),
            user_name=user_name,
            email=email,
            password_hash=password_hasher.hash(password),
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        

        return {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "date_joined": user.date_joined,
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
        
def verify_wallet_ownership(user_id: str, wallet_id: str):
    with get_session() as session:
        wallet = session.get(Wallet, wallet_id)

        if wallet is None:
            raise WalletNotFoundError("Wallet does not exist")

        if wallet.user_id != user_id:
            raise UnauthorizedWalletAccessError(
                "User does not own wallet"
            )
            
# Open a session.
# Find the User by email.
# If the user doesn't exist, reject authentication.
# Verify the supplied password against user.password_hash using:
# password_hasher.verify(password, user.password_hash)
# If verification fails, reject authentication.
# If it succeeds, return the authenticated user's information.

def authenticate_user(email: str, password: str):
    with get_session() as session:
        stmt = select(User).where(User.email == email)
        user = session.execute(stmt).scalar_one_or_none()

        if user is None:
            raise UserNotFoundError("User does not exist")

        if user.password_hash is None:
            raise UnauthorizedUserAccessError(
                "User does not have a password set"
            )

        if not password_hasher.verify(password, user.password_hash):
            raise UnauthorizedUserAccessError(
                "Invalid email or password"
            )

        return {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "email": user.email,
            "date_joined": user.date_joined,
        }