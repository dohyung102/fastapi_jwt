from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = "dohyung102"
password = "dohyung"
host = "127.0.0.1"
port = "5432"
name = "develop"

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=1
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()