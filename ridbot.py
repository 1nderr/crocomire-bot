import discord
import xml.etree.ElementTree as ET

# GLOBALS
#token = "REDACTED"
token = "REDACTED" #Test Bot Token
footerIcon = "https://cdn.discordapp.com/emojis/562502263399251968.png?v=1"
prefix = "?"
imgPath = "Images/"
textCmds = ["op", "social", "help", "vods", "docs"]
embedColor = 10170673
client = discord.Client()
embedTree = ET.parse('embeds.xml')
embedRoot = embedTree.getroot()

# Sets the given embed's thumbnail to a local URL to set a local thumbnail image
def CreateEmbedImage(embed, filename):
	imgURL = "attachment://" + "img.png"
	embed.set_image(url=imgURL)
	f = discord.File(filename, "img.png")
	return f

# Sets the given embed's thumbnail to a local URL to set a local thumbnail image
def CreateEmbedThumbnail(embed, filename):
	imgURL = "attachment://" + "img.png"
	embed.set_thumbnail(url=imgURL)
	f = discord.File(filename, "img.png")
	return f

# Generates an embedded message from the given xml root
def CreateXMLEmbed(title, inline, root, nameAttribute):
	embed = discord.Embed(title=title, color=embedColor)
	for node in root:
		fieldName = node.get(nameAttribute)
		embed.add_field(name=fieldName, value=node.text, inline=inline)
	return embed

# Returns the image of the given move
def GetVizMessage(move):
	embedNode = embedRoot.find(move)
	embed = discord.Embed(color=embedColor)
	filename = imgPath + embedNode.get("image")
	f = CreateEmbedImage(embed, filename)
	return embed, f

# Generates and returns an embedded resource/link message
def GetEmbedMessage(embedName, inline):
	embedNode = embedRoot.find(embedName)
	title = "__" + embedNode.get("name") + "__"
	filename = imgPath + embedNode.get("image")
	embed = CreateXMLEmbed(title, inline, embedNode, "name")
	f = CreateEmbedThumbnail(embed, filename)
	return embed, f

# Changes the bot's presence when ready
@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name="Type %shelp" % prefix))

# Waits for events
@client.event
async def on_message(message):  
	if message.author == client.user:
		return

	try:
		msg = message.content.split()
		givenPre = msg[0][0]
		command = msg[0][1:].lower()
		if command == "stats" or command == "viz":
			move = "".join(msg[1:]).lower()
			if move == "":
				await message.channel.send("Bruh say a move after the command. Ex: `?%s nair`" % command)
	except IndexError:
		return

	if givenPre == prefix:
		if command == "viz":
			embed, image = GetVizMessage(move)
		else:
			if command == "stats":
				embedName = move
				inline = True
			elif command in textCmds:
				embedName = command
				inline = False
			embed, image = GetEmbedMessage(embedName, inline)

		if command == "help":
			await message.author.send(embed=embed, file=image)
		else:
			await message.channel.send(embed=embed, file=image)

client.run(token)