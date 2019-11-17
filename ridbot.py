import discord
import asyncio
from os import listdir
from random import choice, seed
from yaml import safe_load as yamlLoad

prefix = "?"
imgPath = "Images/"
memePath = "Memes/"
crocEmote = "<:Crocomire:583880666970718224>"
reactEmote = "🔴"
embedColor = 10170673
creditsMsg = "Credits: Hitboxes by EyeDonutz | Icon by Gekigami | Bot by 1nder"
moveError = "Bruh I don't recognize the move \"%s\" %s"

# Dictionary with a "main" move name as the key and synonyms for the move as the values.
# Keeps the move name consistent while allowing for multiple ways to refer to a move. Example: nair = neutral air
synData = yamlLoad(open("synonyms.yml"))

# Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
cmdData = yamlLoad(open("commands.yml"))

# Lists of commands by response type.
imgCmds = cmdData["cmds"]["img"]
embedCmds = cmdData["cmds"]["embed"]
textCmds = cmdData["cmds"]["text"]
allCmds = imgCmds + embedCmds + textCmds

client = discord.Client()
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()


# Takes a move and translates it based on the synonyms dictionary.
# Returns "Invalid Move" if the move does not exist and returns the root move name if the move is a synonym.
def TranslateMove(move):
    moveList = list(synData.keys())
    if move in moveList:
        return move

    for i in moveList:
        if move in synData[i]:
            return i

    return "Invalid Move"


# Generates an embedded message to send to the user.
async def GetEmbed(cmd, move):
    if cmd == "viz":
        embed, attach = CreateImageEmbed(move)
        embed.set_footer(
            text="React with %s to see the stats. (Sender Only)" % reactEmote)
    elif cmd == "stats":
        embed, attach = CreateTextEmbed(move, True)
        embed.set_footer(
            text="React with %s to see the hitbox. (Sender Only)" % reactEmote)
    elif cmd in embedCmds:
        embed, attach = CreateTextEmbed(cmd, False)
    elif cmd in imgCmds:
        embed, attach = CreateImageEmbed(cmd)
    return embed, attach


# Takes in an embed and option for inline or stacked embed text.
# Returns an embeded message object with the given command's text and thumbnail.
def CreateTextEmbed(cmd, inline):
    title = "__" + cmdData[cmd]["title"] + "__"
    fields = cmdData[cmd]["fields"]
    embed = discord.Embed(title=title, color=embedColor)

    for i in fields.keys():
        embed.add_field(name=i, value=fields[i], inline=inline)

    if len(fields.keys()) % 3 != 0 and cmd not in embedCmds:
        embed.add_field(name="‏‏‎‏‏‎ ‎", value="‏‏‎‏‏‎ ‎", inline=inline)

    filename = imgPath + cmdData[cmd]["image"]
    f = CreateEmbedAttachment(embed, filename, "thumbnail")

    return embed, f


# Takes in a cmd name.
# Returns an embed object and image file.
def CreateImageEmbed(cmd):
    embed = discord.Embed(color=embedColor)

    if cmd == "meme":
        seed()
        img = memePath + choice(listdir(memePath))
    else:
        img = imgPath + cmdData[cmd]["image"]

        if cmd == "muchart":
            survey = cmdData[cmd]["link"]
            embed.add_field(name="Vote Here:", value=survey, inline=False)

    f = CreateEmbedAttachment(embed, img, "image")
    return embed, f


# Takes an embed, file name, and option to declare the attachment as a thumbnail or image.
# Returns a file object that can be attached to an embedded message.
def CreateEmbedAttachment(embed, filename, attachType):
    # This assures the image is uploaded as a gif file.
    imgURL = "attachment://" + "img.gif"

    # This sets the url of the image the message will use.
    if attachType == "thumbnail":
        embed.set_thumbnail(url=imgURL)
    elif attachType == "image":
        embed.set_image(url=imgURL)

    f = discord.File(filename, "img.gif")
    return f


# Sends an embedded message based on the user's request.
async def SendEmbed(cmd, embed, attach, req):
    if cmd == "help":
        embed.set_footer(text=creditsMsg)
        resp = await req.author.send(embed=embed, file=attach)
    else:
        resp = await req.channel.send(embed=embed, file=attach)
    return resp


# Waits for a reaction on stats or viz and then sends the opposite command if the message is reacted to.
async def WaitForReaction(cmd, move, msg, req):
    await msg.add_reaction(reactEmote)

    try:
        # Checks if the reaction to a message matches the indicated emoji.
        def CheckReaction(reaction, user):
            return str(reaction.emoji) == reactEmote and user == req.author

        await client.wait_for('reaction_add', timeout=60.0, check=CheckReaction)

        if cmd == "stats":
            embed, attach = CreateImageEmbed(move)
        elif cmd == "viz":
            embed, attach = CreateTextEmbed(move, True)

        await req.channel.send(embed=embed, file=attach)

    except asyncio.TimeoutError:
        return


# Sets the bots status on start up.
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bruh, Type %shelp" % prefix))


@client.event
async def on_message(req):
    if req.author == client.user:
        return

    # Parses the message for the command.
    msg = req.content.split()
    if not msg:
        return

    char1 = msg[0][0]
    if char1 != prefix:
        return

    cmd = msg[0][1:].lower()
    if cmd not in allCmds:
        return

    # Parses the move name.
    move = None
    if cmd == "stats" or cmd == "viz":
        move = "".join(msg[1:]).lower()
        temp = move
        move = TranslateMove(move)
        if move == "Invalid Move":
            await req.channel.send(moveError % (temp, crocEmote))
            return

    # Sends the message response.
    if cmd in textCmds:
        await req.channel.send(cmdData[cmd]["text"])
    else:
        embed, attach = await GetEmbed(cmd, move)
        resp = await SendEmbed(cmd, embed, attach, req)

        # Adds reaction to stats or viz message.
        if cmd == "stats" or cmd == "viz":
            await WaitForReaction(cmd, move, resp, req)

client.run(token)
