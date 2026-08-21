import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")
if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
test_engine = create_engine(TEST_DATABASE_URL)

def get_session():
    return Session(engine)   

def get_test_session():
    return Session(test_engine)