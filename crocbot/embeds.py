from discord import Embed

embed_color = 10170673


def create_text_embed(cmd_data):
    """
    Create an embed with text fields.

    :param cmd_data: `dict`
    :return: `Embed`
    """
    title = "__" + cmd_data["title"] + "__"
    fields = cmd_data["fields"]
    embed = Embed(title=title, color=embed_color)
    embed.set_thumbnail(url=cmd_data["image"])
    for i in fields.keys():
        embed.add_field(name=i, value=fields[i], inline=False)
    return embed
