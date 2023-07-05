from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database3.database.database.db_connect import get_db

from database3.database.schemas.response_schemas import ResponseStructure
from database3.database.schemas.request_schemas import GetUser
from database3.database.models.models import User

admin_router = APIRouter()

@admin_router.post("/user_classes")
def get_user_classes(data: GetUser, db: Session = Depends(get_db)):
    result = ResponseStructure()

    user = db.query(User).filter(User.telegram_id == data.telegram_id).first()
    if user:
        return dict(user.classes)
    raise
