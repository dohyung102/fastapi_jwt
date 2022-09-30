from fastapi import status, Request
from fastapi.responses import JSONResponse


class PasswordNotMatchException(Exception):
    pass


def password_not_match_exception_handler(request: Request, exc: PasswordNotMatchException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"password not match"})

def include_app(app):
	app.add_exception_handler(PasswordNotMatchException, password_not_match_exception_handler)