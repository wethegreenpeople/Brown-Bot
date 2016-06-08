import discord
from discord.ext import commands
import requests
from os import path
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import sys

class fun():
	def __init__(self, bot):
		self.bot = bot

	# Simply throws out a lot of trumpets. dootdoot thnkx mr skeltal
	@commands.command(description="And his name is John Cena!", hidden=True)
	async def doot(self):
		await self.bot.say(":trumpet:" * 200)

	# Gives you a random Chuck Norris jokes
	@commands.command(description="Gives you a random chuck norris quote")
	async def chuck(self):
		chuckPull = requests.get("http://api.icndb.com/jokes/random")
		if chuckPull.status_code  == 200:
			await self.bot.say(chuckPull.json()["value"]["joke"])

	@commands.command(description="I think I'm blue", hidden=True)
	async def imblue(self):
		await self.bot.say("?play ytsearch:I'm_blue")
		await self.bot.say("```xl" + "\nNow Listen Up Heres A Story About A Little Guy That Lives In A blue World And All Day" +
			" And All Night And Everything He Sees Is Just blue Like Him Inside And Outside blue His"
			" House With A blue Little Window And A blue Corvette And Everything Is blue For Him And"
			" Himself And Everybody Around Cause He Aint Got Nobody To Listen To"
			" Im blue Da Ba Dee Da Ba Die Da Be Dee Da Ba Die Da Ba Dee Da Ba Die```")

	@commands.command(pass_context=True, description="Makes a wordcloud out of the lasst 500 messages from the channel you're in.")
	async def wordcloud(self, ctx, *args):
		images = "/home/ubuntu/brown/modules/images/wordcloud"
		d = path.dirname(__file__)
		
		# if no arguments are given, default to discord logo as the stencil
		try:
			len(*args) > 1
			stencil = path.join(images, str(*args) + ".jpg")
		# Else use the argument to pick a different stencil
		except:
			stencil = path.join(images, "stencil.png")

		with open("/home/ubuntu/brown/modules/words.txt", "w") as text_file:
				text_file.write("")

		async for messages in self.bot.logs_from(ctx.message.channel, limit=500):
			with open("/home/ubuntu/brown/modules/words.txt", "a") as text_file:
				text_file.write(messages.content + "\n")

		# Read the whole text.
		text = open(path.join(d, 'words.txt')).read()

		# read the mask image
		# taken from
		# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
		discordLogo = np.array(Image.open(path.join(d, stencil)))

		wc = WordCloud(background_color="black", max_words=2000, mask=discordLogo, stopwords=STOPWORDS.add("said"))
		# generate word cloud
		wc.generate(text)

		# store to file
		wc.to_file(path.join(d, "words.png"))

		await self.bot.send_file(ctx.message.channel, "/home/ubuntu/brown/modules/words.png", filename="words.png", content=None, tts=False)



def setup(bot):
	bot.add_cog(fun(bot))