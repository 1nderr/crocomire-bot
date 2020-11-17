from typing import List
from discord.ext import commands
from discord import Role, Message
from crocomire.utils import reactions

croc_emote: str = "<:Crocomire:583880666970718224>"


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="removerole")
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx: commands.Context):
        if "jmu" not in "".join(ctx.message.content.split()[1:]).lower():
            await ctx.send("That is not the JMU role Bruh {}".format(croc_emote))
            return

        role: Role = None
        role_name: str = "".join(ctx.message.content.split()[1:]).lower()
        roles: List[Role] = await ctx.guild.fetch_roles()

        for r in roles:
            r_name: str = "".join(str(r).split()).lower()
            if r_name == role_name:
                role = r
                break

        if role is None:
            await ctx.send("That role does not exist Bruh {}".format(croc_emote))
            return

        resp: Message = await ctx.send(
            "Are you sure you want to remove the **{}** role from every user Bruh {}".format(str(role), croc_emote))
        confirm: bool = await reactions.confirm(ctx, resp)

        if confirm:
            for m in role.members:
                await m.remove_roles(role)
            await ctx.send("I removed the **{}** role Bruh {}".format(str(role), croc_emote))
        else:
            await ctx.send("The removal was cancelled Bruh {}".format(croc_emote))

    @commands.command(name="alts")
    async def rank_alts(self, ctx: commands.Context):
        ranks: str = await self.get_alt_ranks(ctx)
        await ctx.send(ranks)

    async def get_alt_ranks(self, ctx: commands.Context):
        alts: dict = {"Default": 0, "Meta": 0, "Red": 0,
                      "Blue": 0, "Green": 0, "NES": 0,
                      "Golden": 0, "Robot": 0}

        roles: List[Role] = await ctx.guild.fetch_roles()

        for r in roles:
            if r.name in alts.keys():
                alts[r.name] = len(r.members)

        alts = {k: v for k, v in sorted(
            alts.items(), key=lambda item: item[1])}
        return self.build_alt_leaderboard(alts)

    def build_alt_leaderboard(self, alts: dict):
        rank_msg: str = ""

        for i, a in enumerate(list(alts.keys())[::-1]):
            rank_msg += "{}. {:<8} {}\n".format(i + 1, a, alts[a])

        return "**Ridley's Alts Ranked by User Count**```{}```".format(rank_msg)
