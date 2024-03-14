import os
from datetime import datetime
from typing import Union

from dotenv import load_dotenv
from requests_oauth2client import OAuth2Client, OAuth2ClientCredentialsAuth

from tiercepiscinebot.params import *

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

    def get_user_info(self, user) -> dict:
        response = self.session.get(
            f"https://api.intra.42.fr/v2/users/{user}",
            params={"cursus_id": "c-piscine"},
        )
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def user_get_level(response: dict) -> Union[None, str]:
        return response.get("cursus_users", [{}])[0].get("level", None)

    @staticmethod
    def user_get_exam(response: dict, exam_nbr: int) -> Union[None, int]:
        if exam_nbr != 3:
            k = f"c-piscine-exam-0{exam_nbr}"
        else:
            k = "c-piscine-final-exam"
        for v in response.get("projects_users", []):
            if v.get("project", {}).get("slug", {}) == k:
                return v.get("final_mark", None)

    @staticmethod
    def user_get_exercice(
        response: dict, exercice_id: int
    ) -> Union[tuple[datetime, int], None]:
        if not response:
            return None
        for i in response.get("projects_users", None):
            if not i:
                return None
            if i.get("project", {}).get("id", 0) == exercice_id:
                if i.get("validated?"):
                    return (i["marked_at"], i["final_mark"])
                return None
        return None


if __name__ == "__main__":
    handler = API_handler()
    res = handler.get_user_info("rdupeux")
    with open("test.json", "w") as f:
        json.dump(res, f)
    # print(API_handler.user_get_exam(res, 3))
    # print(API_handler.user_get_exam(res, 3))
