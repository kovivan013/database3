from starlette import status
from fastapi import HTTPException

UserExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"
)