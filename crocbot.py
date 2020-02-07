from discord import Game
from discord.ext import commands
from yaml import safe_load

from secret import token
from crocomire import embeds, memes, boost

prefix: str = "?"
croc_emote: str = "<:Crocomire:583880666970718224>"
status_msg: str = "Bruh, Type ?info"
top10_msg: str = "**Top 10 Ridleycord Boosters**```{}```"
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
    embed = embeds.create_text_embed(cmd_data["info"])
    await ctx.author.send(embed=embed)
    await ctx.send(
        "{} Bruh, I sent you a DM {}".format(ctx.author.mention, croc_emote))


@bot.command(aliases=cmd_data["commands"])
async def send_text_embed(ctx: commands.Context):
    """
    Async function that sends a command message from commands.yml.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed = embeds.create_text_embed(cmd_data[ctx.message.content[1:]])
    await ctx.send(embed=embed)


@bot.command(name="meme")
async def send_meme(ctx: commands.Context):
    """
    Async function that sends a random meme.

    :param ctx: `commands.Context`
    :return: `None`
    """
    embed = memes.create_meme_embed()
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
    c: int = 1
    s: str = ""

    for b in list(boosters.keys())[::-1]:
        s += "{}. {: <28} {}\n".format(c, b[0:len(b) - 5], boosters[b])
        c += 1

    await ctx.send(top10_msg.format(s))

bot.run(token)
