from sqlite3 import Connection
from crocomire.embed_model import EmbedModel
from crocomire import cmd_database


def get_full_info():
    embedModel: EmbedModel = EmbedModel("info")
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    cmds: dict = cmd_database.select_all_cmds_types(cmd_db)
    embedModel.set_title("Commands List")
    embedModel.set_description("`?info <command>` for more info.")
    embedModel.set_footer("By: 1nder")

    for cmd_type in cmds.keys():
        for i, c in enumerate(cmds[cmd_type]):
            cmds[cmd_type][i] = "`{}`".format(c)
        cmds[cmd_type] = ", ".join(sorted(cmds[cmd_type]))

    embedModel.set_fields(cmds)
    return embedModel


def get_cmd_info(cmd: str):
    embedModel: EmbedModel = EmbedModel("info")
    cmd_db: Connection = cmd_database.connect_to_cmd_db()
    cmdHelp: tuple = cmd_database.select_cmd_help(cmd, cmd_db)
    embedModel.set_title("Command Usage: ?{}".format(cmd))
    embedModel.set_description(cmdHelp[0])
    usageFields: dict = {"Usage": "`{}`".format(cmdHelp[1])}

    if cmdHelp[2] is not None:
        usageFields["Example"] = "`{}`".format(cmdHelp[2])

    embedModel.set_fields(usageFields)

    return embedModel
