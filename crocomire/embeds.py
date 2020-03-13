from discord import Embed
from crocomire.mu_model import Matchup

embed_color = 10170673


def create_text_embed(cmd_data: dict):
    title: str = "__" + cmd_data["title"] + "__"
    fields: dict = cmd_data["fields"]
    embed: Embed = Embed(title=title, color=embed_color)
    embed.set_thumbnail(url=cmd_data["image"])

    for i in fields.keys():
        embed.add_field(name=i, value=fields[i], inline=False)

    return embed


def create_image_embed(img_url: str):
    embed: Embed = Embed(color=embed_color)
    embed.set_image(url=img_url)
    return embed


def create_mu_embed(mu: Matchup):
    title: str = "__" + mu.title + "__"
    desc: str = "[Click here for more matchup tips.]({})".format(mu.doclink)
    tips: str = ""

    for t in mu.criticaltips:
        tips += "• {}\n".format(t)

    embed: Embed = Embed(title=title, color=embed_color, description=desc)
    if mu.image != "MISSING":
        embed.set_thumbnail(url=mu.image)

    embed.add_field(name="Overview", value=mu.overview, inline=False)
    embed.add_field(name="Critical Tips", value=tips, inline=False)
    embed.add_field(name="Counter-Picks", value=mu.counterpicks, inline=True)
    embed.add_field(name="Bans", value=mu.bans, inline=True)
    return embed
