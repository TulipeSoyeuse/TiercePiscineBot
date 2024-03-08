import os

from dotenv import load_dotenv
from requests_oauth2client import OAuth2Client, OAuth2ClientCredentialsAuth

load_dotenv()

import json

import requests


class API_handler:
    def __init__(self):
        self.client = OAuth2Client(
            "https://api.intra.42.fr/oauth/token",
            auth=(os.getenv("UID"), os.getenv("SECRET")),
        )
        self.session = requests.Session()
        self.session.auth = OAuth2ClientCredentialsAuth(self.client)

    def get_user_info(self, user):
        response = self.session.get(
            f"https://api.intra.42.fr/v2/users/{user}",
            params={"cursus_id": "c-piscine"},
        )
        if response.status_code == 200:
            return response.json()


if __name__ == "__main__":
    handler = API_handler()
    res = handler.get_user_info("rdupeux")
    with open("test.json", "w") as f:
        json.dump(res, f)
