from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database3.database.database.db_connect import get_db
from database3.database.models.models import User
from database3.database.schemas.schemas import UserCreate

user_router = APIRouter()

@user_router.post("/create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    data: dict = {
        "telegram_id": user.telegram_id,
        "username": user.username
    }

    new_user = User(**data)
    db.add(new_user)
    db.commit()