import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from app.exceptions import UnauthorizedUserAccessError

import jwt

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedUserAccessError(
                "Invalid access token"
            )

        return user_id

    except InvalidTokenError:
        raise UnauthorizedUserAccessError(
            "Invalid access token"
        )