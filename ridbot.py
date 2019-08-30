import discord
import xml.etree.ElementTree as ET
from os import listdir
from random import choice, seed

#tokenFile = open("test", "r")
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()
prefix = "?"
imgPath = "Images/"
memePath = "Memes/"
crocEmote = "<:Crocomire:583880666970718224>"
patch = "📝Patch 4.0.0"
textCmds = ["op", "social", "help", "vods", "docs", "levels", "montage", "changes"]
imgCmds = ["meme", "muchart"]
moveset = {}
embedColor = 10170673
client = discord.Client()
embedTree = ET.parse('embeds.xml')
embedRoot = embedTree.getroot()

def ParseSynonyms():
	tree = ET.parse('moveset.xml')
	root = tree.getroot()
	
	for move in root:
		synonyms = []
		for synonym in move:
			synonyms.append(synonym.text)
		moveset[move.tag] = synonyms

def TranslateMove(move):
	moveList = list(moveset.keys())

	if move in moveList:
		return move

	for i in moveList:
		if move in moveset[i]:
			return i

	return "Invalid Move"

def EmbedAttachment(embed, filename, attachType):
	imgURL = "attachment://" + "img.gif"

	if attachType == "thumbnail":
		embed.set_thumbnail(url=imgURL)
	elif attachType == "image":
		embed.set_image(url=imgURL)

	f = discord.File(filename, "img.gif")
	return f

def EmbedXml(title, inline, root, name):
	embed = discord.Embed(title=title, color=embedColor)

	for node in root:
		fieldName = node.get(name)
		embed.add_field(name=fieldName, value=node.text, inline=inline)

	return embed

def GetEmbedMessage(command, inline, thumbnail):
	embedNode = embedRoot.find(command)
	title = "__" + embedNode.get("name") + "__"
	embed = EmbedXml(title, inline, embedNode, "name")
	f = None

	if thumbnail:
		img = imgPath + embedNode.get("image")
		f = EmbedAttachment(embed, img, "thumbnail")

	return embed, f

def GetImageMessage(command):
	embed = discord.Embed(color=embedColor)
	if command == "meme":
		seed()
		img = memePath + choice(listdir(memePath))
	else:
		embedNode = embedRoot.find(command)
		img = imgPath + embedNode.get("image")

		if command == "muchart": 
			embed.add_field(name="Vote Here:", value=embedNode.get("link"), inline=False)

	f = EmbedAttachment(embed, img, "image")
	return embed, f

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
		command = msg[0][1:].lower()

		if command == "stats" or command == "viz":
			move = "".join(msg[1:]).lower()

			if move == "":
				await message.channel.send("Bruh say a move after the command. Ex: `?%s nair` %s" % (command, crocEmote))
				return
			else:
				move = TranslateMove(move)
				if move == "Invalid Move":
					await message.channel.send("Bruh I don't recognize that move %s" % crocEmote)
					return

	except IndexError:
		return

	if command == "viz":
		embed, attach = GetImageMessage(move)
		embed.set_footer(text=patch + " - Hitboxes by @EyeDonutz")

	elif command == "stats":
		embed, attach = GetEmbedMessage(move, True, True)
		embed.set_footer(text=patch)
	elif command in textCmds:
		embed, attach = GetEmbedMessage(command, False, True)
	elif command in imgCmds:
		embed, attach = GetImageMessage(command)
	elif command == "bruh":
		await message.channel.send("Bruh %s" % crocEmote)
		return
	else:
		return

	if command == "help":
		await message.author.send(embed=embed, file=attach)
	else:
		await message.channel.send(embed=embed, file=attach)
	return

ParseSynonyms()
client.run(token)