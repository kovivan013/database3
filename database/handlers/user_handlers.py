import starlette.status
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from database3.database.database.db_connect import get_db
from database3.database.models.models import User
from database3.database.schemas.data_schemas import DataStructure
from database3.database.schemas.schemas import UserCreate

user_router = APIRouter()

@user_router.post("/create_user", response_model=DataStructure)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = DataStructure()

    user_exists: bool = db.query(User).filter(User.telegram_id == user.telegram_id).first() is not None
    if user_exists:
        raise HTTPException(status_code=starlette.status.HTTP_409_CONFLICT, detail="user exists")

    data: dict = {
        "telegram_id": user.telegram_id,
        "username": user.username
    }

    new_user = User(**data)
    db.add(new_user)
    db.commit()

    return result