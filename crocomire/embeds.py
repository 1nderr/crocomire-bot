from typing import List
from sqlite3 import Connection
from random import choice, seed

from discord import Embed
from crocomire import cmd_database
from crocomire.mu_model import Matchup
from crocomire.embed_model import EmbedModel

embed_color = 10170673


def create_embed(embedModel: EmbedModel):
    embed: Embed = Embed(title=embedModel.title,
                         color=embed_color, description=embedModel.description)

    if embedModel.footer is not None:
        embed.set_footer(text=embedModel.footer)

    if embedModel.thumbnail is not None:
        embed.set_thumbnail(url=embedModel.thumbnail)

    if embedModel.image is not None:
        embed.set_image(url=embedModel.image)

    if embedModel.fields is not None:
        for i in embedModel.fields.keys():
            embed.add_field(name=i, value=embedModel.fields[i], inline=False)

    return embed


def create_mu_embed(mu: Matchup):
    desc: str = "[Click here for more matchup tips.]({})".format(mu.doclink)
    tips: str = ""

    for t in mu.criticaltips:
        tips += "• {}\n".format(t)

    embed: Embed = Embed(title=mu.title, color=embed_color, description=desc)
    if mu.image != "MISSING":
        embed.set_thumbnail(url=mu.image)

    embed.add_field(name="Overview", value=mu.overview, inline=False)
    embed.add_field(name="Critical Tips", value=tips, inline=False)
    embed.add_field(name="Counter-Picks", value=mu.counterpicks, inline=True)
    embed.add_field(name="Bans", value=mu.bans, inline=True)
    return embed


def get_embed_model(cmd: str):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    embedData: List = cmd_database.select_embed_cmd(cmd, cmd_db)
    embedModel: EmbedModel = EmbedModel(cmd)
    embedModel.set_title(embedData[0])
    embedModel.set_description(embedData[1])
    embedModel.set_footer(embedData[2])
    embedModel.set_thumbnail(embedData[3])
    embedModel.set_fields(embedData[5])

    if cmd == "meme":
        with open("databases/memes", "r") as f:
            seed()
            meme = choice(f.readlines())
            embedModel.set_image(meme)

    return embedModel
