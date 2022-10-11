from urllib import response
import pytest

from fastapi import Depends
from fastapi.testclient import TestClient

from ..main import app, get_db
from ..models import userModel
from .config_test import engine, get_test_db

userModel.Base.metadata.create_all(bind=engine)




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

def test_create_same_user():
    user = {
        'id': 'dohyung102',
        'email': 'dohyung102@naver.com',
        'password': 'testtest2@',
        'password_validation': 'testtest2@'
    }
    
    response = client.post('/users', json=user)
    assert response.status_code == 400
    
def test_create_id_is_not_valid_user():
    user = {
        'id': 'doh',
        'email': 'dohyung102@naver.com',
        'password': 'testtest2@',
        'password_validation': 'testtest2@'
    }
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_email_is_not_valid_user():
    user = {
        'id': 'dohyung102',
        'email': 'dohyung102@nave',
        'password': 'testtest2@',
        'password_validation': 'testtest2@'
    }
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_password_is_not_valid_user():
    user = {
        'id': 'dohyung102',
        'email': 'dohyung102@naver.com',
        'password': 'testtest2',
        'password_validation': 'testtest2'
    }
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_password_not_match_user():
    user = {
        'id': 'dohyung102',
        'email': 'dohyung102@naver.com',
        'password': 'testtest2@',
        'password_validation': 'testtest3@'
    }
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    

def test_certificate_email():
    email = "dohyung102@naver.com"
    response = client.get('/users/certification', params={"email": email})
    assert response.status_code == 200
