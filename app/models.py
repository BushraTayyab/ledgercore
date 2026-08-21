from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    user_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_joined: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("CURRENT_DATE"),
    )


class Wallet(Base):
    __tablename__ = "wallets"

    __table_args__ = (
        CheckConstraint(
            "balance >= 0.00",
            name="wallets_balance_check",
        ),
        CheckConstraint(
            "status IN ('active', 'closed')",
            name="wallets_status_check",
        ),
    )

    wallet_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("users.user_id"),
        nullable=False,
    )

    balance: Mapped[Decimal | None] = mapped_column(
        Numeric,
        server_default=text("0.00"),
    )

    status: Mapped[str | None] = mapped_column(
        String(6),
        server_default=text("'active'"),
    )

    date_created: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("CURRENT_DATE"),
    )


class Transaction(Base):
    __tablename__ = "transactions"

    __table_args__ = (
        CheckConstraint(
            "amount > 0.00",
            name="transactions_amount_check",
        ),
        CheckConstraint(
            "type IN ('withdraw', 'deposit')",
            name="transactions_type_check",
        ),
    )

    transaction_id: Mapped[str] = mapped_column(
        String(10),
        primary_key=True,
    )

    wallet_id: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("wallets.wallet_id"),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric,
        nullable=False,
    )

    time_stamp: Mapped[datetime | None] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
    )