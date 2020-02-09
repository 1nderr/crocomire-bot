from discord import Game, Embed
from discord.ext import commands
from yaml import safe_load

from secret import token
from crocomire import embeds, memes, boost, roles

prefix: str = "?"
croc_emote: str = "<:Crocomire:583880666970718224>"
status_msg: str = "Bruh, Type ?info"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"
role_msg: str = "I removed the role **{}** from these users Bruh {}:\n```{}```"
role_error: str = "{} you need the permission **Administrator** to remove the role Bruh {}"
cmd_data: dict = safe_load(open("commands.yml"))

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


@bot.command(aliases=cmd_data["commands"])
async def send_text_embed(ctx: commands.Context):
    """
    Async function that sends a command message from commands.yml.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed: Embed = embeds.create_text_embed(cmd_data[ctx.message.content[1:]])
    await ctx.send(embed=embed)


@bot.command(name="meme")
async def send_meme(ctx: commands.Context):
    """
    Async function that sends a random meme.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed: Embed = memes.create_meme_embed()
    await ctx.send(embed=embed)


@bot.command(name="bruh")
async def send_bruh(ctx: commands.Context):
    """
    Async function that sends the bruh message.

    :param ctx: `commands.Context`
    :return: `None`
    """
    await ctx.send("Bruh {}".format(croc_emote))


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
    c: int = 1
    s: str = ""

    for b in list(boosters.keys())[:len(boosters.keys()) - 11:-1]:
        s += "{}. {: <28} {}\n".format(c, b[0:len(b) - 5], boosters[b])
        c += 1

    await ctx.send(top10_msg.format(s))


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


@remove_role.error
async def remove_role_error(ctx: commands.Context, error: commands.CommandError):
    """
    Async function to send a message if a user is missing permissions.

    :param ctx: `Context` original user message's context
    :param error: `commands.CommandError` the error invoked by the user
    :return: `None`
    """
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(role_error.format(ctx.author.mention, croc_emote))


@bot.command(name="mori")
async def send_mori(ctx: commands.Context):
    """
    Async function that sends Mori's special image.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed: Embed = embeds.create_image_embed(
        "https://cdn.discordapp.com/attachments/456260916720173057/675522898471026718/670408231658717206.png")
    await ctx.send(embed=embed)


@bot.command(name="ches")
async def send_ches(ctx: commands.Context):
    """
    Async function that sends Chesnaught's special image.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed: Embed = embeds.create_image_embed(
        "https://cdn.discordapp.com/attachments/567534605091995648/675751591340408838/20200208_111432.gif")
    await ctx.send(embed=embed)

bot.run(token)
