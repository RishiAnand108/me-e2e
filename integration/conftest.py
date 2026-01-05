import pytest
import requests


class MonkeysAuth:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json"
        }

    def register(self, first_name, last_name, email, password):
        url = f"{self.base_url}/api/v1/auth/register"
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        return requests.post(url, json=payload, headers=self.headers)

    def login(self, email, password):
        url = f"{self.base_url}/api/v1/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(url, json=payload, headers=self.headers)


@pytest.fixture(scope="session")
def client():
    return MonkeysAuth("https://dev.monkeys.support")
