import sqlite3
import traceback
from sqlite3 import IntegrityError

from tiercepiscinebot.api import API_handler


class Database:
    def __init__(self) -> None:
        self.poulain = False
        self.con = sqlite3.connect("poulain.db")
        self.handler = API_handler()

    def cursor_handler(func):
        def wrapper(*args):
            cursor = args[0].con.cursor()
            res = func(*args, cursor)
            cursor.close()
            return res

        return wrapper

    @cursor_handler
    def add_poulain(self, poulain: str, mentor: str, cursor: sqlite3.Cursor) -> str:
        if not self.poulain:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS poulains (
	                        poulain_id INTEGER PRIMARY KEY,
	                        intraID TEXT NOT NULL UNIQUE,
	                        mentorID TEXT NOT NULL UNIQUE)"""
            )
            self.poulain = True

        poulain_ = self.handler.get_user_info(poulain)
        if not poulain_:
            return "stp passe moi un login correct par pitié (le poulain existe po)"
        mentor_ = self.handler.get_user_info(mentor)
        if not mentor_:
            return "stp passe moi un login correct par pitié (le mentor existe po)"
        try:
            cursor.execute(
                f"INSERT INTO poulains(intraID, mentorID) VALUES('{poulain}', '{mentor}')"
            )
        except IntegrityError as e:
            return (
                "oups il semblerait que tu te sois foutu de ma gueule :\n\n"
                + traceback.format_exc()
            )
        self.con.commit()
        return f"votre choix a bien été pris en compte {mentor}, ton poulain sera :{poulain}"

    def get_usr_lst(self, poulain):
        response = self.handler.get_user_info(poulain)
        if not response:
            return None
        res = {
            "poulain": poulain,
            "level": self.handler.user_get_level(response),
            "exam1": response.get,
        }

    @cursor_handler
    def list(self, cursor: sqlite3.Cursor):
        cursor.execute("SELECT intraID FROM poulains")
        res = str()
        for p in cursor.fetchall():
            poulain = self.handler.get_user_info(p)
        return res
