from typing import List
from sqlite3 import Connection
from re import sub, search, Match

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
    :return: `Matchup`
    """
    # TODO: Check if URLs are valid
    mu: Matchup = Matchup(char_name)
    mu = parse_mu_msg(mu, mu_sections)
    mu_db: Connection = database.connect_to_mu_db()
    database.insert_mu_data(mu, mu_db)
    return mu


def update_matchup(char_name: str, mu_sections: List) -> Matchup:
    """
    Add a matchup from the given message.

    :param msg: `str`
    :param mu_sections: `List`
    :return: `Matchup`
    """
    # TODO: Check if URLs are valid
    mu: Matchup = get_matchup(char_name)
    mu = parse_mu_msg(mu, mu_sections)
    mu_db: Connection = database.connect_to_mu_db()
    database.update_mu_data(mu, mu_db)
    return mu


def parse_mu_msg(mu: Matchup, mu_sections: List):
    """
    Parse the give mu sections and sets them in the given Matchup.

    :param mu: `Matchup`
    :param mu_sections: `List`
    :return: `Matchup`
    """
    del_count: int = 0
    for m in mu_sections[1:]:
        section_name: str = m.split("=", 1)[0]
        section_text: str = m.split("=", 1)[1]

        if section_name == "TITLE":
            mu.set_title(section_text)
        elif section_name == "OVERVIEW":
            mu.set_overview(section_text)
        elif section_name == "COUNTERS":
            mu.set_counterpicks(section_text)
        elif section_name == "BANS":
            mu.set_bans(section_text)
        elif section_name == "IMAGE":
            mu.set_image(section_text)
        elif section_name == "DOC":
            mu.set_doclink(section_text)
        elif section_name[0:3] == "TIP":
            n_match: Match = search(r'\d+$', section_name)
            if n_match is not None:
                n: int = int(section_name[n_match.start():n_match.end()]) - 1
                if section_text != "DELETE":
                    if n + 1 > len(mu.criticaltips):
                        mu.add_criticaltip(section_text)
                    elif n >= 0:
                        mu.replace_criticaltip(section_text, n)
                else:
                    if n in range(len(mu.criticaltips) + 1):
                        mu.remove_criticaltip(n - del_count)
                        del_count += 1
            elif section_text != "DELETE":
                mu.add_criticaltip(section_text)

    if len(mu.criticaltips) == 0:
        mu.set_criticaltips(["MISSING"])

    return mu
