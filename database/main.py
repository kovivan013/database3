import uvicorn
from fastapi import FastAPI

from config import settings
from database3.database.routers import api_router

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(api_router)

    return application

app = get_application()

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )