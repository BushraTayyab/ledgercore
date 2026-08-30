import jwt
import pytest
from datetime import datetime, timedelta, timezone

from app.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    verify_access_token,
    
)

from app.exceptions import UnauthorizedUserAccessError


def test_create_access_token():
    token = create_access_token("TEST002")

    assert token is not None
    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert payload["sub"] == "TEST002"
    assert "exp" in payload

def test_verify_access_token():
    token = create_access_token("TEST002")

    user_id = verify_access_token(token)

    assert user_id == "TEST002"

def test_verify_access_token_invalid():
    with pytest.raises(
        UnauthorizedUserAccessError,
        match="Invalid access token",
    ):
        verify_access_token("this-is-not-a-valid-token")
        
def test_verify_access_token_wrong_signature():
    token = jwt.encode(
        {
            "sub": "TEST002",           #exp is not a required field in payload
        },
        "THIS_IS_A_DIFFERENT_SECRET_KEY_12345",
        algorithm=ALGORITHM,
    )

    with pytest.raises(
        UnauthorizedUserAccessError,
        match="Invalid access token",
    ):
        verify_access_token(token)

def test_verify_access_token_expired():
    token = jwt.encode(
        {
            "sub": "TEST002",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(
        UnauthorizedUserAccessError,
        match="Invalid access token",
    ):
        verify_access_token(token)
        
def test_verify_access_token_missing_sub():
    token = jwt.encode(
        {
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    with pytest.raises(
        UnauthorizedUserAccessError,
        match="Invalid access token",
    ):
        verify_access_token(token)