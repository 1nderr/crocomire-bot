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

moveset = {
	"fair":"Fair.png", "fsmash":"Fsmash.png", "ftilt":"Ftilt.png", "fthrow":"fthrow.png",
	"bair":"Bair.png", "bthrow":"bthrow.png",
	"dair":"Dair.png", "dsmash":"Dsmash.png", "dtilt":"Dtilt.png", "dthrow":"dthrow.png",
	"upair":"Uair.png", "upsmash":"Upsmash.png", "uptilt":"Uptilt.png", "upthrow":"uthrow.png",
	"nair":"Nair.png", "neutralair":"Nair.png", "jab":"Jab.png", "ridley":"ridley.png",
	"uair":"Uair.png", "usmash":"Upsmash.png", "uthrow":'uthrow.png', "utilt":"Uptilt.png",
	"dash":"Dash.png", "dashattack":"Dash.png", "da":"Dash.png",
	"downb":"Skewer.png", "sideb":"Space_Pirate_Rush.png", "neutralb":"Plasma.png", "upb":"upB.png",
	"skewer":"Skewer.png", "spr":"Space_Pirate_Rush.png", "plasma":"Plasma.png", "recovery":"upB.png", "wingblitz":"upB.png",
	"forwardair":"Fair.png", "forwardsmash":"Fsmash.png", "forwardtilt":"Ftilt.png", "forwardthrow":"fthrow.png",
	"backair":"Bair.png", "backthrow":"backthrow.png",
	"downair":"Dair.png", "downsmash":"Dsmash.png", "downtilt":"Dtilt.png", "downthrow":"dthrow.png",
	"downspecial":"Skewer.png", "sidespecial":"Space_Pirate_Rush.png", "neutralspecial":"Plasma.png", "upspecial":"upB.png",
	"vods":"vods.png", "op":"op.png", "social":"social.png", "docs":"docs.png", "help":"croc.png"
}

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
	if move in list(moveset.keys()):
		embed = discord.Embed(color=embedColor)
		filename = imgPath + moveset[move]
		f = CreateEmbedImage(embed, filename)
		return embed, f

# Generates and returns an embedded resource/link message
def GetEmbedMessage(embedName, inline):
	print(embedName)
	embedNode = embedRoot.find(embedName)
	title = "__" + embedNode.get("name") + "__"
	filename = imgPath + moveset[embedName]
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