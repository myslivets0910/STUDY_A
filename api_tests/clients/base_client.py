
import requests
from typing import Optional, Any, Dict


class BaseClient:

    def __init__(self, base_url: str):
        self.base_url = base_url # указываем базовую URL в conftest.py
        self.session = requests.Session()


    def _get(self, endpoint : str, params : Optional[str, Any] = None, headers : Optional[str, Any] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, headers=headers)
        return response

    def _post(self, endpoint : str, params : Optional[str] = None, headers : Optional[str] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, params=params, headers=headers)
        return response

    def _put(self, endpoint : str, params : Optional[str] = None, headers : Optional[str] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, params=params, headers=headers)
        return response

    def _delete(self, endpoint : str, params : Optional[str] = None, headers : Optional[str] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url, params=params, headers=headers)
        return response