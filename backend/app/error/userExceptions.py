from fastapi import status, Request
from fastapi.responses import JSONResponse


class PasswordNotMatchException(Exception):
    pass

class NotAuthenticateException(Exception):
    pass

class NotUserAndUserTokenMatchException(Exception):
     pass


def password_not_match_exception_handler(request: Request, exc: PasswordNotMatchException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "password not match"})

def not_authenticate_exception_handler(request: Request, exc: NotAuthenticateException):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "you are not authenticated"})

def not_user_and_user_token_match_exception_handler(request: Request, exc: NotUserAndUserTokenMatchException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "user id not matched"})

def include_app(app):
	app.add_exception_handler(PasswordNotMatchException, password_not_match_exception_handler)
	app.add_exception_handler(NotAuthenticateException, not_authenticate_exception_handler)
	app.add_exception_handler(NotUserAndUserTokenMatchException, not_user_and_user_token_match_exception_handler)