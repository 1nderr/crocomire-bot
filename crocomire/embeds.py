from discord import Embed

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
