from discord import Embed
from yaml import safe_load

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
    mu_data: dict = safe_load(open("mus.yml"))[char]
    title: str = "__" + mu_data["title"] + "__"
    desc: str = "[Click here for more matchup tips.]({})".format(
        mu_data["link"])
    tips: str = ""

    for t in mu_data["criticaltips"]:
        tips += "• {}\n".format(t)

    embed: Embed = Embed(title=title, color=embed_color, description=desc)
    embed.set_thumbnail(url=mu_data["image"])
    embed.add_field(name="Overview", value=mu_data["overview"], inline=False)
    embed.add_field(name="Critical Tips",
                    value=tips, inline=False)
    embed.add_field(name="Counter-Picks",
                    value=mu_data["counterpicks"], inline=True)
    embed.add_field(name="Bans", value=mu_data["bans"], inline=True)
    return embed
