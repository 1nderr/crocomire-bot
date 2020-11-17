from sqlite3 import Connection
from discord import Embed
from discord.ext import commands
from crocomire.utils import cmd_database, embeds
from crocomire.utils.embed_model import EmbedModel

cmd_msg: str = "I {} the **?{}** command Bruh {}"
croc_emote: str = "<:Crocomire:583880666970718224>"


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Adds a custom text or embed command to the database
    @commands.command(name="addcommand", aliases=["addcmd"])
    @commands.has_permissions(administrator=True)
    async def add_cmd(self, ctx: commands.Context, *args):
        if len(args) < 2:
            await ctx.send(
                "That's not right Bruh {}. The format is `?addcmd <name> <text>` or `?addcmd embed <name> <fields>`.".format(croc_emote))
            return

        cmd_db: Connection = cmd_database.connect_to_cmd_db()

        # If the custom cmd is an embed cmd
        if args[0] == "embed":
            name: str = args[1]
            embed_model: EmbedModel = EmbedModel(name)
            embed_model = embeds.parse_embed_msg(
                embed_model, ctx.message.content)

            # If the command does not already exist, insert it
            if name not in cmd_database.select_all_cmds(cmd_db):
                cmd_database.insert_embed_cmd(embed_model, cmd_db)
                await ctx.send(cmd_msg.format("created", name, croc_emote))
            # If the command does exist, update it
            elif name in cmd_database.select_all_custom_cmds(cmd_db):
                cmd_database.update_embed_cmd(embed_model, cmd_db)
                await ctx.send(cmd_msg.format("updated", name, croc_emote))
            else:
                await ctx.send("You cannot update that command Bruh {}".format(croc_emote))
                return

            embed: Embed = embeds.create_embed(embed_model)
            await ctx.send(embed=embed)
        else:
            name: str = args[0]
            text: str = " ".join(args[1:])
            # If the command already exists as an embed command
            if name in cmd_database.select_all_embed_cmds(cmd_db):
                await ctx.send(
                    "This command is already an image/embed command Bruh {}. Please remove it if you want it to be a text command.".format(croc_emote))
                return

            # If the command does not already exist, insert it
            if name not in cmd_database.select_all_cmds(cmd_db):
                cmd_database.insert_text_cmd(name, text, cmd_db)
                await ctx.send(cmd_msg.format("created", name, croc_emote))
            # If the command does exist, update it
            elif name in cmd_database.select_all_custom_cmds(cmd_db):
                cmd_database.update_text_cmd(name, text, cmd_db)
                await ctx.send(cmd_msg.format("updated", name, croc_emote))
            else:
                await ctx.send("You cannot update that command Bruh {}".format(croc_emote))
                return

            text: str = cmd_database.select_text_cmd(name, cmd_db)
            await ctx.send(text)

    # Removes the given command from the db
    @commands.command(name="removecommand", aliases=["removecmd"])
    @commands.has_permissions(administrator=True)
    async def remove_cmd(self, ctx: commands.Context, cmd_name: str):
        cmd_db: Connection = cmd_database.connect_to_cmd_db()
        # If the command exists in the db
        if cmd_name in cmd_database.select_all_custom_cmds(cmd_db):
            # If it is a text cmd
            if cmd_name in cmd_database.select_all_text_cmds(cmd_db):
                cmd_database.remove_text_cmd(cmd_name, cmd_db)
            # If it is an embed cmd
            else:
                cmd_database.remove_embed_cmd(cmd_name, cmd_db)
            await ctx.send(cmd_msg.format("removed", cmd_name, croc_emote))
        else:
            await ctx.send("You cannot remove that command Bruh {}".format(croc_emote))

    @add_cmd.error
    @remove_cmd.error
    async def perm_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("{} you do not have permission to do that Bruh {}".format(ctx.author.mention, croc_emote))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
