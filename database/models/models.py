import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, BigInteger, JSON

BaseModel = sqlalchemy.orm.declarative_base()

class User(BaseModel):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, default="")
    classes = Column(JSON, default={})