import marshmallow_dataclass
import requests

from .dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates')
        response = requests.get(url, params={'offset': offset, 'timeout': timeout}).json()
        GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        obj = GetUpdatesResponseSchema().load(response)
        return obj

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        req = self.get_url('sendMessage') + f'?chat_id={chat_id}&text={text}'
        resp = requests.get(req).json()
        SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
        obj = SendMessageResponseSchema().load(resp)
        return obj
