from datetime import date, datetime

from pydantic import BaseModel, constr, validator

class UserBase(BaseModel):
    id: constr(min_length=5, max_length=20)
    email: constr(regex=r'[A-Za-z]+@[a-z]+\.[a-z]+')

class UserCreate(UserBase):
    password: constr(regex=r'^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}')
    password_validation: constr(min_length=8, max_length=20)

    @validator('password_validation')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class User(UserBase):
    registration_date: date
    is_admin: bool

    class Config:
        orm_mode = True


class UserSessionBase(BaseModel):
    user_id: constr(min_length=5, max_length=20)

class UserSessionCreate(UserSessionBase):
    password: constr(min_length=8, max_length=20)

class UserSession(UserSessionBase):
    id: int
    session_key: str
    login_date: datetime

    class Config:
        orm_mode = True