from datetime import date, datetime

from pydantic import BaseModel, constr, validator

class UserBase(BaseModel):
    id: constr(min_length=5, max_length=20)
    email: constr(regex=r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.[a-z]+$')

class UserCreate(UserBase):
    password: constr(regex=r'^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}')
    
class UserValid(UserCreate):
    password_validation: constr(min_length=8, max_length=20)

    @validator('password_validation')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class User(UserBase):
    registration_date: date
    is_admin: bool | None = False

    class Config:
        orm_mode = True


class UserEmail(BaseModel):
    email: constr(regex=r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.[a-z]+$')


class UserTokenBase(BaseModel):
    access_token: str
    refresh_token: str

class UserToken(UserTokenBase):
    id: int
    login_date: date

    class Config:
        orm_mode = True