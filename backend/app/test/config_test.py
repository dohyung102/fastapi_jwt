import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session ,sessionmaker


user = "dohyung102"
password = "dohyung"
host = "127.0.0.1"
port = "5432"
name = "test_develop"

TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, pool_size=1
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

