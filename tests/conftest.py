import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import test_engine


@pytest.fixture
def test_session_factory():
    connection = test_engine.connect()
    transaction = connection.begin()

    with Session(connection) as setup_session:
        setup_session.execute(
            text("""
                UPDATE wallets
                SET balance = 500
                WHERE wallet_id = 'TESTW001'
            """)
        )

        setup_session.execute(
            text("""
                DELETE FROM transactions
                WHERE wallet_id = 'TESTW001'
            """)
        )

        setup_session.flush()

    def factory():
        return Session(
            connection,
            join_transaction_mode="create_savepoint",
        )

    yield factory

    transaction.rollback()
    connection.close()