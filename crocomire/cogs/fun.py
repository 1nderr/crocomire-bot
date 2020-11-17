from random import randint, seed, choice
from string import ascii_letters
from os import path

from discord import Embed
from discord.ext import commands

from crocomire.utils import embeds, url
from crocomire.utils.embed_model import EmbedModel

# TODO: this is literally a text file, will need a table for this some day
meme_path: str = "databases/memes"
tubes_path: str = "databases/tubes"
add_meme_msg: str = "I added this new meme"


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Adds the meme from the given link and sends it back
    @commands.command(name="addmeme")
    @commands.has_permissions(administrator=True)
    async def add_meme(self, ctx: commands.Context, meme_link: str):
        if url.is_image(meme_link):
            with open(meme_path, "a") as f:
                f.write("\n" + meme_link)
            embed_model: EmbedModel = EmbedModel("NewMeme")
            embed_model.set_image(meme_link)
            embed: Embed = embeds.create_embed(embed_model)
            await ctx.send(embed=embed)
            await ctx.send(add_meme_msg)
        else:
            await ctx.send("That is not a valid image url.")

    # Sends a random meme from the memes file
    @commands.command(name="meme")
    async def send_meme(self, ctx: commands.Context):
        if not path.exists(meme_path):
            open(meme_path, "w+")
        with open(meme_path, "r") as f:
            seed()
            try:
                meme: str = choice(f.readlines())
            except:
                await ctx.send("There are no memes")
                return
        model: EmbedModel = EmbedModel("meme")
        model.set_image(meme)
        embed: Embed = embeds.create_embed(model)
        await ctx.send(embed=embed)

    # Sends a random meme from the tubes memes file
    @commands.command(name="tubes")
    async def send_meme(self, ctx: commands.Context):
        if not path.exists(tubes_path):
            open(tubes_path, "w+")
        with open(tubes_path, "r") as f:
            seed()
            try:
                meme: str = choice(f.readlines())
            except:
                await ctx.send("There are no tubes")
                return
        model: EmbedModel = EmbedModel("tubes")
        model.set_image(meme)
        embed: Embed = embeds.create_embed(model)
        await ctx.send(embed=embed)

    @commands.command(name="mash")
    async def send_mash(ctx: commands.Context):
        await ctx.send("".join([choice(list(ascii_letters)) for i in range(randint(30, 76))]))

    @add_meme.error
    async def perm_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} you do not have permission to do that!".format(ctx.author.mention))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
