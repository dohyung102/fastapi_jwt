from datetime import datetime, timedelta
import random, string, os, yagmail

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..main import get_db
from ..database import engine
from ..crud import userCrud
from ..schemas import userSchemas
from ..models import userModel
from ..error.commonExceptions import ExistException, NotFoundException
from ..error.userExceptions import PasswordNotMatchException

ACCESS_SECRET_KEY = "5b7caa062f47fefeece8e25004fd2ac62e40109227a948972d35ffbc8a26ef1f"
REFRESH_SECRET_KEY = "ea04ecd2790f5171341279f0134e29adcd7c1c80b1641761"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_MINUTES = 2880

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
        print('sended')
    except Exception as e:
        print(e)
    
def create_token(data: dict, expries_delta: timedelta, secret_key: str):
    to_encode = data.copy()
    expire =datetime.utcnow() + expries_delta
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encode_jwt

@router.post("", response_model=userSchemas.User)
def create_user(user: userSchemas.UserValid, db: Session = Depends(get_db)):
    db_user = userCrud.get_user_by_id_or_email(db, id=user.id, email=user.email)
    if db_user:
        raise ExistException(name=f"{user.id} or {user.email}") 
    user.password = pwd_context.hash(user.password)
    create_user = userSchemas.UserCreate(**user.dict())
    return userCrud.create_user(db, user=create_user)

@router.get("/certification")
def certificate_email(email: str, background_tasks: BackgroundTasks):
    str_length = random.randint(4, 6)
    str_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_length))
    background_tasks.add_task(
        send_certification_email, email=email, value=str_value
    )
    return str_value

@router.post("/login", response_model=userSchemas.UserToken)
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = userCrud.get_user_by_id_and_password(db, id=user.username, password=pwd_context.hash(user.password))
    if not db_user:
        raise NotFoundException(name=user.id)
    access_token_expires, refresh_token_expires = map(lambda minutes: timedelta(minutes=minutes), [ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES])
    users = [{"sub": user.username}, {"sub": user.username}]
    expires = [access_token_expires, refresh_token_expires]
    secret_keys = [ACCESS_SECRET_KEY, REFRESH_SECRET_KEY]
    access_token, refresh_token = map(create_token, users, expires, secret_keys)
    no_login_user = userSchemas.UserTokenBase(access_token=access_token, refresh_token=refresh_token)
    return userCrud.login_user(db, user=no_login_user)
