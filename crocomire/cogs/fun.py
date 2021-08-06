from os import path
from random import choice, randint, seed
from string import ascii_letters

from crocomire.utils import embeds, url
from crocomire.utils.embed_model import EmbedModel
from discord import Embed
from discord.ext import commands
from requests import get

# TODO: this is literally a text file, will need a table for this some day
meme_path: str = "databases/memes"
tubes_path: str = "databases/tubesmemes"
croc_emote: str = "<:Crocomire:583880666970718224>"


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
            await ctx.send("I added this new meme Bruh {}".format(croc_emote))
        else:
            await ctx.send("That is not a valid image url Bruh {}".format(croc_emote))

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
                await ctx.send("There are no memes Bruh {}".format(croc_emote))
                return
        model: EmbedModel = EmbedModel("meme")
        model.set_image(meme)
        embed: Embed = embeds.create_embed(model)
        await ctx.send(embed=embed)

    # Sends a random meme from the tubes memes file
    @commands.command(name="tubes")
    async def send_tubes(self, ctx: commands.Context):
        if not path.exists(tubes_path):
            open(tubes_path, "w+")
        with open(tubes_path, "r") as f:
            seed()
            try:
                meme: str = choice(f.readlines())
            except:
                await ctx.send("There are no tubes Bruh {}".format(croc_emote))
                return
        model: EmbedModel = EmbedModel("tubes")
        model.set_image(meme)
        embed: Embed = embeds.create_embed(model)
        await ctx.send(embed=embed)

    @commands.command(name="mash")
    async def send_mash(self, ctx: commands.Context):
        s = "".join([choice(list(ascii_letters))
                     for i in range(randint(30, 76))])
        await ctx.send(s)

    @commands.command(name="fact")
    async def send_fact(self, ctx: commands.Context):
        fact: dict = get(
            "https://uselessfacts.jsph.pl/random.json?language=en")
        await ctx.send(fact.json()["text"])

    @commands.command(name="power")
    async def send_power(self, ctx: commands.Context):
        await ctx.send("**%s power stats:**\nHP: %d\nATK: %d \nFUNNY: %d\n" % (ctx.author.name, randint(0, 100), randint(0, 100), 0))

    @add_meme.error
    async def perm_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} you do not have permission to do that Bruh {}".format(ctx.author.mention, croc_emote))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
