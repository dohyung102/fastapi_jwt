import random, string, os, yagmail

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..main import get_db
from ..database import SessionLocal, engine
from ..crud import userCrud
from ..schemas import userSchemas
from ..models import userModel
from ..error.commonExceptions import ExistException
from ..error.userExceptions import PasswordNotMatchException

userModel.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

def send_certification_email(email: str, value: str):
    gmail = os.environ.get("Gmail", None)
    password = os.environ.get("GmailPassword", None)
    try:
        yag = yagmail.SMTP({gmail: "개발용"}, password)
        yag.send(email, "인증용 메일입니다.", value)
    except Exception as e:
        print(e)
    

@router.post("", response_model=userSchemas.User)
def create_user(user: userSchemas.UserValid):
    db_user = userCrud.get_user_by_id_or_email(next(get_db()), id=user.id, email=user.email)
    if db_user:
        raise ExistException(name=f"{user.id} or {user.email}") 
    user.password = pwd_context.hash(user.password)
    create_user = userSchemas.UserCreate(**user.dict())
    return userCrud.create_user(next(get_db), user=create_user)

@router.get("/certification")
def certificate_email(email: str, background_tasks: BackgroundTasks):
    str_length = random.randint(4, 6)
    str_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_length))
    background_tasks.add_task(
        send_certification_email, email=email, value=str_value
    )
    return str_value
