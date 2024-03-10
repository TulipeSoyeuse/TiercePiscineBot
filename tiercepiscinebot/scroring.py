import sqlite3

import pandas as pd
from tiercepiscinebot.api import API_handler
from tiercepiscinebot.db_interaction import Database
from tiercepiscinebot.params import *


class Database(Database):
    def __init__(self) -> None:
        super().__init__()

    def update_scoring(self):
        cursor = self.con.cursor()
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
        cursor.close()


if __name__ == "__main__":
    import json

    with open("test.json", "r") as f:
        res = json.load(f)
    # print(API_handler.user_get_exercice(res, 1270))
    db = Database()
    db.update_scoring()
    print(pd.read_sql_query("SELECT * FROM exercice", db.con).to_markdown())
    # update_scoring()
