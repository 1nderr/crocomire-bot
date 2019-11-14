import discord
from os import listdir
from random import choice, seed
from yaml import safe_load as yamlLoad

prefix = "?"
imgPath = "Images/"
memePath = "Memes/"
crocEmote = "<:Crocomire:583880666970718224>"
embedColor = 10170673
creditsMsg = "Credits: Hitboxes by EyeDonutz | Icon by Gekigami | Bot by 1nder"

# Dictionary with a "main" move name as the key and synonyms for the move as the values.
# Keeps the move name consistent while allowing for multiple ways to refer to a move. Example: nair = neutral air
synData = yamlLoad(open("synonyms.yml"))

# Dictionary with command name as the key and the command attributes (title, text, image, etc.) as the values.
cmdData = yamlLoad(open("commands.yml"))
cmds = cmdData["cmds"]

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


# Takes in an embed and option for inline or stacked embed text.
# Returns an embeded message object with the given command's text and thumbnail.
def CreateTextEmbed(cmd, inline):
	embedData = cmdData[cmd]
	title = "__" + embedData["title"] + "__"
	fields = embedData["fields"]
	embed = discord.Embed(title=title, color=embedColor)

	for i in fields.keys():
		embed.add_field(name=i, value=fields[i], inline=inline)

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


# Sets the bots status on start up.
@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bruh, Type %shelp" % prefix))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	try:
		msg = message.content.split()
		char1 = msg[0][0]

		if char1 != prefix:
			return

		cmd = msg[0][1:].lower()

		if cmd == "stats" or cmd == "viz":
			move = "".join(msg[1:]).lower()

			if move == "":
				await message.channel.send("Bruh say a move after the cmd. Ex: `?%s nair` %s" % (cmd, crocEmote))
				return
			else:
				move = TranslateMove(move)
				if move == "Invalid Move":
					await message.channel.send("Bruh I don't recognize that move %s" % crocEmote)
					return

	except IndexError:
		return

	if cmd == "viz":
		embed, attach = CreateImageEmbed(move)
	elif cmd == "stats":
		embed, attach = CreateTextEmbed(move, True)
	elif cmd in cmds["embed"]:
		embed, attach = CreateTextEmbed(cmd, False)
	elif cmd in cmds["img"]:
		embed, attach = CreateImageEmbed(cmd)

	if cmd in cmds["text"]:
		await message.channel.send(cmdData[cmd]["text"])
	elif cmd == "help":
		embed.set_footer(text=creditsMsg)
		await message.author.send(embed=embed, file=attach)
	else:
		await message.channel.send(embed=embed, file=attach)
	return

client.run(token)
