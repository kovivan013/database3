from fastapi import Depends, APIRouter, Response
from starlette import status
from sqlalchemy.orm import Session

from database3.database.database.db_connect import get_db
from database3.database.models.models import User
from database3.database.schemas.response_schemas import DataStructure, ResponseStructure
from database3.database.schemas.request_schemas import UserCreate
from database3.database.schemas.exceptions_schemas import UserExistsException

user_router = APIRouter()

@user_router.post("/create_user", response_model=ResponseStructure)
def create_user(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    result = ResponseStructure()

    user_exists: bool = db.query(User).filter(User.telegram_id == user.telegram_id).first() is not None
    if user_exists:
        raise UserExistsException

    data: dict = {
        "telegram_id": user.telegram_id,
        "username": user.username
    }

    new_user = User(**data)
    db.add(new_user)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return result.as_dict()