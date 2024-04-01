from datetime import date, datetime
import re

from pydantic import BaseModel, constr, validator, Field, field_validator

class UserBase(BaseModel):
    id: constr(min_length=5, max_length=20)
    email: constr(pattern=r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.[a-z]+$')

class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def regex_match(cls, p: str) -> str:
        re_for_pw: re.Pattern[str] = re.compile(r"^(?=.*?[\d])(?=.*?[a-z])(?=.*?[!@#$%^&*()])[\w\d!@#$%^&*()]{8,20}")
        if not re_for_pw.match(p):
            raise ValueError("invalid password")
        return p

    
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
        from_attribute = True


class UserEmail(BaseModel):
    email: constr(pattern=r'^[A-Za-z0-9]+@[A-Za-z0-9]+\.[a-z]+$')


class UserToken(BaseModel):
    access_token: str
    refresh_token: str

