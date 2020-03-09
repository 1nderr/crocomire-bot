from random import choice, seed
from typing import List
from sqlite3 import Connection

from discord import Game, Embed
from discord.ext import commands
from yaml import safe_load

from secret import token
from crocomire import embeds, boost, roles, mu, database
from crocomire.mu_model import Matchup

prefix: str = "?"
croc_emote: str = "<:Crocomire:583880666970718224>"
lul_emote: str = "<:RidLul:562495276141510667>"
dab_emote: str = "<:RidDab:562492164664197120>"
status_msg: str = "Bruh, Type ?info"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"
role_msg: str = "I removed the role **{}** from these users Bruh {}:\n```{}```"
admin_error: str = "{} you need the permission **Administrator** to use that command Bruh {}"
cmd_data: dict = safe_load(open("commands.yml"))
embed_cmds: List = list(cmd_data["embed"].keys())
text_cmds: List = list(cmd_data["text"].keys())
image_cmds: List = list(cmd_data["image"].keys())
custom_cmds: List = embed_cmds + text_cmds + image_cmds

bot: commands.Bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    activity=Game(status_msg))


@bot.command(name="info")
async def send_help(ctx: commands.Context):
    """
    Async function that dms the help text.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed: Embed = embeds.create_text_embed(cmd_data["info"])
    await ctx.author.send(embed=embed)
    await ctx.send("{} Bruh, I sent you a DM {}".format(ctx.author.mention, croc_emote))


@bot.command(aliases=custom_cmds)
async def send_custom_cmd(ctx: commands.Context):
    """
    Async function that sends a custom command from commands.yml.

    :param ctx: `commands.Context`
    :return: `None`
    """
    cmd: str = ctx.message.content[1:]
    if cmd in text_cmds:
        await ctx.send(cmd_data["text"][cmd])
    elif cmd in embed_cmds:
        embed: Embed = embeds.create_text_embed(cmd_data["embed"][cmd])
        await ctx.send(embed=embed)
    elif cmd in image_cmds:
        embed: Embed = embeds.create_image_embed(cmd_data["image"][cmd])
        await ctx.send(embed=embed)


@bot.command(name="mu")
async def send_mu(ctx: commands.Context):
    """
    Async function that sends the MU summary for the given character.

    :param ctx: `commands.Context`
    :return: `None`
    """
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
    """
    Async function that adds the MU summary for the given character.

    :param ctx: `commands.Context`
    :return: `None`
    """
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

    mu_db: Connection = database.connect_to_mu_db()
    if len(database.select_mu_data(char, mu_db)) != 0:
        matchup = mu.update_matchup(char, mu_sections)
    else:
        matchup = mu.add_matchup(char, mu_sections)

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="removemu")
@commands.has_permissions(administrator=True)
async def remove_mu(ctx: commands.Context):
    """
    Async function that removes the MU summary for the given character.

    :param ctx: `commands.Context`
    :return: `None`
    """
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send("Bruh, that's not right. You didn't give a character name {}".format(croc_emote))
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send("That character does not exist Bruh {}".format(croc_emote))
        return

    mu_db: Connection = database.connect_to_mu_db()
    if len(database.select_mu_data(char, mu_db)) == 0:
        await ctx.send("That character does not have any mu data Bruh {}".format(croc_emote))
        return

    database.remove_mu_data(char, mu_db)
    await ctx.send("I removed the MU write up for **{}** Bruh {}".format(char, croc_emote))


@bot.command(name="removerole")
@commands.has_permissions(administrator=True)
async def remove_role(ctx: commands.Context):
    """
    Async function that removes the given role from all users.

    :param ctx: `commands.Context`
    :return: `None`
    """
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
    """
    Async function that sends the booster leaderboard.

    :param ctx: `commands.Context`
    :return: `None`
    """
    boosters: dict = boost.get_boosters(ctx)
    if len(boosters) == 0:
        await ctx.send("No one boosted this server Bruh {}".format(croc_emote))
        return

    msg: str = boost.build_leaderboard(boosters)
    await ctx.send(top10_msg.format(msg))
    await boost.update_leaderboard(ctx)


@bot.command(name="boost")
async def send_funny_boost(ctx: commands.Context):
    """
    Async function that sends a booster only msg.

    :param ctx: `commands.Context`
    :return: `None`
    """
    if ctx.author in ctx.guild.premium_subscribers:
        await ctx.send("What's up booster Bruh {}. Imagine not being a booster {}".format(croc_emote, lul_emote))
    else:
        await ctx.message.add_reaction(dab_emote)
    await boost.update_leaderboard(ctx)


@bot.command(name="meme")
async def send_meme(ctx: commands.Context):
    """
    Async function that sends a random meme.

    :param ctx: `commands.Context`
    :return: `None`
    """
    seed()
    with open("memes", "r") as f:
        embed: Embed = embeds.create_image_embed(choice(f.readlines()))
    embed.add_field(name="Album Link",
                    value="https://imgur.com/a/LpuE5j1?grid")
    await ctx.send(embed=embed)


@remove_role.error
@add_mu.error
async def cmd_error(ctx: commands.Context, error: commands.CommandError):
    """
    Async function to send a message if a user is missing permissions.

    :param ctx: `Context` original user message's context
    :param error: `commands.CommandError` the error invoked by the user
    :return: `None`
    """
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(admin_error.format(ctx.author.mention, croc_emote))

bot.run(token)
