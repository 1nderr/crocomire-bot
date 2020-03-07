from sqlite3 import connect, Connection, Cursor
from typing import List
from crocomire.mu_model import Matchup


def connect_to_synonyms_db() -> Connection:
    """
    Connect to the synonyms database.

    :return: `Connection` connection to db
    """
    conn: Connection = connect("databases/synonyms.db")
    return conn


def connect_to_mu_db() -> Connection:
    """
    Connect to the synonyms database.

    :return: `Connection` connection to db
    """
    conn: Connection = connect("databases/mu.db")
    return conn


def select_char(char_name: str, db: Connection) -> str:
    """
    Get the code name of the given character name.

    :param move_name: `str` name of the character
    :param db: `Connection` connection to the synonyms db
    :return: `str` "" if not found
    """
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM characters where name=?", (char_name,))
    rows: List = c.fetchall()

    if len(rows) != 0:
        return rows[0][0]

    c = db.execute("""
        SELECT
            characters.name
        FROM
            characters, char_synonyms
        WHERE
            char_synonyms.synonym = ?
        AND
            char_synonyms.char_id = characters.id
    """, (char_name,))
    rows = c.fetchall()

    if len(rows) == 0:
        return ""

    return rows[0][0]


def select_mu_data(char_name: str, db: Connection) -> Matchup:
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

    return rows[0][1:9]
