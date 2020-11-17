from typing import List
from sqlite3 import Connection
from re import sub, search, Match

from crocomire.utils.mu_model import Matchup
from crocomire.utils.embed_model import EmbedModel
from crocomire import mu_database, url


def get_all_chars() -> EmbedModel:
    embedModel: EmbedModel = EmbedModel("chars")
    mu_db: Connection = mu_database.connect_to_mu_db()
    chars: List = sorted(mu_database.select_all_chars(mu_db))

    for i, c in enumerate(chars):
        chars[i] = "`{}`".format(c)

    embedModel.set_title("Available Character Matchups:")
    embedModel.set_description(", ".join(chars))

    return embedModel


def translate_char(char: str) -> str:
    char: str = sub(r"[^\w\d]|[_\-]", "", char)
    syn_db: Connection = mu_database.connect_to_synonyms_db()
    char = mu_database.select_char(char, syn_db)
    return char


def get_matchup(char_name: str) -> Matchup:
    mu_db: Connection = mu_database.connect_to_mu_db()
    mu_data: tuple = mu_database.select_mu_data(char_name, mu_db)

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
    mu: Matchup = Matchup(char_name)
    mu = parse_mu_msg(mu, mu_sections)
    mu_db: Connection = mu_database.connect_to_mu_db()
    mu_database.insert_mu_data(mu, mu_db)
    return mu


def update_matchup(char_name: str, mu_sections: List) -> Matchup:
    mu: Matchup = get_matchup(char_name)
    mu = parse_mu_msg(mu, mu_sections)
    mu_db: Connection = mu_database.connect_to_mu_db()
    mu_database.update_mu_data(mu, mu_db)
    return mu


def parse_mu_msg(mu: Matchup, mu_sections: List):
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
        elif section_name == "IMAGE" and url.is_image(section_text):
            mu.set_image(section_text)
        elif section_name == "DOC" and url.exists(section_text):
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
