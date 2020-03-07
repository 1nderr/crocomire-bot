from typing import List
from sqlite3 import Connection

from crocomire.mu_model import Matchup
from crocomire import database


def get_matchup(char_name: str) -> Matchup:
    """
    Get the Matchup data object.

    :param char_name: `str`
    :return: Matchup, None if not found
    """
    mu_db: Connection = database.connect_to_mu_db()
    mu_data: List = database.select_mu_data(char_name, mu_db)

    if len(mu_data) == 0:
        print(len(mu_data))
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
