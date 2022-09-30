from fastapi import status, Request
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class ExistException(Exception):
    def __init__(self, name: str):
        self.name = name


def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f"{exc.name} is not found"})

def exist_exception_handler(requset: Request, exc: ExistException):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{exc.name} is already exist"})

def include_app(app):
	app.add_exception_handler(NotFoundException, not_found_exception_handler)
	app.add_exception_handler(ExistException, exist_exception_handler)