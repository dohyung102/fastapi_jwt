from enum import unique
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.sql import func

from ..database import Base

class User(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String, unique=True)
    registration_date = Column(Date, server_default=func.now())
    is_admin = Column(Boolean)

class UserToken(Base):
    __tablename__ = "UserToken"

    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True)
    refresh_token = Column(String, unique=True)
    login_date = Column(DateTime(timezone=True), server_default=func.now())
