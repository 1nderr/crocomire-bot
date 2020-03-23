from typing import List
from datetime import datetime, timedelta

from discord import TextChannel, Message, Guild

booster_chan_id: int = 675826799317483538
board_id: int = 675834739516637244
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"


async def update_leaderboard(guild: Guild):
    boosters: dict = get_boosters(guild.premium_subscribers)
    booster_chan: TextChannel = guild.get_channel(booster_chan_id)
    oldBoard: Message = await booster_chan.fetch_message(board_id)
    newBoard: str = build_leaderboard(boosters)
    await oldBoard.edit(content=top10_msg.format(newBoard))


def get_boosters(boosters: List):
    today: datetime = datetime.today()
    ranks: dict = {}

    for b in boosters:
        ranks[str(b)] = (today - b.premium_since).total_seconds()

    ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1])}
    for r in list(ranks.keys())[:len(ranks.keys()) - 11:-1]:
        ranks[r] = timedelta(seconds=ranks[r])

    return ranks


def build_leaderboard(boosters: dict):
    c: int = 1
    s: str = ""

    for b in list(boosters.keys())[:len(boosters.keys()) - 11:-1]:
        s += "{:}. {: <28} {}\n".format(c, b[0:len(b) - 5], boosters[b])
        c += 1

    return s
