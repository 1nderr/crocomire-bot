from sqlite3 import connect, Connection, Cursor
from typing import List


def connect_to_cmd_db() -> Connection:
    return connect("databases/commands.db")


def select_all_text_cmds(db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM text_commands")
    rows: List = c.fetchall()

    if len(rows) == 0:
        return []

    return [row[0] for row in rows]


def select_all_image_cmds(db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM image_commands")
    rows: List = c.fetchall()

    if len(rows) == 0:
        return []

    return [row[0] for row in rows]


def select_text_cmd(cmd: str, db: Connection) -> str:
    c: Cursor = db.cursor()
    c = db.execute("SELECT text FROM text_commands WHERE name=?", (cmd,))
    rows: List = c.fetchall()

    if len(rows) == 0:
        return ""

    return rows[0][0]


def select_image_cmd(cmd: str, db: Connection) -> str:
    c: Cursor = db.cursor()
    c = db.execute("SELECT image FROM image_commands WHERE name=?", (cmd,))
    rows: List = c.fetchall()

    if len(rows) == 0:
        return ""

    return rows[0][0]
