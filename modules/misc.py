import discord
from discord.ext import commands
import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class misc():
	def __init__(self, bot):
		self.bot = bot
	
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

	# A thing for work
	@commands.command(hidden="True")
	async def timesheet(self):
		im = Image.open("/home/ubuntu/brown/modules/poo.png")
		draw = ImageDraw.Draw(im)
		font = ImageFont.truetype("DejaVuSans.ttf", 16)

		#box = (100,100,400,400)
		#im = im.crop(box)
		draw.text((0,0), "FUcking test", (0,0,0), font=font)
		im.save("/home/ubuntu/brown/modules/poo11.png")

		await self.bot.say(im.size)

	@commands.command(pass_context=True, hidden=True)
	async def logs2(ctx):
		counter = 0
		async for messages in self.bot.logs_from(ctx.message.channel, limit=500):
		    if ctx.message.author == self.bot.user:
		        counter += 1
		await self.bot.say(counter)


	
		
def setup(bot):
	bot.add_cog(misc(bot))