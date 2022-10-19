from fastapi import Header, Depends
from jose import jwt, JWTError
from backend.app.error.userExceptions import NotAuthenticateException
from common import ALGORITHM, ACCESS_SECRET_KEY

from sqlalchemy.orm import Session

from .main import get_db
from .crud import userCrud
from .error import NotAuthenticateException

async def verify_jwt(jwt_token: str = Header(...), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(jwt_token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise NotAuthenticateException()
    except:
        raise NotAuthenticateException()
    db_token = userCrud.get_user_token_by_access_token(db, access_token=jwt_token)
    if not db_token:
        raise NotAuthenticateException()
    