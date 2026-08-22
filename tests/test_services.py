import pytest
import app.services as services
from decimal import Decimal

from sqlalchemy import select

from app.models import Transaction
from app.models import Wallet
from sqlalchemy.exc import IntegrityError

from app.exceptions import (
    WalletNotFoundError,
    InvalidAmountError,
    InsufficientBalanceError,
)


def test_withdraw_success(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    result = services.withdraw("TESTW001", Decimal("100"))

    assert result["wallet_id"] == "TESTW001"
    assert result["new_balance"] == Decimal("400.00")
    assert result["transaction_id"]


def test_withdraw_invalid_amount():
    with pytest.raises(
        InvalidAmountError,
        match="Amount must be greater than zero",
    ):
        services.withdraw("TESTW001", Decimal("0"))
        
def test_withdraw_wallet_not_found(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)
    
    with pytest.raises(
        WalletNotFoundError,
        match="Wallet does not exist",
    ):
        services.withdraw("DOESNOTEXIT", Decimal("100"))

def test_withdraw_insufficient_balance(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)
    
    with pytest.raises(
        InsufficientBalanceError,
        match="Insufficient balance",
    ):
        services.withdraw("TESTW001", Decimal("600"))

def test_withdraw_creates_transaction(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    result = services.withdraw("TESTW001", Decimal("100"))

    with test_session_factory() as session:
        transaction = session.execute(
            select(Transaction)
            .where(Transaction.transaction_id == result["transaction_id"])
        ).scalar_one()
    
    assert transaction.wallet_id == "TESTW001"
    assert transaction.type == "withdraw"
    assert transaction.amount == Decimal("100")
    
    
def test_withdraw_rolls_back_if_transaction_creation_fails(
    monkeypatch,
    test_session_factory,
):
    monkeypatch.setattr(services, "get_session", test_session_factory)
    monkeypatch.setattr(
        services,
        "generate_transaction_id",
        lambda: "DUPLICATE1",
    )
    
    with test_session_factory() as session:
        existing_transaction = Transaction(
            transaction_id="DUPLICATE1",
            wallet_id="TESTW001",
            type="withdraw",
            amount=Decimal("50"),
        )
        session.add(existing_transaction)
        session.flush()

        with pytest.raises(IntegrityError):
            services.withdraw("TESTW001", Decimal("100"))
        
        with test_session_factory() as session:
            wallet = session.execute(
                select(Wallet)
                .where(Wallet.wallet_id == "TESTW001")
            ).scalar_one()
        
        assert wallet.balance == Decimal("500.00")

def test_deposit_success(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    result = services.deposit("TESTW001", Decimal("100"))

    assert result["wallet_id"] == "TESTW001"
    assert result["new_balance"] == Decimal("600.00")
    assert result["transaction_id"]
    
def test_deposit_invalid_amount():
    with pytest.raises(
        InvalidAmountError,
        match="Amount must be greater than zero",
    ):
        services.deposit("TESTW001", Decimal("0"))
        
def test_deposit_wallet_not_found(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    with pytest.raises(
        WalletNotFoundError,
        match="Wallet does not exist",
    ):
        services.deposit("DOESNOTEXIST", Decimal("100"))
        
def test_deposit_creates_transaction(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    result = services.deposit("TESTW001", Decimal("100"))

    with test_session_factory() as session:
        transaction = session.execute(
            select(Transaction)
            .where(
                Transaction.transaction_id == result["transaction_id"]
            )
        ).scalar_one()

    assert transaction.wallet_id == "TESTW001"
    assert transaction.type == "deposit"
    assert transaction.amount == Decimal("100")