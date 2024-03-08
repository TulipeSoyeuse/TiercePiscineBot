import sqlite3

from tiercepiscinebot.api import API_handler


class Database:
    def __init__(self) -> None:
        self.poulain = False
        self.con = sqlite3.connect("mydatabase.db")
        self.cur = self.con.cursor()
        self.handler = API_handler()

    def add_poulain(self, poulain: str, mentor: str) -> str:
        if not self.poulain:
            self.cur.execute(
                """CREATE TABLE [IF NOT EXISTS] 
                             poulain(intraID, mentorID)"""
            )
            self.poulain = True

        poulain_ = self.handler.get_user_info(poulain)
        if not poulain_:
            return "stp passe moi un login correct par pitié (le poulain existe po)"
        mentor_ = self.handler.get_user_info(mentor)
        if not mentor_:
            return "stp passe moi un login correct par pitié (le mentor existe po)"

        self.cur.execute(f"INSERT INTO poulain VALUES({poulain}, {mentor})")
        return f"votre choix a bien été pris en compte {mentor}"
        return f"votre choix a bien été pris en compte {mentor}"
