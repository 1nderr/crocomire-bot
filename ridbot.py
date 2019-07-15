#!/usr/bin/env python3
import discord
import xml.etree.ElementTree as ET

# GLOBALS
token = "REDACTED"
#token = "REDACTED" #Test Bot Token
footerIcon = "https://cdn.discordapp.com/emojis/562502263399251968.png?v=1"
docLink = "https://docs.google.com/document/d/1DFeQrzvIgG6XaRa4fw2hULfGLmlLuIRpkZ2hY8FMsW8/edit"
labLink = "https://docs.google.com/spreadsheets/d/1dnxndTKxjMVKTl0v8YYUnY1X80lgOOFK17OAw2BwVpI/edit?usp=sharing"
guideLink = "https://docs.google.com/document/d/1GTCGcJzEWrv4REbv3PfwiWmceZU8NbZhoJCgmb-JAs8/edit?usp=sharing"
vodLink = "https://www.youtube.com/playlist?list=PL7Ejy0uNwbLPkbY79HJwH--6kbkPL6Z9F"
cbLink = "https://www.youtube.com/watch?v=UOtIefuhsAI&list=PLssLy8lTPzI65HcUX_K_6ox9sOtjv79Na"
opLink = "https://streamable.com/zj6gz"
youLink = "https://www.youtube.com/channel/UCPTi_HYm1_96rpIVgXQEeEA"
twitLink = "https://twitter.com/RidleyDiscord"
prefix = "?"
imgPath = "Images/"
embedColor = 10170673
client = discord.Client()
statTree = ET.parse('stats.xml')
cmdTree = ET.parse('commands.xml')

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
	 "downspecial":"Skewer.png", "sidespecial":"Space_Pirate_Rush.png", "neutralspecial":"Plasma.png", "upspecial":"upB.png"
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

# Returns the embedded stat message and image of the given move
def GetStatMessage(move):
	 statRoot = statTree.getroot()
	 statNode = statRoot.find(move)
	 title = "__" + statNode.get("name") + "__"
	 filename = imgPath + moveset[move]
	 embed = CreateXMLEmbed(title, True, statNode, "name")
	 f = CreateEmbedThumbnail(embed, filename)
	 return embed, f

# Generates and returns the embedded help message
def GetHelpMessage():
	 title = "__Ridley Stats Commands__"
	 cmdRoot = cmdTree.getroot()
	 embed = CreateXMLEmbed(title, False, cmdRoot, "name")
	 return embed

# Generates and returns the embedded Ridleycord docs message
def GetDocMessage():
	 title = "__Ridleycord Documentation__"
	 embed = discord.Embed(title=title, color=embedColor)
	 embed.add_field(name="Ultimate Ridley Resource Doc:", value=docLink)
	 embed.add_field(name="Ridley Master Lab Doc:", value=labLink)
	 embed.add_field(name="An in-Depth Guide to Ridley:", value=guideLink)
	 return embed

# Generates and returns the embedded Ridleycord vods message
def GetVodMessage():
	 title = "__Ridley Vods__"
	 embed = discord.Embed(title=title, color=embedColor)
	 embed.add_field(name="Tournament VODs:", value=vodLink)
	 embed.add_field(name="Crew Battle VODs:", value=cbLink)
	 return embed

def GetOPMessage():
	 title = "__Ridleycord Anime Opening__"
	 embed = discord.Embed(title=title, color=embedColor)
	 embed.add_field(name="Streamable:", value=opLink)
	 return embed

def GetSocialMessage():
	 title = "__Ridleycord Social Media__"
	 embed = discord.Embed(title=title, color=embedColor)
	 embed.add_field(name="Twitter:", value=twitLink)
	 embed.add_field(name="YouTube:", value=youLink)
	 return embed

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
			command = msg[0]
			move = "".join(msg[1:]).lower()
	 except IndexError:
			return

	 if command == prefix + "help":
			helpEmbed = GetHelpMessage()
			await message.author.send(embed=helpEmbed)
	 elif command == prefix + "docs":
			docEmbed = GetDocMessage()
			await message.channel.send(embed=docEmbed)
	 elif command == prefix + "vods":
			vodEmbed = GetVodMessage()
			await message.channel.send(embed=vodEmbed)
	 elif command == prefix + "op":
			opEmbed = GetOPMessage()
			await message.channel.send(embed=opEmbed)
	 elif command == prefix + "social":
			socialEmbed = GetSocialMessage()
			await message.channel.send(embed=socialEmbed)
	 elif command == prefix + "viz":
			if len(msg) == 1:
				await message.channel.send("Bruh say a move after the command. Ex: `?stats nair`")
				return
			vizEmbed, image = GetVizMessage(move)
			await message.channel.send(embed=vizEmbed, file=image)
	 elif command == prefix + "stats":
			if len(msg) == 1:
				await message.channel.send("Bruh say a move after the command. Ex: `?stats nair`")
				return
			statEmbed, image = GetStatMessage(move)
			await message.channel.send(embed=statEmbed, file=image)

client.run(token)
