from typing import List
from sqlite3 import Connection
from re import sub

from crocomire.mu_model import Matchup
from crocomire import database


def translate_char(char: str) -> str:
    """
    Get the given character's code name.

    :param char: `str`
    :return: `str`, "" if not found
    """
    char: str = sub(r"[^\w\d]|[_\-]", "", char)
    syn_db: Connection = database.connect_to_synonyms_db()
    char = database.select_char(char, syn_db)
    return char


def get_matchup(char_name: str) -> Matchup:
    """
    Get the Matchup data object.

    :param char_name: `str`
    :return: `Matchup`, `None` if not found
    """
    mu_db: Connection = database.connect_to_mu_db()
    mu_data: List = database.select_mu_data(char_name, mu_db)

    if len(mu_data) == 0:
        return None

    mu: Matchup = Matchup(char_name)
    mu.set_title(mu_data[0])
    mu.set_overview(mu_data[1])
    mu.set_criticaltips(mu_data[2].split("\n"))
    mu.set_counterpicks(mu_data[3])
    mu.set_bans(mu_data[4])
    mu.set_image(mu_data[5])
    mu.set_doclink(mu_data[6])

    return mu


def add_matchup(char_name: str, mu_sections: List) -> Matchup:
    """
    Add a matchup from the given message.

    :param msg: `str`
    :param mu_sections: `List`
    :return: `Matchup`, `None` if not found
    """
    # TODO: Check if URLs are valid
    mu: Matchup = Matchup(char_name)
    tips: List = []

    for m in mu_sections[1:]:
        section_name: str = m.split("=", 1)[0]
        section_text: str = m.split("=", 1)[1]

        if section_name == "TITLE":
            mu.set_title(section_text)
        elif section_name == "OVERVIEW":
            mu.set_overview(section_text)
        elif section_name == "TIP":
            tips.append(section_text)
        elif section_name == "COUNTERS":
            mu.set_counterpicks(section_text)
        elif section_name == "BANS":
            mu.set_bans(section_text)
        elif section_name == "IMAGE":
            mu.set_image(section_text)
        elif section_name == "DOC":
            mu.set_doclink(section_text)

    if len(tips) == 0:
        mu.set_criticaltips(["MISSING"])
    else:
        mu.set_criticaltips(tips)
    mu_db: Connection = database.connect_to_mu_db()
    database.insert_mu_data(mu, mu_db)
    return mu
