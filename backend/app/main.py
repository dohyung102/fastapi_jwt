from fastapi import FastAPI

from .database import SessionLocal
from .router import userRouter
from .error import commonExceptions, userExceptions


app = FastAPI()
commonExceptions.include_app(app)
userExceptions.include_app(app)

app.include_router(userRouter.router)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
