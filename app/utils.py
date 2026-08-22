from uuid import uuid4


def generate_user_id() -> str:
    return uuid4().hex[:10].upper()


def generate_transaction_id() -> str:
    return uuid4().hex[:10].upper()

def generate_wallet_id() -> str:
    return uuid4().hex[:10].upper()