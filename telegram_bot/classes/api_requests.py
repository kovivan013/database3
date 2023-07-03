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