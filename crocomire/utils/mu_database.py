from sqlite3 import connect, Connection, Cursor
from typing import List
from os import path
from crocomire.utils.mu_model import Matchup

synonym_db_path: str = "databases/synonyms.db"
mu_db_path: str = "databases/mu.db"


def init_synonym_db() -> Connection:
    db: Connection = connect(synonym_db_path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS moves(
        id int not NULL,
        name char(256) NOT NULL,
        PRIMARY KEY(id))""")
    db.execute("""
        CREATE TABLE IF NOT EXISTS move_synonyms(move_id int not NULL, synonym char(256) NOT NULL)""")
    db.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id int not NULL,
            name char(256) NOT NULL,
            PRIMARY KEY (id));""")
    db.execute("""
        CREATE TABLE IF NOT EXISTS char_synonyms (char_id int not NULL, synonym char(256) NOT NULL);""")
    return db


def init_mu_db() -> Connection:
    db: Connection = connect(mu_db_path)
    db.execute("""
        CREATE TABLE IF NOT EXISTS "matchups" (
        "name"  TEXT,
        "title" TEXT,
        "overview"      TEXT,
        "criticaltips"  TEXT,
        "counterpicks"  TEXT,
        "bans"  TEXT,
        "image" TEXT,
        "doclink"       TEXT
    );""")
    return db


def connect_to_synonyms_db() -> Connection:
    if not path.exists(synonym_db_path):
        open(synonym_db_path, "w+").close()
    return init_synonym_db()


def connect_to_mu_db() -> Connection:
    if not path.exists(mu_db_path):
        open(mu_db_path, "w+").close()
    return init_mu_db()


def select_all_chars(db: Connection) -> List:
    c: Cursor = db.cursor()
    c = db.execute("SELECT name FROM matchups")
    rows: List = c.fetchall()
    return [row[0] for row in rows]


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
