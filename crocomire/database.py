from sqlite3 import connect, Connection, Cursor
from typing import List


def connect_to_mu_db() -> Connection:
    """
    Connect to the synonyms database.

    :return: `Connection` connection to db
    """
    conn: Connection = connect("databases/mu.db")
    return conn


def select_mu_data(char_name: str, db: Connection) -> tuple:
    """
    Get the character's mu data.

    :param char_name: `str` name of the character
    :param db: `Connection` connection to the mu db
    :return: `List[str]` [] if not found.
    """
    c: Cursor = db.cursor()
    c = db.execute("""
            SELECT
                *
            FROM
                matchups
            WHERE
                matchups.name = ?
            """, (char_name,))

    rows: List = c.fetchall()

    if len(rows) == 0:
        return []

    return rows[0][1:12]
