

import requests
from .base_client import BaseClient


class CookieClient(BaseClient):

    def set_cookie(self, name: str, value: str):
        """Сервис устанавливает куки через Set-Cookie и делает Session"""
        return self._get("/cookies/set", params={"name": name, "value": value})

    def get_cookie(self):
        """Cервер возвращает те куки, реально получил от запроса"""
        return self._get("/cookies")

    def post_echo(self, data: dict):
        """POST: в ответе будет эхо загаловка, включая куки"""
        return self._post("/post", json=data)

