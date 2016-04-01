import discord
from discord.ext import commands
import requests

class fun():
	def __init__(self, bot):
		self.bot = bot

	# Simply throws out a lot of trumpets. dootdoot thnkx mr skeltal
	@commands.command(description="And his name is John Cena!")
	async def doot(self):
		await self.bot.say(":trumpet:" * 200)

	# Gives you a random Chuck Norris jokes
	@commands.command(description="Gives you a random chuck norris quote")
	async def chuck(self):
		chuckPull = requests.get("http://api.icndb.com/jokes/random")
		if chuckPull.status_code  == 200:
			await self.bot.say(chuckPull.json()["value"]["joke"])

	@commands.command(description="I think I'm blue")
	async def imblue(self):
		await self.bot.say("?play ytsearch:I'm_blue")
		await self.bot.say("```xl" + "\nNow Listen Up Heres A Story About A Little Guy That Lives In A blue World And All Day" +
			" And All Night And Everything He Sees Is Just blue Like Him Inside And Outside blue His"
			" House With A blue Little Window And A blue Corvette And Everything Is blue For Him And"
			" Himself And Everybody Around Cause He Aint Got Nobody To Listen To"
			" Im blue Da Ba Dee Da Ba Die Da Be Dee Da Ba Die Da Ba Dee Da Ba Die```")




def setup(bot):
	bot.add_cog(fun(bot))