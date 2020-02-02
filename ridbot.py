import discord
from asyncio import TimeoutError
from random import choice, seed
from yaml import safe_load as yamlLoad

prefix = "?"
charPath = "characters/%s.yml"
embedColor = 10170673
moveError = "The move **%s** does not exist bruh <:Crocomire:583880666970718224>"
charError = "That character doesn't exist bruh <:Crocomire:583880666970718224>"
hBoxError = "**%s** does not have a hitbox gif yet bruh <:Crocomire:583880666970718224>"
statError = "**%s** does not have stats yet bruh <:Crocomire:583880666970718224>"
matchMsg = "There are multiple hitboxes for this move bruh <:Crocomire:583880666970718224>. React with the hitbox you would like (Sender Only):\n```%s```"
nums = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
smashPath = "../SmashStats/"

client = discord.Client()
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()


# Takes a move/char and translates it based on the synonyms yaml.
# Returns False if the move/char does not exist and returns the root move/char name if the move/char is a synonym.
def Translate(og, synFile):
    # Dictionary with a "main" move/char name as the key and synonyms for the move/char as the values.
    # Keeps the move/char name consistent while allowing for multiple ways to refer to a move/char.
    # Example: nair = neutral air, bayonetta = bayo.

    synData = yamlLoad(open(synFile))

    synList = list(synData.keys())
    if og in synList:
        return og

    for i in synList:
        if og in synData[i]:
            return i

    return False


# Takes in a string that could be a character name.
# Returns the data for the character. Returns False if the given character does not exist or has no data.
def GetCharacter(char):
    char = Translate(char, smashPath + "synonyms/characters.yml")
    if not char:
        return False

    # Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
    charData = yamlLoad(open(smashPath + charPath % char))

    if charData == None:
        return False

    return charData


# Takes in a move name and a character's move data.
# Returns the move in a specific format. Returns False if the move was not found.
def GetMove(ogMove, charData):
    move = Translate(ogMove, smashPath + "synonyms/moves.yml")
    if not move:
        for i in charData.keys():
            if "names" in charData[i].keys() and ogMove in charData[i]["names"]:
                move = i
    return move


# Takes in a move name and a character's move data.
# Returns a list of moves that match the move name.
def GetMatchingMoves(moves, charData):
    matching = []

    for i in moves:
        if "image" in charData[i]:
            matching.append(i)

    return matching


# Takes in a list of moves, a character's move data, and the original request.
# Sends a message to the user asking them to pick the move from the list.
# Returns the move that the user picked.
async def ParseMoveSelection(movesList, charData, req):
    msg = ""
    c = 0

    for i in movesList:
        c += 1
        moveName = charData[i]["title"]
        msg += ("\n %d. %s" % (c, moveName))

    resp = await req.channel.send(matchMsg % msg)

    for i in range(len(movesList)):
        await resp.add_reaction(nums[i])

    n = await WaitForReaction(req, resp)
    await resp.delete()

    if n == -1:
        return False
    return movesList[n]


# Takes in an embed and option for inline or stacked embed text.
# Returns an embeded message object with the given command's text and thumbnail.
def CreateTextEmbed(cmdData, cmd, inline):
    title = "__" + cmdData["title"] + "__"

    fields = cmdData["fields"]
    if not fields:
        return False

    embed = discord.Embed(title=title, color=embedColor)

    for i in fields.keys():
        embed.add_field(name=i, value=fields[i], inline=inline)

    if len(fields.keys()) % 3 != 0 and cmd == "stats":
        embed.add_field(name="‏‏‎‏‏‎ ‎", value="‏‏‎‏‏‎ ‎", inline=inline)
    return embed


# Takes in a command/character's data.
# Returns an embed object with an image link.
def CreateImageEmbed(cmdData):
    try:
        imgURL = cmdData["image"]
    except KeyError:
        return False
    embed = discord.Embed(title=cmdData["title"], color=embedColor)
    embed.set_image(url=imgURL)
    return embed


# Returns an embed object containing a random meme
def CreateMemeEmbed():
    seed()
    memes = open("memes", "r")
    memeURLs = memes.readlines()
    imgURL = choice(memeURLs)
    embed = discord.Embed(color=embedColor)
    embed.set_image(url=imgURL)
    return embed


