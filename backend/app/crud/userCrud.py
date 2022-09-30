from sqlalchemy.orm import Session

from ..models import userModel
from ..schemas import userSchemas

def get_user_by_id(db: Session, id: str):
    return db.query(userModel).filter(userModel.id == id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(userModel).filter(userModel.email == email).first()

def get_user_by_id_or_email(db: Session, id: str, email: str):
    return db.query(userModel).filter(userModel.email == email or userModel.id == id).first()

def create_user(db: Session, user: userSchemas.UserCreate):
    db_user = userModel.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
