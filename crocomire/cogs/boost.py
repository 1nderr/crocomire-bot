from discord.ext import commands, tasks
from discord import Member, TextChannel, Guild, Message
from typing import List
from datetime import datetime, timedelta

booster_chan_id: int = 675826799317483538
board_id: int = 696531092957823020
dab_emote: str = "<:RidDab:562492164664197120>"
croc_emote: str = "<:Crocomire:583880666970718224>"
lul_emote: str = "<:RidLul:562495276141510667>"


class Boost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_board.start()

    # Goes through all the boosters of the server and returns the
    # top ten longest boosters
    @commands.command(name="boosters")
    async def boostboard(self, ctx: commands.Context):
        boosters: dict = self.get_boosters(ctx.guild)
        if len(boosters) == 0:
            await ctx.send("This server has no boosts Bruh {}.".format(croc_emote))
            return

        msg: str = self.build_leaderboard(boosters)
        await ctx.send(msg)

    # Special message for boosters only
    @commands.command(name="boost")
    async def boost_msg(self, ctx: commands.Context):
        if ctx.author in ctx.guild.premium_subscribers:
            await ctx.send("What's up booster Bruh {}. Imagine not being a booster {}".format(croc_emote, lul_emote))
        else:
            await ctx.message.add_reaction(dab_emote)

    @tasks.loop(hours=1)
    async def update_board(self):
        guild: Guild = self.bot.get_guild(456142548667465728)
        boosters: dict = self.get_boosters(guild)
        booster_chan: TextChannel = guild.get_channel(booster_chan_id)
        oldBoard: Message = await booster_chan.fetch_message(board_id)
        newBoard: str = self.build_leaderboard(boosters)
        await oldBoard.edit(content=newBoard)

    @update_board.before_loop
    async def before_update_board(self):
        await self.bot.wait_until_ready()

    # Returns a dictionary of users ordered by boost time
    def get_boosters(self, guild: Guild) -> dict:
        today: datetime = datetime.today()
        boosters: List[Member] = guild.premium_subscribers
        ranks: dict = {}

        for b in boosters:
            ranks[str(b)] = (today - b.premium_since).total_seconds()

        ranks = {k: v for k, v in sorted(
            ranks.items(), key=lambda item: item[1])}
        for r in list(ranks.keys())[:len(ranks.keys()) - 11:-1]:
            ranks[r] = timedelta(seconds=ranks[r])

        return ranks

    # Returns a string that looks like a leaderboard
    def build_leaderboard(self, boosters: dict) -> str:
        c: int = 1
        s: str = ""

        for b in list(boosters.keys())[:len(boosters.keys()) - 11:-1]:
            s += "{:}. {: <32} {}\n".format(c, b[0:len(b) - 5], boosters[b])
            c += 1

        return "**Top 10 Ridleycord Boosters**```{}```".format(s)
