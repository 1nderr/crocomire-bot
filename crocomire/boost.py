from typing import List
from datetime import datetime, timedelta

from discord import Member
from discord.ext import commands


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
    for r in list(ranks.keys())[0:10]:
        ranks[r] = timedelta(seconds=ranks[r])

    return ranks
