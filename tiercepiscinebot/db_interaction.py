import sqlite3
import traceback
from sqlite3 import IntegrityError

import pandas as pd
from tiercepiscinebot.api import API_handler
from tiercepiscinebot.params import *


class Database:
    def __init__(self) -> None:
        self.con = sqlite3.connect("poulain.db", detect_types=sqlite3.PARSE_DECLTYPES)
        self.handler = API_handler()
        cursor = self.con.cursor()
        cursor.execute(CREATE_TABLE_POULAIN)
        cursor.execute(CREATE_TABLE_EXERCICE)
        self.con.commit()
        cursor.close()

    def cursor_handler(func):
        def wrapper(*args):
            cursor = args[0].con.cursor()
            res = func(*args, cursor)
            cursor.close()
            return res

        return wrapper

    @cursor_handler
    def add_poulain(self, poulain: str, mentor: str, cursor: sqlite3.Cursor) -> str:
        poulain_ = self.handler.get_user_info(poulain)
        if not poulain_:
            return "stp passe moi un login correct par pitié (le poulain existe po)"
        mentor_ = self.handler.get_user_info(mentor)
        if not mentor_:
            return "stp passe moi un login correct par pitié (le mentor existe po)"
        try:
            cursor.execute(
                "INSERT INTO poulains(intraID, mentorID) VALUES(?, ?)",
                (poulain, mentor),
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
            return "Error"
        return LIST_STRING.format(
            poulain=poulain,
            level=API_handler.user_get_level(response),
            exam1=API_handler.user_get_exam(response, 0),
            exam2=API_handler.user_get_exam(response, 1),
            exam3=API_handler.user_get_exam(response, 2),
            exam4=API_handler.user_get_exam(response, 3),
        )

    @cursor_handler
    def list(self, cursor: sqlite3.Cursor):
        cursor.execute("SELECT intraID FROM poulains")
        res = str()
        for p in cursor.fetchall():
            res += self.get_usr_lst(p[0])
        return res

    @cursor_handler
    def update_scoring(self, cursor: sqlite3.Cursor):
        cursor.execute("DROP TABLE exercice")
        cursor.execute(CREATE_TABLE_EXERCICE)
        cursor.execute("SELECT id, IntraID FROM poulains")
        for poulain in cursor.fetchall():
            info = self.handler.get_user_info(poulain[1])
            for exercice in EXERCICE_IDS:
                exercice_res = API_handler.user_get_exercice(info, exercice[0])
                if exercice_res:
                    cursor.execute(
                        """REPLACE INTO exercice (
                        exercice_name, exercice_id, poulain_id, timestamp, final_grade )
                        VALUES (?, ?, ?, ?, ?)""",
                        (
                            exercice[1],
                            exercice[0],
                            poulain[0],
                            exercice_res[0],
                            exercice_res[1],
                        ),
                    )
        self.con.commit()


if __name__ == "__main__":
    import json

    with open("test.json", "r") as f:
        res = json.load(f)
    # print(API_handler.user_get_exercice(res, 1270))
    db = Database()
    db.update_scoring()
    print(pd.read_sql_query("SELECT * FROM exercice", db.con).to_markdown())
    # update_scoring()
