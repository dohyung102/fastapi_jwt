from fastapi.testclient import TestClient

from main import app, get_db
from models import userModel
from .config_test import engine, get_test_db

userModel.Base.metadata.create_all(bind=engine)




app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


class User:
    def __init__(self, id, email, password,password_validation):
        self.id = id
        self.email = email
        self.password = password
        self.password_validation = password_validation
        self.access_token = ''

    def get_user_data(self):
        user = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'password_validation': self.password_validation
        }
        return user

    def get_user_login_data(self):
        user = {
            'username': self.id,
            'password': self.password
        }
        return user

    def get_aceess_token(self):
        return self.access_token
    
    def set_access_token(self, access_token):
        self.access_token = access_token


test_user = User('dohyung102', 'dohyung102@naver.com', 'testtest2@', 'testtest2@')


def test_create_user():
    user = test_user.get_user_data()
    response = client.post('/users', json=user)
    assert response.status_code == 200

def test_create_same_user():
    user = test_user.get_user_data()
    
    response = client.post('/users', json=user)
    assert response.status_code == 400
    
def test_create_id_is_not_valid_user():
    user = test_user.get_user_data()
    user['id'] = 'doh'
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_email_is_not_valid_user():
    user = test_user.get_user_data()
    user['email'] = 'dohyung102@nave'
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_password_is_not_valid_user():
    user = test_user.get_user_data()
    user['password'] = 'testtest2'
    user['password_validation'] = 'testtest2'
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
def test_create_password_not_match_user():
    user = test_user.get_user_data()
    user['password'] = 'testtest2@'
    user['password_validation'] = 'testtest3@'
    
    response = client.post('/users', json=user)
    assert response.status_code == 422
    
# def test_certificate_email():
#     email = "dohyung102@naver.com"
#     response = client.get('/users/certification', params={"email": email})
#     assert response.status_code == 200

def test_login_user():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    user = test_user.get_user_login_data()
    response = client.post('/users/login', data=user, headers=headers)
    test_user.set_access_token(response.json()['access_token'])
    assert response.status_code == 200

def test_delete_user():
    user_id = test_user.id
    token = test_user.get_aceess_token()
    response = client.delete(f'/users/{user_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200