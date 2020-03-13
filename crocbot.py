from typing import List
from sqlite3 import Connection

from discord import Game, Embed, Message
from discord.ext import commands

from secret import token
from crocomire import embeds, boost, roles, mu, mu_database, cmd_database, info
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
cmd_msg: str = "Bruh, I {} the **?{}** command {}"

admin_error: str = "{} you need the permission **Administrator** to use that command Bruh {}"
bad_cmd_error: str = "Bruh, that command does not exist {}"
no_name_error: str = "Bruh, that's not right. You didn't give a character name {}"
no_char_error: str = "That character does not exist Bruh {}"
no_data_error: str = "That character does not have any MU data Bruh {}"
bad_role_error: str = "That is not a JMU role Bruh {}"
no_role_error: str = "No one had the role **{}** Bruh {}"
no_boost_error: str = "No one boosted this server Bruh {}"
add_cmd_fmt_err: str = "Bruh, that's not right. The format is `?addcmd <type> <name> <text>` {}"
custom_cmd_error: str = "Bruh, you cannot update that command {}"
invalid_type_err: str = "Bruh, that is not a valid command type. Try `text` or `embed` {}"
no_info_error: str = "Bruh, I do not have info on custom commands {}"
rm_cmd_fmt_err: str = "Bruh, that's not right. You didn't give the command name {}"
no_remove_error: str = "Bruh, you cannot remove that command {}"

bot: commands.Bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    activity=Game(status_msg))


@bot.command(name="info")
async def send_help(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) == 0:
        embedModel: EmbedModel = info.get_full_info()
        embedModel.set_thumbnail(bot.user.avatar_url)
    elif args[0] in cmd_database.select_all_custom_cmds(cmd_db):
        await ctx.send(no_info_error.format(croc_emote))
        return
    elif args[0] in cmd_database.select_all_cmds(cmd_db):
        embedModel: EmbedModel = info.get_cmd_info(args[0])
    else:
        await ctx.send(bad_cmd_error.format(croc_emote))
        return

    embed: Embed = embeds.create_embed(embedModel)
    await ctx.send(embed=embed)


@bot.command(name="mu")
async def send_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        embedModel: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embedModel)
        await ctx.send(embed=embed)
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
@commands.is_owner()
async def add_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        embedModel: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embedModel)
        await ctx.send(embed=embed)
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
        embedModel: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embedModel)
        await ctx.send(embed=embed)
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


@bot.command(name="addcommand", aliases=["addcmd"])
@commands.has_permissions(administrator=True)
async def add_cmd(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) < 3:
        await ctx.send(add_cmd_fmt_err.format(croc_emote))

    if args[0] == "text":
        name: str = args[1]
        text: str = " ".join(args[2:])
        if name not in cmd_database.select_all_cmds(cmd_db):
            cmd_database.insert_text_cmd(name, text, cmd_db)
            await ctx.send(cmd_msg.format("created", name, croc_emote))
        elif name in cmd_database.select_all_custom_cmds(cmd_db):
            cmd_database.update_text_cmd(name, text, cmd_db)
            await ctx.send(cmd_msg.format("updated", name, croc_emote))
        else:
            await ctx.send(custom_cmd_error.format(croc_emote))
            return

        text: str = cmd_database.select_text_cmd(name, cmd_db)
        await ctx.send(text)
    else:
        await ctx.send(invalid_type_err.format(croc_emote))


@bot.command(name="removecommand", aliases=["removecmd"])
@commands.has_permissions(administrator=True)
async def remove_cmd(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) == 0:
        await ctx.send(rm_cmd_fmt_err.format(croc_emote))
    else:
        cmd: str = args[0]
        if cmd in cmd_database.select_all_custom_cmds(cmd_db):
            cmd_database.remove_text_data(cmd, cmd_db)
            await ctx.send(cmd_msg.format("removed", cmd, croc_emote))
        else:
            await ctx.send(no_remove_error.format(croc_emote))


@remove_role.error
@add_mu.error
@remove_mu.error
async def cmd_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(admin_error.format(ctx.author.mention, croc_emote))


@bot.event
async def on_message(msg: Message):
    if bot.user == msg.author:
        return

    cmd: str = msg.content.split()[0][1:]
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    text_cmds: List = cmd_database.select_all_text_cmds(cmd_db)
    embed_cmds: List = cmd_database.select_all_embed_cmds(cmd_db)

    if cmd in text_cmds:
        text: str = cmd_database.select_text_cmd(cmd, cmd_db)
        await msg.channel.send(text)
        return
    elif cmd in embed_cmds:
        embedModel: EmbedModel = embeds.get_embed_model(cmd)
        embed: Embed = embeds.create_embed(embedModel)
        await msg.channel.send(embed=embed)
        return

    await bot.process_commands(msg)


bot.run(token)
