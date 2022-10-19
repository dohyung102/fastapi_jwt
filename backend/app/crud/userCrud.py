from sqlalchemy.orm import Session

from ..models import userModel
from ..schemas import userSchemas

def get_user_by_id(db: Session, id: str):
    return db.query(userModel.User).filter(userModel.User.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(userModel.User).filter(userModel.User.email == email).first()

def get_user_by_id_or_email(db: Session, id: str, email: str):
    return db.query(userModel.User).filter((userModel.User.email == email) | (userModel.User.id == id)).first()

def get_user_by_id_and_email(db: Session, id: str, email: str):
    return db.query(userModel.User).filter(userModel.User.id == id, userModel.User.email == email).first()

def create_user(db: Session, user: userSchemas.UserCreate):
    db_user = userModel.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id_and_password(db: Session, id: str, password: str):
    return db.query(userModel.User).filter(userModel.User.id == id, userModel.User.password == password).first()

def get_login_user_by_user_id(db: Session, user_id: str):
    return db.query(userModel.UserSession).filter(userModel.UserSession.user_id == user_id).first()

def login_user(db: Session, user: userSchemas.UserTokenBase):
    db_login_user = userModel.UserToken(**user.dict())
    db.add(db_login_user)
    db.commit()
    db.refresh(db_login_user)
    return db_login_user

def get_user_id_by_email(db: Session, email: str):
    return db.query(userModel.User.id).filter(userModel.User.email == email).first()

def get_user_token_by_access_token(db: Session, access_token: str):
    return db.query(userModel.UserToken).filter(userModel.UserToken.access_token == access_token).first()

def update_user_password(db: Session, user: userSchemas.UserCreate):
    db_user = db.query(userModel.User).filter(userModel.User.id == user.id, userModel.User.email == user.email).update(
        dict(password=user.password)
    )
    db.commit()
    return db_user