from typing import List

from discord import Role
from discord.ext import commands


async def remove_all_roles(ctx: commands.Context):
    role: Role = None
    users: str = ""
    role_name: str = "".join(ctx.message.content.split()[1:]).lower()
    roles: List[Role] = await ctx.guild.fetch_roles()

    for r in roles:
        r_name: str = "".join(str(r).split()).lower()
        if r_name == role_name:
            role = r
            break

    if role is None:
        return role_name, users

    for m in role.members:
        await m.remove_roles(role)
        users += str(m) + ", "

    return str(role), users


async def get_alt_ranks(ctx: commands.Context):
    alts: dict = {"Default": 0, "Meta": 0, "Red": 0,
                  "Blue": 0, "Green": 0, "NES": 0,
                  "Golden": 0, "Robot": 0}

    roles: List[Role] = await ctx.guild.fetch_roles()

    for r in roles:
        if r.name in alts.keys():
            alts[r.name] = len(r.members)

    alts = {k: v for k, v in sorted(
        alts.items(), key=lambda item: item[1])}
    return build_alt_leaderboard(alts)


def build_alt_leaderboard(alts: dict):
    rank_msg: str = ""

    for i, a in enumerate(list(alts.keys())[::-1]):
        rank_msg += "{}. {:<8} {}\n".format(i + 1, a, alts[a])

    return "**Ridley's Alts Ranked by User Count**```{}```".format(rank_msg)
