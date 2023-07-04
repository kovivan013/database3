from fastapi import Depends, APIRouter, Response
from starlette import status
from sqlalchemy.orm import Session

from database3.database.utils.utils import gen_uuid
from database3.database.database.db_connect import get_db
from database3.database.models.models import User
from database3.database.schemas.response_schemas import DataStructure, ResponseStructure
from database3.database.schemas.request_schemas import UserCreate, ClassCreate
from database3.database.schemas.exceptions_schemas import ItemExistsException

user_router = APIRouter()

@user_router.post("/create_user", response_model=ResponseStructure)
def create_user(new_user: UserCreate, response: Response, db: Session = Depends(get_db)):
    result = ResponseStructure()

    user_exists: bool = db.query(User).filter(User.telegram_id == new_user.telegram_id).first() is not None
    if user_exists:
        raise ItemExistsException

    data: dict = {
        "telegram_id": new_user.telegram_id,
        "username": new_user.username
    }

    user = User(**data)
    db.add(user)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return result.as_dict()

@user_router.post("/create_class", response_model=ResponseStructure)
def create_class(new_class: ClassCreate, response: Response, db: Session = Depends(get_db)):
    result = ResponseStructure()

    user = db.query(User).filter(User.telegram_id == new_class.owner).first()
    edit_class: str = new_class.name
    data: dict = dict(user.classes)

    if edit_class in data:
        raise ItemExistsException

    data.update({edit_class: new_class.as_dict()})

    data.get(edit_class).update({"id": str(gen_uuid())})
    data.get(edit_class).update({"all_users": [new_class.owner]})
    data.get(edit_class).update({"description": new_class.description})

    user.classes = data
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    return result.as_dict()