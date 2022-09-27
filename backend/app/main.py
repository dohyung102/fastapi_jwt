from fastapi import FastAPI

from .database import SessionLocal
from .router import userRouter


app = FastAPI()


app.include_router(userRouter.router)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
