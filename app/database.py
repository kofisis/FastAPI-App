from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_port}/{settings.db_hostname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#function to start session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

