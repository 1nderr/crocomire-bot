from random import choice, seed
from typing import List
from sqlite3 import Connection

from discord import Game, Embed
from discord.ext import commands

from secret import token
from crocomire import embeds, boost, roles, mu, mu_database, cmd_database
from crocomire.mu_model import Matchup
from crocomire.embed_model import EmbedModel

prefix: str = "?"
status_msg: str = "Bruh, Type ?info"

croc_emote: str = "<:Crocomire:583880666970718224>"
lul_emote: str = "<:RidLul:562495276141510667>"
dab_emote: str = "<:RidDab:562492164664197120>"

remove_mu_msg: str = "I removed the MU write up for **{}** Bruh {}"
role_msg: str = "I removed the role **{}** from these users Bruh {}:\n```{}```"
boost_msg: str = "What's up booster Bruh {}. Imagine not being a booster {}"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"

admin_error: str = "{} you need the permission **Administrator** to use that command Bruh {}"
bad_cmd_error: str = "Bruh, that command does not exist {}"
no_name_error: str = "Bruh, that's not right. You didn't give a character name {}"
no_char_error: str = "That character does not exist Bruh {}"
no_data_error: str = "That character does not have any MU data Bruh {}"
bad_role_error: str = "That is not a JMU role Bruh {}"
no_role_error: str = "No one had the role **{}** Bruh {}"
no_boost_error: str = "No one boosted this server Bruh {}"

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
    embedModel: EmbedModel = EmbedModel(cmd)
    embedModel.set_title(embedData[0])
    embedModel.set_description(embedData[1])
    embedModel.set_footer(embedData[2])
    embedModel.set_thumbnail(embedData[3])
    embedModel.set_fields(embedData[5])

    if cmd == "meme":
        with open("databases/memes", "r") as f:
            seed()
            meme = choice(f.readlines())
            embedModel.set_image(meme)
    else:
        embedModel.set_image(embedData[4])

    embed: Embed = embeds.create_embed(embedModel)
    await ctx.send(embed=embed)


@bot.command(name="info")
async def send_help(ctx: commands.Context, *args):
    embedModel: EmbedModel = EmbedModel("info")
    if len(args) == 0:
        cmds: dict = cmd_database.select_all_cmds_types(cmd_db)
        embedModel.set_title("Commands List")
        embedModel.set_description("`?info <command>` for more info.")
        embedModel.set_thumbnail(bot.user.avatar_url)
        embedModel.set_footer("By: 1nder")

        for cmd_type in cmds.keys():
            for i, c in enumerate(cmds[cmd_type]):
                cmds[cmd_type][i] = "`{}`".format(c)
            cmds[cmd_type] = ", ".join(sorted(cmds[cmd_type]))

        embedModel.set_fields(cmds)
    elif args[0] in cmd_database.select_all_cmds(cmd_db):
        cmd: str = args[0]
        cmdHelp: tuple = cmd_database.select_cmd_help(cmd, cmd_db)
        embedModel.set_title("Command Usage: ?{}".format(cmd))
        embedModel.set_description(cmdHelp[0])
        usageFields: dict = {"Usage": "`{}`".format(cmdHelp[1])}

        if cmdHelp[2] is not None:
            usageFields["Example"] = "`{}`".format(cmdHelp[2])

        embedModel.set_fields(usageFields)
    else:
        await ctx.send(bad_cmd_error.format(croc_emote))
        return

    embed: Embed = embeds.create_embed(embedModel)
    await ctx.send(embed=embed)


@bot.command(name="mu")
async def send_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send(no_name_error.format(croc_emote))
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send(no_char_error.format(croc_emote))
        return

    matchup: Matchup = mu.get_matchup(char)
    if matchup is None:
        await ctx.send(no_data_error.format(croc_emote))
        return

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="addmu")
@commands.has_permissions(administrator=True)
async def add_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        await ctx.send(no_name_error.format(croc_emote))
        return

    mu_sections: List = msg.split("\n")
    char: str = "".join(mu_sections[0].split()[1:]).lower()
    char = mu.translate_char(char)
    if len(char) == 0:
        await ctx.send(no_char_error.format(croc_emote))
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
        await ctx.send(no_name_error.format(croc_emote))
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send(no_char_error.format(croc_emote))
        return

    mu_db: Connection = mu_database.connect_to_mu_db()
    if len(mu_database.select_mu_data(char, mu_db)) == 0:
        await ctx.send(no_data_error.format(croc_emote))
        return

    mu_database.remove_mu_data(char, mu_db)
    await ctx.send(remove_mu_msg.format(char, croc_emote))


@bot.command(name="removerole")
@commands.has_permissions(administrator=True)
async def remove_role(ctx: commands.Context):
    if "jmu" not in "".join(ctx.message.content.split()[1:]).lower():
        await ctx.send(bad_role_error.format(croc_emote))
        return

    role_name, members = await roles.remove_all_roles(ctx)
    if len(members) == 0:
        await ctx.send(no_role_error.format(role_name, croc_emote))
        return

    await ctx.send(role_msg.format(role_name, croc_emote, members))


@bot.command(name="boosters")
async def send_leaderboard(ctx: commands.Context):
    boosters: dict = boost.get_boosters(ctx)
    if len(boosters) == 0:
        await ctx.send(no_boost_error.format(croc_emote))
        return

    msg: str = boost.build_leaderboard(boosters)
    await ctx.send(top10_msg.format(msg))
    await boost.update_leaderboard(ctx)


@bot.command(name="boost")
async def send_funny_boost(ctx: commands.Context):
    if ctx.author in ctx.guild.premium_subscribers:
        await ctx.send(boost_msg.format(croc_emote, lul_emote))
    else:
        await ctx.message.add_reaction(dab_emote)
    await boost.update_leaderboard(ctx)


@remove_role.error
@add_mu.error
async def cmd_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(admin_error.format(ctx.author.mention, croc_emote))

bot.run(token)
