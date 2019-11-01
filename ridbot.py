import discord
from os import listdir
from random import choice, seed
from yaml import safe_load as yamlLoad

prefix = "?"
imgPath = "Images/"
memePath = "Memes/"
crocEmote = "<:Crocomire:583880666970718224>"
embedColor = 10170673 

synData = yamlLoad(open("synonyms.yml"))
cmdData = yamlLoad(open("commands.yml"))
cmds = cmdData["cmds"]

client = discord.Client()
tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()


def TranslateMove(move):
	moveList = list(synData.keys())
	if move in moveList:
		return move

	for i in moveList:
		if move in synData[i]:
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


def CreateEmbed(cmd, inline):
	embedData = cmdData[cmd]
	title = "__" + embedData["title"] + "__"
	fields = embedData["fields"]
	embed = discord.Embed(title=title, color=embedColor)
	
	for i in fields.keys():
		embed.add_field(name=i, value=fields[i], inline=inline)

	return embed


def GetEmbedMessage(cmd, inline, thumbnail):
	embed = CreateEmbed(cmd, inline)
	f = None

	if thumbnail:
		filename = imgPath + cmdData[cmd]["image"]
		f = EmbedAttachment(embed, filename, "thumbnail")

	return embed, f


def GetImageMessage(cmd):
	embed = discord.Embed(color=embedColor)

	if cmd == "meme":
		seed()
		img = memePath + choice(listdir(memePath))
	else:
		img = imgPath + cmdData[cmd]["image"]

		if cmd == "muchart":
			survey = cmdData[cmd]["link"]
			embed.add_field(name="Vote Here:", value=survey, inline=False)

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
		embed, attach = GetImageMessage(move)
	elif cmd == "stats":
		embed, attach = GetEmbedMessage(move, True, True)
	elif cmd in cmds["text"]:
		embed, attach = GetEmbedMessage(cmd, False, True)
	elif cmd in cmds["img"]:
		embed, attach = GetImageMessage(cmd)
	elif cmd == "bruh":
		await message.channel.send("Bruh %s" % crocEmote)
		return
	if cmd == "help":
		embed.set_footer(text="Credits: Hitboxes by EyeDonutz | Icon by Gekigami | Bot by 1nder")
		await message.author.send(embed=embed, file=attach)
	else:
		await message.channel.send(embed=embed, file=attach)
	return

client.run(token)
