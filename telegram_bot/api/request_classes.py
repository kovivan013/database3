import aiohttp

from abc import abstractmethod, ABC
from database3.database.schemas.response_schemas import DataStructure

class RequestSender(ABC):

    def __init__(self, url: str = ""):
        self.url: str = url
        self._payload: dict = {}

    @abstractmethod
    async def _send(self):
        pass

    async def send_request(self):

        self._payload: dict = {
            "url": self.url
        }
        session_params: dict = {
            "trust_env": True,
            "connector": aiohttp.TCPConnector()
        }

        try:
            async with aiohttp.ClientSession(**session_params) as session:
                answer: dict =  await self._send(session)
        except:
            raise Exception("API_ERROR")

        status = answer.get("status")
        data: dict = answer.get("answer_data")

        return DataStructure(status=status, data=data).as_dict()

class GetRequest(RequestSender):

    async def _send(self, session):
        async with session.get(**self._payload) as response:

            return {
                "status": response.status,
                "answer_data": await response.json()
            }

class PostRequest(RequestSender):

    def __init__(self, data: dict = None, url: str = ""):
        super().__init__(url)
        self._data_for_send: dict = data

    async def _send(self, session):

        self._payload.update(json=self._data_for_send)
        async with session.post(**self._payload) as response:

            return {
                "status": response.status,
                "answer_data": await response.json()
            }

