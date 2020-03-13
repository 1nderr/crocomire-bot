from sqlite3 import connect, Connection, Cursor
from typing import List


def connect_to_cmd_db() -> Connection:
    return connect("databases/commands.db")


def select_all_text_cmds(db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM text_commands")
    rows: List = c.fetchall()
    return [row[0] for row in rows]


def select_text_cmd(cmd: str, db: Connection) -> str:
    c: Cursor = db.cursor()
    c = db.execute("SELECT text FROM text_commands WHERE name=?", (cmd,))
    rows: List = c.fetchall()
    return rows[0][0]


def select_all_embed_cmds(db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM embed_commands")
    rows: List = c.fetchall()
    return [row[0] for row in rows]


def select_embed_cmd(cmd: str, db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT * FROM embed_commands WHERE name=?", (cmd,))
    rows: List = c.fetchall()
    fields: dict = select_embed_fields(rows[0][0], db)
    embedData: List = list(rows[0][2:])
    embedData.append(fields)
    return embedData


def select_embed_fields(cmd_id: int, db: Connection) -> dict:
    c: Cursor = db.cursor()
    c = db.execute(
        "SELECT name, value FROM embed_fields WHERE embed_id=?", (cmd_id,))

    rows: List = c.fetchall()
    fields: dict = {}
    for row in rows:
        fields[row[0]] = row[1]

    return fields
