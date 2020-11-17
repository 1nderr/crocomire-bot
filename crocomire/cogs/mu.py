from typing import List
from sqlite3 import Connection

from discord.ext import commands
from discord import Embed

from crocomire.utils import embeds, mu_helper, mu_database
from crocomire.utils.embed_model import EmbedModel

croc_emote: str = "<:Crocomire:583880666970718224>"


class Matchup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mu")
    async def send_mu(self, ctx: commands.Context):
        msg: str = ctx.message.content
        if len(msg.split()) == 1:
            embed_model: EmbedModel = mu_helper.get_all_chars()
            embed: Embed = embeds.create_embed(embed_model)
            await ctx.send(embed=embed)
            return

        char: str = "".join(msg.split()[1:]).lower()
        char = mu_helper.translate_char(char)

        if len(char) == 0:
            await ctx.send("That character does not exist Bruh {}".format(croc_emote))
            return

        matchup: Matchup = mu_helper.get_matchup(char)
        if matchup is None:
            await ctx.send("That character has no data Bruh {}".format(croc_emote))
            return

        embed: Embed = embeds.create_mu_embed(matchup)
        await ctx.send(embed=embed)

    @commands.command(name="addmu")
    @commands.has_permissions(administrator=True)
    async def add_mu(self, ctx: commands.Context):
        msg: str = ctx.message.content
        if len(msg.split()) == 1:
            embed_model: EmbedModel = mu_helper.get_all_chars()
            embed: Embed = embeds.create_embed(embed_model)
            await ctx.send(embed=embed)
            return

        mu_sections: List = msg.split("\n")
        char: str = "".join(mu_sections[0].split()[1:]).lower()
        char = mu_helper.translate_char(char)
        if len(char) == 0:
            await ctx.send("That character does not exist Bruh {}".format(croc_emote))
            return

        mu_db: Connection = mu_database.connect_to_mu_db()
        if len(mu_database.select_mu_data(char, mu_db)) != 0:
            matchup = mu_helper.update_matchup(char, mu_sections)
        else:
            matchup = mu_helper.add_matchup(char, mu_sections)

        embed: Embed = embeds.create_mu_embed(matchup)
        await ctx.send(embed=embed)

    @commands.command(name="removemu")
    @commands.has_permissions(administrator=True)
    async def remove_mu(self, ctx: commands.Context):
        msg: str = ctx.message.content
        if len(msg.split()) == 1:
            embed_model: EmbedModel = mu_helper.get_all_chars()
            embed: Embed = embeds.create_embed(embed_model)
            await ctx.send(embed=embed)
            return

        char: str = "".join(msg.split()[1:]).lower()
        char = mu_helper.translate_char(char)

        if len(char) == 0:
            await ctx.send("That character does not exist Bruh {}".format(croc_emote))
            return

        mu_db: Connection = mu_database.connect_to_mu_db()
        if len(mu_database.select_mu_data(char, mu_db)) == 0:
            await ctx.send("That character has no data Bruh {}".format(croc_emote))
            return

        mu_database.remove_mu_data(char, mu_db)
        await ctx.send("I removed that character's mu data Bruh {}".format(croc_emote))

    @add_mu.error
    @remove_mu.error
    async def perm_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} you do not have permission to do that Bruh {}".format(ctx.author.mention, croc_emote))
