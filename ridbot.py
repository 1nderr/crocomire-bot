import discord
from asyncio import TimeoutError
from random import choice, seed
from yaml import safe_load as yamlLoad

prefix = "?"
charPath = "characters/%s.yml"
crocEmote = "<:Crocomire:583880666970718224>"
embedColor = 10170673
moveError1 = "The move **%s** does not exist bruh %s"
charError1 = "The character **%s** doesn't exist bruh %s (Character names can't have spaces)"
charError2 = "The character **%s** has no data yet bruh %s"
hBoxError = "**%s** does not have a hitbox graphic bruh %s"
statError = "**%s** does not have stats yet bruh %s"
matchMsg = "There are multiple hitboxes for this move bruh %s. React with the hitbox you would like (Sender Only):\n```%s```"
nums = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
smashPath = "../SmashStats/"

client = discord.Client()
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()

# Takes a move and translates it based on the synonyms dictionary.
# Returns "Invalid Move" if the move does not exist and returns the root move name if the move is a synonym.
def Translate(og, synFile):
    synData = yamlLoad(open(synFile))

    synList = list(synData.keys())
    if og in synList:
        return og

    for i in synList:
        if og in synData[i]:
            return i

    return "Invalid"


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


# Takes in a cmd name.
# Returns an embed object
def CreateImageEmbed(cmdData):
    try:
        imgURL = cmdData["image"]
    except KeyError:
        return False
    embed = discord.Embed(title=cmdData["title"] ,color=embedColor)
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


# Waits for a reaction on stats or viz and then sends the opposite command if the message is reacted to.
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
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bruh, Type %shelp" % prefix))


@client.event
async def on_message(req):
    if req.author == client.user:
        return

    # Parses the message for the command.
    msg = req.content.split()
    if not msg:
        return

    if msg[0][0] != prefix:
        return

    # Checks cmd type.
    cmd = msg[0][1:].lower()

    if cmd == "viz" or cmd == "stats":
        # Parses the character name.
        char = msg[1].lower()
        tempChar = char
        char = Translate(char, smashPath + "charSynonyms.yml")
        if char == "Invalid":
            await req.channel.send(charError1 % (tempChar, crocEmote))
            return

        # Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
        cmdData = yamlLoad(open(smashPath + (charPath % char)))

        if cmdData == None:
            await req.channel.send(charError2 % (char, crocEmote))
            return

        # Parses the move name.
        move = char
        if len(msg) > 2:
            move = "".join(msg[2:]).lower()
            if move not in cmdData.keys():
                tempMove = move
                move = Translate(move, smashPath + "moveSynonyms.yml")
                if move == "Invalid":
                    await req.channel.send(moveError1 % (tempMove, crocEmote))
                    return

        # Checks if the move has multiple hitboxes
        matching = [i for i in cmdData.keys() if move in i]
        actualMatching = []
        if len(matching) > 1:
            s = ""
            b = 0

            for i in range(len(matching)):
                try:
                    m = cmdData[matching[i]]["image"]
                    actualMatching.append(matching[i])
                except KeyError:
                    b += 1
                    continue
                m = cmdData[matching[i]]["title"]
                s += ("\n %d. %s" % (i+1-b ,m))

            if not actualMatching:
                await req.channel.send(hBoxError % (move, crocEmote))
                return
            elif len(actualMatching) == 1:
                move = actualMatching[0]
            else:
                resp = await req.channel.send(matchMsg % (crocEmote, s))

                for i in range(len(actualMatching)):
                    await resp.add_reaction(nums[i])

                n = await WaitForReaction(req, resp)
                if n == -1:
                    return

                move = actualMatching[n]

                await resp.delete()
    else:
        # Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
        cmdData = yamlLoad(open("commands.yml"))

    # Sends the message response.
    if cmd == "bruh":
        await req.channel.send("Bruh %s" % crocEmote)
        return
    elif cmd == "meme":
        embed = CreateMemeEmbed()
    elif cmd in cmdData.keys():
        embed = CreateTextEmbed(cmdData[cmd], cmd, False)
        if cmd == "help":
            await req.author.send(embed=embed)
            return
    elif cmd == "viz":
        embed = CreateImageEmbed(cmdData[move])
        if embed == False:
            await req.channel.send(hBoxError % (cmdData[move]["title"], crocEmote))
            return
    elif cmd == "stats":
        embed = CreateTextEmbed(cmdData[move], cmd, True)
        if embed == False:
            await req.channel.send(statError % (cmdData[move]["title"], crocEmote))
            return
    else:
        return
    await req.channel.send(embed=embed)

client.run(token)
