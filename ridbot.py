import discord
import xml.etree.ElementTree as ET

#tokenFile = open("test", "r")
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()
prefix = "?"
imgPath = "Images/"
textCmds = ["op", "social", "help", "vods", "docs"]
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
	imgURL = "attachment://" + "img.png"
	if attachType == "image":
		embed.set_image(url=imgURL)
	elif attachType == "thumbnail":
		embed.set_thumbnail(url=imgURL)
	f = discord.File(filename, "img.png")
	return f

def EmbedXml(title, inline, root, nameAttribute):
	embed = discord.Embed(title=title, color=embedColor)
	for node in root:
		fieldName = node.get(nameAttribute)
		embed.add_field(name=fieldName, value=node.text, inline=inline)
	return embed

def GetEmbedMessage(embedName, embedType, inline, thumbnail):
	embedNode = embedRoot.find(embedName)
	title = "__" + embedNode.get("name") + "__"

	if embedType == "text":
		embed = EmbedXml(title, inline, embedNode, "name")
	elif embedType == "image":
		embed = discord.Embed(color=embedColor)
		img = imgPath + embedNode.get("image")
		f = EmbedAttachment(embed, img, "image")

	if thumbnail:
		img = imgPath + embedNode.get("image")
		f = EmbedAttachment(embed, img, "thumbnail")
	return embed, f

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="Bruh, Type %shelp" % prefix))

@client.event
async def on_message(message):  
	if message.author == client.user:
		return

	try:
		msg = message.content.split()
		char1 = msg[0][0]
		command = msg[0][1:].lower()
		if command == "stats" or command == "viz":
			move = "".join(msg[1:]).lower()
			if move == "":
				await message.channel.send("Bruh say a move after the command. Ex: `?%s nair`" % command)
				return
			else:
				move = TranslateMove(move)
				if move == "Invalid Move":
					await message.channel.send("Bruh I don't recognize that move.")
					return
	except IndexError:
		return

	if char1 == prefix:
		if command == "viz" and move not in textCmds:
			embed, attach = GetEmbedMessage(move, "image", False, False)
		elif command == "stats" and move not in textCmds:
			embed, attach = GetEmbedMessage(move, "text", True, True)
		elif command in textCmds:
			embed, attach = GetEmbedMessage(command, "text", False, True)
		
		if command == "help":
			await message.author.send(embed=embed, file=attach)
		else:
			await message.channel.send(embed=embed, file=attach)

ParseSynonyms()
client.run(token)
