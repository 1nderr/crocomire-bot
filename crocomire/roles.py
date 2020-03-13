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
