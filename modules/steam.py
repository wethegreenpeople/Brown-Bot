import discord
from discord.ext import commands
import requests
import json
import datetime
import private

class steam():
	def __init__(self, bot):
		self.bot = bot

	# This command just gives you your steam number from your vanity URL. Mostly for debugging.
	@commands.command()
	async def vanity(self, steamUser):
		steamUser = steamUser.lower()
        
		params = {
		    'key': private.steamApi,
		    'vanityurl': steamUser
		    }

		steamId = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params)
        
		try:
			await self.bot.say("Steam ID: " + str(steamId.json()["response"]["steamid"]))
            
		except:
			await self.bot.say("Sorry, doesn't look like that's a valid vanity URL")

	@commands.command()
	async def steam(self, steamUser):
		# Check if you were given a vanity or an ID
		try:
			int(steamUser) + 0
		# Convert to an ID if you were given a vanity
		except:
			params = {
			'key': private.steamApi,
			'vanityurl': steamUser
			}

			steamUser = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params)
			steamUser = steamUser.json()["response"]["steamid"]

		userParams = {
		"key": private.steamApi,
		"steamids": steamUser
		}

		gameParams = {
		"key": private.steamApi,
		"steamid": steamUser
		}

		userInfo = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=userParams)
		gameInfo = requests.get("http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/", params=gameParams)

		class steamStuff:
			#Username
			try:
			    userInfo.json()["response"]["players"][0]["personaname"]
			    username = userInfo.json()["response"]["players"][0]["personaname"]
			except:
				username = "No username :("
    
			#Last played game
			try:
				gameInfo.json()["response"]["total_count"]
				recentPlaytime = gameInfo.json()["response"]["games"][0]["playtime_2weeks"] / 60
				totalPlaytime = gameInfo.json()["response"]["games"][0]["playtime_forever"] / 60
				lastPlayed = gameInfo.json()["response"]["games"][0]["name"] + " (recent: " + str(recentPlaytime) + " hrs, total: " + str(totalPlaytime) + " hrs)"
			except KeyError:
				lastPlayed = "Last played game not available :("
    
			#Location
			try:
			    userInfo.json()["response"]["players"][0]["loccountrycode"]
			    userLocation = userInfo.json()["response"]["players"][0]["loccountrycode"]
			except:
				userLocation = "No location added"
    
		timestamp = userInfo.json()["response"]["players"][0]["lastlogoff"]
		timestamp = int(timestamp)
		value = datetime.datetime.fromtimestamp(timestamp)

		onlineReference = {
			"0": "Offline",
			"1": "Online",
			"2": "Busy",
			"3": "Away",
			"4": "Snooze",
			"5": "Looking to trade",
			"6": "Looking to play"
			}

		userStatus = str(userInfo.json()["response"]["players"][0]["personastate"])
		userStatus = onlineReference[userStatus]

		await self.bot.say( 
		"```" +
		"Username: " + steamStuff.username + "\n" +
		"Status: " + userStatus + "\n" +  
		"Last logged on at: " + value.strftime('%Y-%m-%d %H:%M') + "\n" +
		"Location: " + steamStuff.userLocation + "\n" +
		"Last played game: " + str(steamStuff.lastPlayed) + "\n" +
		"```")

def setup(bot):
	bot.add_cog(steam(bot))