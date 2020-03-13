from discord import Embed
from crocomire.mu_model import Matchup
from crocomire.embed_model import TextEmbed

embed_color = 10170673


def create_embed(textEmbed: TextEmbed):
    title = ""
    embed: Embed = Embed()

    if textEmbed.title is not None:
        title = "__" + textEmbed.title + "__"

    if textEmbed.description is not None:
        embed = Embed(title=title, color=embed_color,
                      description=textEmbed.description)
    else:
        embed: Embed = Embed(title=title, color=embed_color)

    if textEmbed.footer is not None:
        embed.set_footer(text=textEmbed.footer)

    if textEmbed.thumbnail is not None:
        embed.set_thumbnail(url=textEmbed.thumbnail)

    if textEmbed.image is not None:
        embed.set_image(url=textEmbed.image)

    if textEmbed.fields is not None:
        for i in textEmbed.fields.keys():
            embed.add_field(name=i, value=textEmbed.fields[i], inline=False)

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
