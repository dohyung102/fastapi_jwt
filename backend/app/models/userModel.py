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

class UserSession(Base):
    __tablename__ = "UserSession"

    id = Column(Integer, primary_key=True)
    session_key = Column(String, unique=True)
    login_date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, ForeignKey("User.id"))