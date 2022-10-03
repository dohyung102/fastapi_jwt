import os

from fastapi import FastAPI, Depends

from .database import SessionLocal, get_db
from .router import userRouter
from .error import commonExceptions, userExceptions


app = FastAPI(dependencies=[Depends(get_db)])


commonExceptions.include_app(app)
userExceptions.include_app(app)

app.include_router(userRouter.router)



@app.on_event('startup')
def startup_test_code():
    os.system('pytest -v')