from random import choice, seed
from discord import Embed

embed_color = 10170673


def create_meme_embed():
    """
    Create an image embed with a random meme.

    :return: `Embed`
    """
    seed()
    embed = Embed(color=embed_color)
    with open("memes", "r") as f:
        embed.set_image(url=choice(f.readlines()))
    return embed
