from sqlite3 import connect, Connection, Cursor
from typing import List
from crocomire.mu_model import Matchup


def connect_to_synonyms_db() -> Connection:
    return connect("databases/synonyms.db")


def connect_to_mu_db() -> Connection:
    return connect("databases/mu.db")


def select_char(char_name: str, db: Connection) -> str:
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


def select_mu_data(char_name: str, db: Connection) -> tuple:
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


def insert_mu_data(mu: Matchup, db: Connection):
    db.execute("""
            INSERT INTO
                matchups
            VALUES
                (?,?,?,?,?,?,?,?)
            """, (mu.name, mu.title, mu.overview, "\n".join(mu.criticaltips),
                  mu.counterpicks, mu.bans, mu.image, mu.doclink))
    db.commit()


def update_mu_data(mu: Matchup, db: Connection):
    db.execute("""
            UPDATE
                matchups
            SET
                title=?, overview=?, criticaltips=?,
                counterpicks=?, bans=?, image=?, doclink=?
            WHERE
                name=?
            """, (mu.title, mu.overview, "\n".join(mu.criticaltips),
                  mu.counterpicks, mu.bans, mu.image, mu.doclink, mu.name))
    db.commit()


def remove_mu_data(char_name: str, db: Connection):
    db.execute("""
            DELETE
            FROM
                matchups
            WHERE
                matchups.name = ?
            """, (char_name,))

    db.commit()
