from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database3.database.database.db_connect import get_db

from database3.database.schemas.response_schemas import ResponseStructure
from database3.database.schemas.request_schemas import GetUser
from database3.database.models.models import User
from database3.database.schemas.exceptions_schemas import ItemNotFoundException

admin_router = APIRouter()

@admin_router.post("/user_classes")
def get_user_classes(data: GetUser, db: Session = Depends(get_db)):
    result = ResponseStructure()

    user = db.query(User).filter(User.telegram_id == data.telegram_id).first()
    if user:
        return dict(user.classes)
    raise ItemNotFoundException

@admin_router.get("/get_all_users")
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()
    for i in users:
        classes: dict = dict(i.classes)
        if classes:
            print(f"ID - {i.telegram_id}:")
            for j, v in enumerate(classes.values(), start=1):
                cls = {v.get("invite_code"): v.get("id")}
                print(f"| {j}. {cls}")
    return users
