from fastapi.testclient import TestClient
import app.services as services
from app.main import app


client = TestClient(app)

def test_transaction_endpoint_deposit(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    response = client.post(
        "/wallets/TESTW001/transactions",
        json={
            "type": "deposit",
            "amount": "100",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["wallet_id"] == "TESTW001"
    assert data["new_balance"] == 600
    assert data["transaction_id"]

def test_transaction_endpoint_withdraw(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    response = client.post(
        "/wallets/TESTW001/transactions",
        json={
            "type": "withdraw",
            "amount": "100",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["wallet_id"] == "TESTW001"
    assert data["new_balance"] == 400
    assert data["transaction_id"]
    
    
def test_transaction_endpoint_wallet_not_found(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    response = client.post(
        "/wallets/DOESNOTEXIST/transactions",
        json={
            "type": "withdraw",
            "amount": "100",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet does not exist"
    
def test_transaction_endpoint_insufficient_balance(monkeypatch, test_session_factory):
    monkeypatch.setattr(services, "get_session", test_session_factory)

    response = client.post(
        "/wallets/TESTW001/transactions",
        json={
            "type": "withdraw",
            "amount": "600",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient balance"


def test_transaction_endpoint_invalid_amount():

    response = client.post(
        "/wallets/TESTW001/transactions",
        json={
            "type": "withdraw",
            "amount": "-100",
        },
    )

    assert response.status_code == 422
    

def test_transaction_endpoint_invalid_transaction():

    response = client.post(
        "/wallets/TESTW001/transactions",
        json={
            "type": "banana",
            "amount": "100",
        },
    )

    assert response.status_code == 422
    

