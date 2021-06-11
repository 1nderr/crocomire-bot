from typing import List
from sqlite3 import Connection
from os import path, mkdir

from discord import Game, Embed, Message, Intents, Guild, TextChannel
from discord.ext import commands

from secret import token
from crocomire.utils.embed_model import EmbedModel
from crocomire.utils import embeds, cmd_database, url

from crocomire.cogs.boost import Boost
from crocomire.cogs.mu import Matchup
from crocomire.cogs.custom import CustomCommands
from crocomire.cogs.fun import Fun
from crocomire.cogs.help import Help
from crocomire.cogs.roles import Roles


wonder_id: int = 139148414507155457
img_chans: List[int] = [456254056977924106, 628739256503762954,
                        456578084485988363, 456149873507565568]
prefix: str = "?"
status_msg: str = "Type ?info"
intents = Intents.default()
intents.members = True
bot: commands.Bot = commands.Bot(
    command_prefix=prefix,
    help_command=None,
    activity=Game(status_msg),
    intents=intents)


@bot.event
# This method is to check if a command is a custom added command
# or one that is built into the bot.
async def on_message(msg: Message):
    if bot.user == msg.author or len(msg.content) == 0 or msg.author.bot:
        return

    if msg.content == "how":
        await msg.channel.send("(how)")

    if msg.content[0] != prefix and url.exists(msg.content) and msg.channel.id not in img_chans:
        embed_fail = True
        roles = ["Alpha Pirate", "Gamma Pirate",
                 "Zeta Pirate", "Delta Pirate",
                 "Omega Pirate"]
        for role in msg.author.roles:
            if role.name in roles:
                embed_fail = False
                break
        if embed_fail:
            await msg.channel.send("epic embed fail")
        return

    cmd: str = msg.content.split()[0][1:]
    if msg.author.id == wonder_id and cmd == "speak":
        await self_msg(msg)
        return

    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    text_cmds: List = cmd_database.select_all_text_cmds(cmd_db)
    embed_cmds: List = cmd_database.select_all_embed_cmds(cmd_db)

    # Checks if the cmd is a custom text or embed cmd first
    if cmd in text_cmds:
        text: str = cmd_database.select_text_cmd(cmd, cmd_db)
        await msg.channel.send(text)
        return
    elif cmd in embed_cmds:
        embed_model: EmbedModel = embeds.get_embed_model(cmd)
        embed: Embed = embeds.create_embed(embed_model)
        await msg.channel.send(embed=embed)
        return

    # Processes the hardcoded bot commands if not a custom
    await bot.process_commands(msg)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


@bot.event
async def on_member_join(member):
    await member.send("new fren!")


async def self_msg(msg: str):
    ridcord: Guild = bot.get_guild(456142548667465728)
    chan_id: int = 456260916720173057

    if len(msg.content.split()) > 1:
        chan_id = int(msg.content.split()[1])
    chan: TextChannel = ridcord.get_channel(chan_id)

    while True:
        m: str = input("> ")
        await chan.send(m)


if not path.exists("./databases"):
    mkdir("./databases")

bot.add_cog(Boost(bot))
bot.add_cog(CustomCommands(bot))
bot.add_cog(Fun(bot))
bot.add_cog(Help(bot))
bot.add_cog(Matchup(bot))
bot.add_cog(Roles(bot))
bot.run(token)