# Takes in the original request, and the response the bot sent.
# Returns a number based on the emoji they picked for the move selected.
# Returns -1 if the user picks nothing.
async def WaitForReaction(req, resp):
    try:
        # Checks if the reaction to a message matches the indicated emoji.
        def CheckReaction(reaction, user):
            e = str(reaction.emoji)
            return e in nums and user == req.author

        # This loop prevents a bug where if you did two stats cmds and reacted to one of them,
        # it would send the follow up message to both messages instead of the one that was reacted to.
        while True:
            await client.wait_for('reaction_add', timeout=120.0, check=CheckReaction)

            # Updates the response sent earlier with the newly added reactions.
            resp = await req.channel.fetch_message(resp.id)

            for r in resp.reactions:
                users = await r.users().flatten()
                if r.count > 1 and req.author in users:
                    n = nums.index(r.emoji)
                    return n

    except TimeoutError:
        return -1

    return -1


# Sets the bots status on start up.
@client.event
async def on_ready():
    servers = list(client.guilds)
    for s in servers:
        print(s.name)
    print(len(servers))
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bruh, Type %shelp" % prefix))


@client.event
async def on_message(req):
    if req.author == client.user:
        return

    # if str(req.content) == "ok." and str(req.author) == "Periodmancer":
    #     while True:
    #         sasd = input("> ")
    #         await req.channel.send(sasd)

    # Parses the message for the command.
    msg = req.content.split()
    if not msg:
        return

    if msg[0][0] != prefix:
        return

    cmd = msg[0][1:].lower()
    moveIndex = 2
    cmdData = {}
    if cmd == "viz" or cmd == "vis" or cmd == "stats":
        # Gets character's move data.
        for i in range(2, len(msg[1:]) + 2):
            char = ''.join(e for e in "".join(
                msg[1:i]) if e.isalnum()).lower()
            temp = GetCharacter(char)
            if temp:
                cmdData = temp
                moveIndex = i

        if not cmdData:
            await req.channel.send(charError % msg[1])
            return

        # Parses the move name.
        if len(msg) > moveIndex:
            move = ''.join(e for e in "".join(
                msg[moveIndex:]) if e.isalpha()).lower().lower()
            tempMove = move

            if move not in cmdData.keys():
                move = GetMove(move, cmdData)

            if not move:
                await req.channel.send(moveError % tempMove)
                return

            # Checks if the move has multiple hitboxes
            matching = [i for i in cmdData.keys() if move in i]
            if len(matching) > 1:
                moves = GetMatchingMoves(matching, cmdData)
                if not moves:
                    await req.channel.send(hBoxError % cmdData[move]["title"])
                    return
                elif len(moves) == 1:
                    move = moves[0]
                else:
                    move = await ParseMoveSelection(moves, cmdData, req)
                    if not move:
                        return
        else:
            move = char
    else:
        # Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
        cmdData = yamlLoad(open("commands.yml"))

    # Sends the message response.
    if cmd == "bruh":
        await req.channel.send("Bruh, Dedede clobbered that there Ridley <:PenguinRidley:562160021161508884>")
        return
    elif cmd == "mori":
        await req.channel.send("https://cdn.discordapp.com/attachments/600471466152296469/673403944545943572/mori.gif")
        return
    elif cmd == "meme":
        embed = CreateMemeEmbed()
    elif cmd == "dab" or "nud3":
        embed = CreateImageEmbed(cmdData[cmd])
    elif cmd in cmdData.keys():
        embed = CreateTextEmbed(cmdData[cmd], cmd, False)
        if cmd == "help":
            await req.author.send(embed=embed)
            return
    elif cmd == "viz":
        embed = CreateImageEmbed(cmdData[move])
        if embed == False:
            await req.channel.send(hBoxError % cmdData[move]["title"])
            return
    elif cmd == "stats":
        embed = CreateTextEmbed(cmdData[move], cmd, True)
        if embed == False:
            await req.channel.send(statError % cmdData[move]["title"])
            return
    else:
        return
    await req.channel.send(embed=embed)

client.run(token)
