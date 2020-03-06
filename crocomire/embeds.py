from sqlite3 import Connection
from typing import List

from discord import Embed

from crocomire import database

embed_color = 10170673


def create_text_embed(cmd_data: dict):
    """
    Create an embed with text fields.

    :param cmd_data: `dict`
    :return: `Embed`
    """
    title: str = "__" + cmd_data["title"] + "__"
    fields: dict = cmd_data["fields"]
    embed: Embed = Embed(title=title, color=embed_color)
    embed.set_thumbnail(url=cmd_data["image"])
    for i in fields.keys():
        embed.add_field(name=i, value=fields[i], inline=False)
    return embed


def create_image_embed(img_url: str):
    """
    Create an embed with an image.

    :param cmd_data: `dict`
    :return: `Embed`
    """
    embed: Embed = Embed(color=embed_color)
    embed.set_image(url=img_url)
    return embed


def create_mu_embed(char: str):
    """
    Create an embed for MU data.

    :param char: `str`
    :return: `Embed`
    """
    mu_db: Connection = database.connect_to_mu_db()
    mu_data: List = database.select_mu_data(char, mu_db)

    if len(mu_data) == 0:
        return None

    title: str = "__" + mu_data[0] + "__"
    desc: str = "[Click here for more matchup tips.]({})".format(
        mu_data[6])
    tips: str = ""

    for t in mu_data[2].split("\n"):
        tips += "• {}\n".format(t)

    embed: Embed = Embed(title=title, color=embed_color, description=desc)
    embed.set_thumbnail(url=mu_data[5])
    embed.add_field(name="Overview", value=mu_data[1], inline=False)
    embed.add_field(name="Critical Tips",
                    value=tips, inline=False)
    embed.add_field(name="Counter-Picks",
                    value=mu_data[3], inline=True)
    embed.add_field(name="Bans", value=mu_data[4], inline=True)
    return embed
