from typing import List
from sqlite3 import Connection

from discord import Game, Embed, Message, Guild, TextChannel
from discord.ext import commands

from secret import token
from crocomire import embeds, boost, roles, mu, mu_database, cmd_database, info, meme, url, errors, wholesome
from crocomire.mu_model import Matchup
from crocomire.embed_model import EmbedModel

prefix: str = "?"
status_msg: str = "Tubes, Type ?tubes"
owners: List = [257675080262352896, 139148414507155457, 290964436527874058]
rid_id: int = 456142548667465728
lounge_id: int = 456260916720173057

croc_emote: str = "<:Crocomire:583880666970718224>"
lul_emote: str = "<:RidLul:562495276141510667>"
dab_emote: str = "<:RidDab:562492164664197120>"

remove_mu_msg: str = "I removed the MU write up for **{}** Bruh {}"
role_msg: str = "I removed the role **{}** from these users Bruh {}:\n```{}```"
boost_msg: str = "What's up booster Bruh {}. Imagine not being a booster {}"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"
cmd_msg: str = "Bruh, I {} the **?{}** command {}"
add_meme_msg: str = "Bruh, I added this new meme {}"


bot: commands.Bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    activity=Game(status_msg))


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in owners
    return commands.check(predicate)


@bot.command(name="info")
async def send_help(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) == 0:
        embed_model: EmbedModel = info.get_full_info()
        embed_model.set_thumbnail(bot.user.avatar_url)
    elif args[0] in cmd_database.select_all_custom_cmds(cmd_db):
        await ctx.send(errors.no_custom_info)
        return
    elif args[0] in cmd_database.select_all_cmds(cmd_db):
        embed_model: EmbedModel = info.get_cmd_info(args[0])
    else:
        await ctx.send(errors.invalid_cmd)
        return

    embed: Embed = embeds.create_embed(embed_model)
    await ctx.send(embed=embed)


@bot.command(name="mu")
async def send_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        embed_model: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embed_model)
        await ctx.send(embed=embed)
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send(errors.no_char_exists)
        return

    matchup: Matchup = mu.get_matchup(char)
    if matchup is None:
        await ctx.send(errors.no_mu_data)
        return

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="addmu")
@is_owner()
async def add_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        embed_model: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embed_model)
        await ctx.send(embed=embed)
        return

    mu_sections: List = msg.split("\n")
    char: str = "".join(mu_sections[0].split()[1:]).lower()
    char = mu.translate_char(char)
    if len(char) == 0:
        await ctx.send(errors.no_char_exists)
        return

    mu_db: Connection = mu_database.connect_to_mu_db()
    if len(mu_database.select_mu_data(char, mu_db)) != 0:
        matchup = mu.update_matchup(char, mu_sections)
    else:
        matchup = mu.add_matchup(char, mu_sections)

    embed: Embed = embeds.create_mu_embed(matchup)
    await ctx.send(embed=embed)


@bot.command(name="removemu")
@is_owner()
async def remove_mu(ctx: commands.Context):
    msg: str = ctx.message.content
    if len(msg.split()) == 1:
        embed_model: EmbedModel = mu.get_all_chars()
        embed: Embed = embeds.create_embed(embed_model)
        await ctx.send(embed=embed)
        return

    char: str = "".join(msg.split()[1:]).lower()
    char = mu.translate_char(char)

    if len(char) == 0:
        await ctx.send(errors.no_char_exists)
        return

    mu_db: Connection = mu_database.connect_to_mu_db()
    if len(mu_database.select_mu_data(char, mu_db)) == 0:
        await ctx.send(errors.no_mu_data)
        return

    mu_database.remove_mu_data(char, mu_db)
    await ctx.send(remove_mu_msg.format(char, croc_emote))


@bot.command(name="removerole")
@commands.has_permissions(administrator=True)
async def remove_role(ctx: commands.Context):
    if "jmu" not in "".join(ctx.message.content.split()[1:]).lower():
        await ctx.send(errors.not_jmu_role)
        return

    role_name, members = await roles.remove_all_roles(ctx)
    if len(members) == 0:
        await ctx.send(errors.no_role.format(role_name))
        return

    await ctx.send(role_msg.format(role_name, croc_emote, members))


@bot.command(name="boosters")
async def send_leaderboard(ctx: commands.Context):
    boosters: dict = boost.get_boosters(ctx.guild.premium_subscribers)
    if len(boosters) == 0:
        await ctx.send(errors.no_boosts)
        return

    msg: str = boost.build_leaderboard(boosters)
    await ctx.send(top10_msg.format(msg))


@bot.command(name="boost")
async def send_funny_boost(ctx: commands.Context):
    if ctx.author in ctx.guild.premium_subscribers:
        await ctx.send(boost_msg.format(croc_emote, lul_emote))
    else:
        await ctx.message.add_reaction(dab_emote)


