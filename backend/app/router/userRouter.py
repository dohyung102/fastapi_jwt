import random, string, os, yagmail

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database import SessionLocal
from ..crud import userCrud
from ..schemas import userSchemas
from ..error.commonExceptions import ExistException
from ..error.userExceptions import PasswordNotMatchException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_certification_email(email: str, value: str):
    gmail = os.environ.get("Gmail", None)
    password = os.environ.get("GmailPassword", None)
    try:
        yag = yagmail.SMTP({gmail: "개발용"}, password)
        yag.send(email, "인증용 메일입니다.", value)
    except Exception as e:
        print(e)
    

@router.post("/users", response_model=userSchemas.User)
def create_user(user: userSchemas.UserCreate, db: Session = Depends(get_db)):
    if not user.password == user.password_validation:
        raise PasswordNotMatchException()
    db_user = userCrud.get_user_by_id_or_email(db, id=user.id, email=user.email)
    if db_user:
        raise ExistException(name=f"{user.id} or {user.email}") 
    user.password = pwd_context.hash(user.password)
    return userCrud.create_user(db, user=user)

@router.get("/users/certification")
def certificate_email(email: str, background_tasks: BackgroundTasks):
    str_length = random.randint(4, 6)
    str_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_length))
    background_tasks.add_task(
        send_certification_email, email=email, value=str_value
    )
    return str_value
