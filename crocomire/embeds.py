from discord import Embed
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
