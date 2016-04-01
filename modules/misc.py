import discord
from discord.ext import commands
import requests
import json

class misc():
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(description="Invite BrownBot to your server!")
	async def join(self, invite):
		try:
			await self.bot.accept_invite(invite)
			await self.bot.whisper("I joined!")
		except:
			await self.bot.whisper("Couldn't join the room :(")

	# Gives you a list of servers that the bot is currently in. 
	@commands.command(description="Gives a list of servers BrownBot is currently in", hidden="True")
	async def serverlist(self):
		serverCount = 0
		serverList = []
		for s in self.bot.servers:
			serverList.append(s.name)
			serverCount = serverCount + 1
		await self.bot.whisper(serverList)
		await self.bot.whisper(serverCount)

	
		
def setup(bot):
	bot.add_cog(misc(bot))