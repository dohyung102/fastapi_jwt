import pytest

from fastapi import Depends
from fastapi.testclient import TestClient

from ..main import app, get_db
from ..models import userModel
from .config_test import engine, TestSessionLocal

userModel.Base.metadata.create_all(bind=engine)

# @pytest.fixture
def get_test_db():
    test_db = TestSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


def test_create_user():
    user = {
        'id': 'dohyung102',
        'email': 'dohyung102@naver.com',
        'password': 'testtest2@',
        'password_validation': 'testtest2@'
    }
    response = client.post('/users', json=user)
    assert response.status_code == 200

def test_certificate_email():
    pass