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
from ..common import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
from ..error.commonExceptions import ExistException, NotFoundException
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
def certificate_email(email: str, background_tasks: BackgroundTasks, user_id: str = None, regist: bool = False, db: Session = Depends(get_db)):
    if regist:
        if user_id:
            user = userCrud.get_user_by_id_and_email(db, user_id, email)
        else:
            user = userCrud.get_user_by_email(db, email)
        if not user:
            raise NotFoundException(name=email)
    str_length = random.randint(4, 6)
    str_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_length))
    background_tasks.add_task(
        send_certification_email, email=email, value=str_value
    )
    if regist and not user_id:
        data = dict(str_value=str_value, user_id=user.id)
        return data
    else:
        return str_value

@router.post("/login", response_model=userSchemas.UserToken)
def login_user(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = userCrud.get_user_by_id(db, id=user.username)
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise NotFoundException(name=user.username)
    access_token_expires, refresh_token_expires = map(lambda minutes: timedelta(minutes=minutes), [ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES])
    users = [{"sub": user.username}, {"sub": user.username}]
    expires = [access_token_expires, refresh_token_expires]
    secret_keys = [ACCESS_SECRET_KEY, REFRESH_SECRET_KEY]
    access_token, refresh_token = map(create_token, users, expires, secret_keys)
    no_login_user = userSchemas.UserTokenBase(access_token=access_token, refresh_token=refresh_token)
    return userCrud.login_user(db, user=no_login_user)

@router.get("/{userId}", response_model=userSchemas.User)
def get_user(userId: str, db: Session = Depends(get_db)):
    return userCrud.get_user_by_id(db, userId)

@router.get("/find-user-id")
def find_user_id(user: userSchemas.UserEmail, db: Session = Depends(get_db)):
    return userCrud.get_user_id_by_email(db, email=user.email)

@router.put("/change-password", response_model=userSchemas.User)
def change_password(user: userSchemas.UserValid, db: Session = Depends(get_db)):
    user.password = pwd_context.hash(user.password)
    update_user = userSchemas.UserCreate(**user.dict())
    return userCrud.update_user_password(db, user=update_user)


