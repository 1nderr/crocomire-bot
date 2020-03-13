from discord import Embed
from crocomire.mu_model import Matchup
from crocomire.embed_model import EmbedModel

embed_color = 10170673


def create_embed(embedModel: EmbedModel):
    title = ""
    embed: Embed = Embed()

    if embedModel.title is not None:
        title = "__" + embedModel.title + "__"

    if embedModel.description is not None:
        embed = Embed(title=title, color=embed_color,
                      description=embedModel.description)
    else:
        embed: Embed = Embed(title=title, color=embed_color)

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
