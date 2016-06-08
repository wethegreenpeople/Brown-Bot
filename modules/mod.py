import discord
from discord.ext import commands

class mod():
	def __init__(self, bot):
		self.bot = bot

	# Throws out 65 new lines so you clear the screen. This is a brute force screen clear
	@commands.command(pass_context=True, hidden="True")
	async def flood(self, ctx):
		if ctx.message.author.id in open("admins.txt").read():
			await self.bot.say("\n" * 65)
		else:
			await self.bot.say("You dont have permission to use this command")

	# Updates the status of the bot
	@commands.command(pass_context=True, hidden="True")
	async def status(self, ctx, status:str):
		if ctx.message.author.id == "87250476927549440":
			await self.bot.change_status(discord.Game(name=status))
			await self.bot.say("Status updated!")
		else:
			await self.bot.say("You don't have permission to use this command")

	# Eval command
	@commands.command(pass_context=True, hidden="True")
	async def eval(self, ctx, evaluate:str):
		if ctx.message.author.id == "87250476927549441":
			content = eval(evaluate)
			await self.bot.say(content)
		else:
			await self.bot.say("You don't have permission to use this command")

def setup(bot):
	bot.add_cog(mod(bot))
