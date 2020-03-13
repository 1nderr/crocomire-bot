from random import choice, seed
from typing import List
from sqlite3 import Connection

from discord import Game, Embed
from discord.ext import commands
from yaml import safe_load

from secret import token
from crocomire import embeds, boost, roles, mu, mu_database, cmd_database
from crocomire.mu_model import Matchup
from crocomire.embed_model import TextEmbed

prefix: str = "?"
croc_emote: str = "<:Crocomire:583880666970718224>"
lul_emote: str = "<:RidLul:562495276141510667>"
dab_emote: str = "<:RidDab:562492164664197120>"
status_msg: str = "Bruh, Type ?info"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"
role_msg: str = "I removed the role **{}** from these users Bruh {}:\n```{}```"
admin_error: str = "{} you need the permission **Administrator** to use that command Bruh {}"
cmd_data: dict = safe_load(open("commands.yml"))
cmd_db: Connection = cmd_database.connect_to_cmd_db()

bot: commands.Bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    activity=Game(status_msg))


@bot.command(aliases=cmd_database.select_all_text_cmds(cmd_db))
async def send_text(ctx: commands.Context):
    cmd: str = ctx.message.content[1:]
    msg: str = cmd_database.select_text_cmd(cmd, cmd_db)
    await ctx.send(msg)


@bot.command(aliases=cmd_database.select_all_embed_cmds(cmd_db))
async def send_embed(ctx: commands.Context):
    cmd: str = ctx.message.content[1:]
    embedData: List = cmd_database.select_embed_cmd(cmd, cmd_db)
    textEmbed: TextEmbed = TextEmbed(cmd)
    textEmbed.set_title(embedData[0])
    textEmbed.set_description(embedData[1])
    textEmbed.set_footer(embedData[2])
    textEmbed.set_thumbnail(embedData[3])
    textEmbed.set_fields(embedData[5])

    if cmd == "meme":
        with open("memes", "r") as f:
            seed()
            meme = choice(f.readlines())
            textEmbed.set_image(meme)
    else:
        textEmbed.set_image(embedData[4])

    embed: Embed = embeds.create_embed(textEmbed)
    await ctx.send(embed=embed)


# @bot.command(name="info")
# async def send_help(ctx: commands.Context):
#     embed: Embed = embeds.create_text_embed(cmd_data["info"])
#     await ctx.author.send(embed=embed)
#     await ctx.send("{} Bruh, I sent you a DM {}".format(ctx.author.mention, croc_emote))


@bot.command(name="mu")
async def send_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send("Bruh, that's not right. You didn't give a character name {}".format(croc_emote))
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send("That character does not exist Bruh {}".format(croc_emote))
        return

    matchup: Matchup = mu.get_matchup(char)
    if matchup is None:
        await ctx.send("That character does not have data *yet* Bruh {}".format(croc_emote))
        return

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="addmu")
@commands.has_permissions(administrator=True)
async def add_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send("Bruh, that's not right. You didn't give a character name {}".format(croc_emote))
        return

    mu_sections: List = msg.split("\n")
    char: str = "".join(mu_sections[0].split()[1:]).lower()
    char = mu.translate_char(char)
    if len(char) == 0:
        await ctx.send("That character does not exist Bruh {}".format(croc_emote))
        return

    mu_db: Connection = mu_database.connect_to_mu_db()
    if len(mu_database.select_mu_data(char, mu_db)) != 0:
        matchup = mu.update_matchup(char, mu_sections)
    else:
        matchup = mu.add_matchup(char, mu_sections)

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="removemu")
@commands.has_permissions(administrator=True)
async def remove_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send("Bruh, that's not right. You didn't give a character name {}".format(croc_emote))
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send("That character does not exist Bruh {}".format(croc_emote))
        return

    mu_db: Connection = mu_database.connect_to_mu_db()
    if len(mu_database.select_mu_data(char, mu_db)) == 0:
        await ctx.send("That character does not have any mu data Bruh {}".format(croc_emote))
        return

    mu_database.remove_mu_data(char, mu_db)
    await ctx.send("I removed the MU write up for **{}** Bruh {}".format(char, croc_emote))


@bot.command(name="removerole")
@commands.has_permissions(administrator=True)
async def remove_role(ctx: commands.Context):
    if "jmu" not in "".join(ctx.message.content.split()[1:]).lower():
        await ctx.send("That is not a JMU role Bruh {}".format(croc_emote))
        return

    role_name, members = await roles.remove_all_roles(ctx)
    if len(members) == 0:
        await ctx.send("No one had the role **{}** Bruh {}".format(role_name, croc_emote))
        return

    await ctx.send(role_msg.format(role_name, croc_emote, members))


@bot.command(name="boosters")
async def send_leaderboard(ctx: commands.Context):
    boosters: dict = boost.get_boosters(ctx)
    if len(boosters) == 0:
        await ctx.send("No one boosted this server Bruh {}".format(croc_emote))
        return

    msg: str = boost.build_leaderboard(boosters)
    await ctx.send(top10_msg.format(msg))
    await boost.update_leaderboard(ctx)


@bot.command(name="boost")
async def send_funny_boost(ctx: commands.Context):
    if ctx.author in ctx.guild.premium_subscribers:
        await ctx.send("What's up booster Bruh {}. Imagine not being a booster {}".format(croc_emote, lul_emote))
    else:
        await ctx.message.add_reaction(dab_emote)
    await boost.update_leaderboard(ctx)


@remove_role.error
@add_mu.error
async def cmd_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(admin_error.format(ctx.author.mention, croc_emote))

bot.run(token)
