from database3.database.config import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(db.get_db_name())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()