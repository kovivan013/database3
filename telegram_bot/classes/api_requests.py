from database3.telegram_bot.config import BASE_API_URL
from database3.telegram_bot.api.request_classes import GetRequest, PostRequest

class API:

    __BASE_SERVER_URL: str = BASE_API_URL

    @classmethod
    async def _get_request(cls, endpoint: str):

        url: str = cls.__BASE_SERVER_URL + endpoint
        return await GetRequest(url=url).send_request()

    @classmethod
    async def _post_request(cls, data: dict, endpoint: str):

        url: str = cls.__BASE_SERVER_URL + endpoint
        return await PostRequest(data=data, url=url).send_request()


class UserAPI(API):

    __URL: str = "/user"

    @classmethod
    async def create_user(cls, telegram_id: int, username: str):

        endpoint: str = cls.__URL + "/create_user"
        data: dict = {
            "telegram_id": telegram_id,
            "username": username
        }

        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    async def create_class(cls, telegram_id: int, name: str, description: str = ""):

        endpoint: str = cls.__URL + "/create_class"
        data: dict = {
            "owner": telegram_id,
            "name": name,
            "description": description
        }

        return await cls._post_request(data=data, endpoint=endpoint)

class AdminAPI(API):

    __URL: str = "/admin"

    @classmethod
    async def get_user_classes(cls, telegram_id: int):

        endpoint: str = cls.__URL + f"/user_classes"
        data: dict = {
            "telegram_id": telegram_id
        }

        return await cls._post_request(data=data, endpoint=endpoint)

import asyncio
import random
import string
for i in range(1,2001):
    asyncio.run(UserAPI.create_user(telegram_id=i, username=""))
    for v in range(2):
        asyncio.run(UserAPI.create_class(telegram_id=i, name="".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for j in range(6))))