@bot.command(name="addcommand", aliases=["addcmd"])
@is_owner()
async def add_cmd(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) < 2:
        await ctx.send(errors.add_cmd_fmt)
        return

    if args[0] == "embed":
        name: str = args[1]
        embed_model: EmbedModel = EmbedModel(name)
        embed_model = embeds.parse_embed_msg(embed_model, ctx.message.content)
        if name not in cmd_database.select_all_cmds(cmd_db):
            cmd_database.insert_embed_cmd(embed_model, cmd_db)
            await ctx.send(cmd_msg.format("created", name, croc_emote))
        elif name in cmd_database.select_all_custom_cmds(cmd_db):
            cmd_database.update_embed_cmd(embed_model, cmd_db)
            await ctx.send(cmd_msg.format("updated", name, croc_emote))
        else:
            await ctx.send(errors.no_update_cmd)
            return

        embed: Embed = embeds.create_embed(embed_model)
        await ctx.send(embed=embed)
    else:
        name: str = args[0]
        text: str = " ".join(args[1:])
        if name in cmd_database.select_all_embed_cmds(cmd_db):
            await ctx.send(errors.wrong_cmd_type)
            return
        if name not in cmd_database.select_all_cmds(cmd_db):
            cmd_database.insert_text_cmd(name, text, cmd_db)
            await ctx.send(cmd_msg.format("created", name, croc_emote))
        elif name in cmd_database.select_all_custom_cmds(cmd_db):
            cmd_database.update_text_cmd(name, text, cmd_db)
            await ctx.send(cmd_msg.format("updated", name, croc_emote))
        else:
            await ctx.send(errors.no_update_cmd)
            return

        text: str = cmd_database.select_text_cmd(name, cmd_db)
        await ctx.send(text)


@bot.command(name="removecommand", aliases=["removecmd"])
@is_owner()
async def remove_cmd(ctx: commands.Context, *args):
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    if len(args) == 0:
        await ctx.send(errors.rm_cmd_fmt)
    else:
        cmd: str = args[0]
        if cmd in cmd_database.select_all_custom_cmds(cmd_db):
            if cmd in cmd_database.select_all_text_cmds(cmd_db):
                cmd_database.remove_text_cmd(cmd, cmd_db)
            else:
                cmd_database.remove_embed_cmd(cmd, cmd_db)
            await ctx.send(cmd_msg.format("removed", cmd, croc_emote))
        else:
            await ctx.send(errors.no_rm_cmd)


@bot.command(name="addmeme")
@is_owner()
async def add_meme(ctx: commands.Context, *args):
    if len(args) == 0:
        await ctx.send(errors.no_meme_given)
    elif url.is_image(args[0]):
        meme.add_meme(args[0])
        embed_model: EmbedModel = EmbedModel("NewMeme")
        embed_model.set_image(args[0])
        embed: Embed = embeds.create_embed(embed_model)
        await ctx.send(embed=embed)
        await ctx.send(add_meme_msg.format(croc_emote))
    else:
        await ctx.send(errors.not_img_url)


@bot.event
async def on_message(msg: Message):
    if len(msg.content) == 0 or bot.user == msg.author or msg.content[0] != prefix:
        return

    cmd: str = msg.content.split()[0][1:]
    if msg.author.id == owners[1] and cmd == "speak":
        self_msg(msg)
        return

    # cmd_db: Connection = cmd_database.connect_to_cmd_db()
    # text_cmds: List = cmd_database.select_all_text_cmds(cmd_db)
    # embed_cmds: List = cmd_database.select_all_embed_cmds(cmd_db)

    # if cmd in text_cmds:
    #     text: str = cmd_database.select_text_cmd(cmd, cmd_db)
    #     await msg.channel.send(text)
    # elif cmd in embed_cmds:
    #     embed_model: EmbedModel = embeds.get_embed_model(cmd)
    #     embed: Embed = embeds.create_embed(embed_model)
    #     await msg.channel.send(embed=embed)
    # else:
    #     await bot.process_commands(msg)
    if cmd == "tubes":
        cmd = "meme"
        embed_model: EmbedModel = embeds.get_embed_model(cmd)
        embed: Embed = embeds.create_embed(embed_model)
        await msg.channel.send(embed=embed)
    else:
        await msg.channel.send(wholesome.give_compliment(msg.author.mention))
    await boost.update_leaderboard(msg.guild)


@remove_role.error
@add_mu.error
@remove_mu.error
@add_cmd.error
@remove_cmd.error
async def cmd_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(errors.not_admin.format(ctx.author.mention))
    else:
        await ctx.send(errors.not_owner.format(ctx.author.mention, croc_emote))


async def self_msg(msg: str):
    ridcord: Guild = bot.get_guild(rid_id)
    chan_id: int = lounge_id

    if len(msg.content.split()) > 1:
        chan_id = int(msg.content.split()[1])
    chan: TextChannel = ridcord.get_channel(chan_id)

    while True:
        m: str = input("> ")
        await chan.send(m)


bot.run(token)
