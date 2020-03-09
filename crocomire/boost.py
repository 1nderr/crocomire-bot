from typing import List
from datetime import datetime, timedelta

from discord import Member, TextChannel, Message
from discord.ext import commands

booster_chan_id: int = 675826799317483538
board_id: int = 675834739516637244
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"


async def update_leaderboard(ctx: commands.Context):
    """
    Async function that updates the booster leaderboard in the booster rewards channel.

    :param ctx: `commands.Context`
    :return: `None`
    """
    boosters: dict = get_boosters(ctx)
    booster_chan: TextChannel = ctx.guild.get_channel(booster_chan_id)
    oldBoard: Message = await booster_chan.fetch_message(board_id)
    newBoard: str = build_leaderboard(boosters)
    await oldBoard.edit(content=top10_msg.format(newBoard))


def get_boosters(ctx: commands.Context):
    """
    Get the boosters sorted by time since they boosted.

    :param ctx: `commands.Context`
    :return: `dict`
    """
    today: datetime = datetime.today()
    boosters: List[Member] = ctx.guild.premium_subscribers
    ranks: dict = {}

    for b in boosters:
        ranks[str(b)] = (today - b.premium_since).total_seconds()

    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1])}
    for r in list(ranks.keys())[:len(ranks.keys()) - 11:-1]:
        ranks[r] = timedelta(seconds=ranks[r])

    return ranks


def build_leaderboard(boosters: dict):
    """
    Build the leaderboard message.

    :param boosters: `dict`
    :return: `str`
    """
    c: int = 1
    s: str = ""

    for b in list(boosters.keys())[:len(boosters.keys()) - 11:-1]:
        s += "{:}. {: <28} {}\n".format(c, b[0:len(b) - 5], boosters[b])
        c += 1

    return s
