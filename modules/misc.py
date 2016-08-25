import discord
from discord.ext import commands
import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textMessage


class misc():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True, pass_context=True)
	async def text(self, ctx, phone, message, carrier):
		if ctx.message.author.id in open("admins.txt").read():
			carriers = {
				"att": "@txt.att.net",
				"tmobile": "@tmomail.net",
			}
			textMessage.toaddrs  = phone + str(carriers[carrier])
			textMessage.doneTextSend(textMessage.start_time, textMessage.get_Time(), message)
		else:
			self.bot.say("Lmao you can't text people")
	
	@commands.command(description="Invite BrownBot to your server!")
	async def join(self):
		await self.bot.say("https://discordapp.com/oauth2/authorize?&client_id=168210514541936640&scope=bot&permissions=0")

	# Gives you a list of servers that the bot is currently in. 
	@commands.command(description="Gives a list of servers BrownBot is currently in", hidden="True")
	async def serverlist(self):
		serverCount = 0
		for s in self.bot.servers:
			serverCount = serverCount + 1
		await self.bot.whisper(serverCount)

	@commands.command(pass_context=True, hidden=True)
	async def logs2(ctx):
		counter = 0
		async for messages in self.bot.logs_from(ctx.message.channel, limit=500):
		    if ctx.message.author == self.bot.user:
		        counter += 1
		await self.bot.say(counter)


	
		
def setup(bot):
	bot.add_cog(misc(bot))