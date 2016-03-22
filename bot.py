import discord
from discord.ext import commands
import requests
import json
import private
import os
import subprocess
import datetime
from tabulate import tabulate

description = '''Brown bot!'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_status(discord.Game(name="!info for help."))

class fun():
	# Simply throws out a lot of trumpets. dootdoot thnkx mr skeltal
	@bot.command()
	async def doot():
		await bot.say(":trumpet:" * 200)

	# Gives you a random Chuck Norris jokes
	@bot.command()
	async def chuck():
		chuckPull = requests.get("http://api.icndb.com/jokes/random")
		if chuckPull.status_code  == 200:
			await bot.say(chuckPull.json()["value"]["joke"])
	
class mod():
	# Throws out 65 new lines so you clear the screen. This is a brute force screen clear
	@bot.command(pass_context=True)
	async def flood(ctx):
		if ctx.message.author.id in open("admins.txt").read():
			await bot.say("\n" * 65)
		else:
			await bot.say("You dont have permission to use this command")

	# Updates the status of the bot
	@bot.command(pass_context=True)
	async def status(ctx, status:str):
		if ctx.message.author.id == "87250476927549440" or "97525736696455168":
			await bot.change_status(discord.Game(name=status))
			await bot.say("Status updated!")
		else:
			await bot.say("You don't have permission to use this command")

class misc():
	@bot.command()
	async def join(invite):
		try:
			await bot.accept_invite(invite)
			await bot.whisper("I joined!")
		except:
			await bot.whisper("Couldn't join the room :(")

	# Gives you a list of servers that the bot is currently in. 
	@bot.command()
	async def serverlist():
		serverList = []
		for s in bot.servers:
			serverList.append(s.name)
		await bot.whisper(serverList)

	@bot.command()
	async def info():
		helpFile = open("commands.txt")
		fileContent = helpFile.read()
		await bot.whisper(fileContent)
		helpFile.close()

class steam():
	# This command just gives you your steam number from your vanity URL. Mostly for debugging.
	@bot.command()
	async def vanity(steamUser):
		steamUser = steamUser.lower()
        
		params = {
		    'key': private.steamApi,
		    'vanityurl': steamUser
		    }

		steamId = requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params)
        
		try:
			await bot.say("Steam ID: " + str(steamId.json()["response"]["steamid"]))
            
		except:
			await bot.say("Sorry, doesn't look like that's a valid vanity URL")

	@bot.command()
	async def steam(steamUser):
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
			except:
				lastPlayed = "No games played in the last two weeks"
			
			# Steam gives you your last played game in minutes, so you divide by 60 for hours played
			recentPlaytime = gameInfo.json()["response"]["games"][0]["playtime_2weeks"] / 60
			totalPlaytime = gameInfo.json()["response"]["games"][0]["playtime_forever"] / 60
			lastPlayed = gameInfo.json()["response"]["games"][0]["name"] + " (recent: " + str(recentPlaytime) + " hrs, total: " + str(totalPlaytime) + " hrs)"
    
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

		await bot.say( 
		"```" +
		"Username: " + steamStuff.username + "\n" +
		"Status: " + userStatus + "\n" +  
		"Last logged on at: " + value.strftime('%Y-%m-%d %H:%M') + "\n" +
		"Location: " + steamStuff.userLocation + "\n" +
		"Last played game: " + str(steamStuff.lastPlayed) + "\n" +
		"```")

class leagueOfLegends():
	@bot.command()
	async def summonerid(summoner):
		summoner = summoner.lower()

		#pulls the summoners ID from his username
		leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
		if leaguePull.status_code == 200:
			await bot.say("Summoner ID\n\n" + "```" +
			str(leaguePull.json()[summoner]["id"]) + 
			"```")
		else:
			await bot.say(leaguePull.status_code)

	@bot.command()
	async def freechamps():
		#pulls free to play champs
		leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&"+private.leagueApi)

		#pulls champs info, so I can convert an ID to a name
		champList = []
		aNumber = 0
		draven = 0

		#cycle through the list of free champions, adding their ID's to the "champList"
		while aNumber < 10:
			championName = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(leaguePull.json()["champions"][draven]["id"])+"?champData=info,recommended&"+private.leagueApi)
			championName = str(championName.json()["name"])
			champList.append(championName)
			aNumber += 1
			draven += 1

		if leaguePull.status_code == 200:
			await bot.say(
			"```" + 
			"**Free to play champs**\n\n" + str(champList) + "\n" + "```"
			)
		else: 
			await bot.say(leaguePull.status_code)

	@bot.command()
	async def matchhistory(summoner, region:str):
		summoner = summoner.lower()
		region = region.lower()

		if region == "eu" or region == "euw":
			#finding the ID from the username
			leaguePull = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
			if leaguePull.status_code == 200:
				summoner = str(leaguePull.json()[summoner]["id"])
			else:
				client.send_message(message.channel, leaguePull.status_code)
			#pulling the game stats from the last game
			leaguePull = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.3/game/by-summoner/"+summoner+"/recent?"+private.leagueApi)
			if leaguePull.status_code == 200:
				if leaguePull.json()["games"][0]["stats"]["win"] == True:
					winStatus = "****Game Won!****"
				else:
					winStatus = "****Game Lost****"

				gameLength = (int(leaguePull.json()["games"][0]["stats"]["timePlayed"]) / 60)
				#pulls champipn name from it's ID
				championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/"+str(leaguePull.json()["games"][0]["championId"])+"?champData=info,recommended&"+private.leagueApi)
				championUsed = str(championPull.json()["name"])

				try: 
					numDeaths = str(leaguePull.json()["games"][0]["stats"]["numDeaths"])
				except KeyError:
					numDeaths = str("0")

				try: 
					champsKilled = str(leaguePull.json()["games"][0]["stats"]["championsKilled"])
				except KeyError:
					champsKilled = str("0")

				try: 
					assists = str(leaguePull.json()["games"][0]["stats"]["assists"])
				except KeyError:
					assists = str("0")

				await bot.say(
					"**Latest Match History**\n\n" + 
					"```" +
					winStatus +
					"\nChampions killed: " + champsKilled +
					"\nNumber of deaths: " + numDeaths +
					"\nAssists: " + assists +
					"\nLength of game: " + str(gameLength) + " minutes" +
					"\nChampion used: " + championUsed +
					"```")

				#pulling stats from the second to last game played
				if leaguePull.json()["games"][1]["stats"]["win"] == True:
					winStatus = "****Game Won!****"
				else:
					winStatus = "****Game Lost****"
				gameLength = (int(leaguePull.json()["games"][1]["stats"]["timePlayed"]) / 60)
				championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/"+str(leaguePull.json()["games"][1]["championId"])+"?champData=info,recommended&"+private.leagueApi)
				championUsed = str(championPull.json()["name"])

				try: 
					str(leaguePull.json()["games"][1]["stats"]["numDeaths"])
					numDeaths = str(leaguePull.json()["games"][1]["stats"]["numDeaths"])
				except KeyError:
					numDeaths = str("0")

				try: 
					str(leaguePull.json()["games"][1]["stats"]["championsKilled"])
					champsKilled = str(leaguePull.json()["games"][1]["stats"]["championsKilled"])
				except KeyError:
					champsKilled = str("0")

				try: 
					str(leaguePull.json()["games"][1]["stats"]["assists"])
					assists = str(leaguePull.json()["games"][1]["stats"]["assists"])
				except KeyError:
					assists = str("0")

				await bot.say(
				"**Previous Match History**\n\n" + 
				"```" +
				winStatus +
				"\nChampions killed: " + champsKilled +
				"\nNumber of deaths: " + numDeaths +
				"\nAssists: " + assists +
				"\nLength of game: " + str(gameLength) + " minutes" +
				"\nChampion used: " + championUsed +
				"```")

		else:
			#finding the ID from the username
			leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
			if leaguePull.status_code == 200:
				summoner = str(leaguePull.json()[summoner]["id"])
			else:
				client.send_message(message.channel, leaguePull.status_code)
			#pulling the game stats from the last game
			leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"+summoner+"/recent?"+private.leagueApi)
			if leaguePull.status_code == 200:
				if leaguePull.json()["games"][0]["stats"]["win"] == True:
					winStatus = "****Game Won!****"
				else:
					winStatus = "****Game Lost****"

				gameLength = (int(leaguePull.json()["games"][0]["stats"]["timePlayed"]) / 60)
				#pulls champipn name from it's ID
				championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(leaguePull.json()["games"][0]["championId"])+"?champData=info,recommended&"+private.leagueApi)
				championUsed = str(championPull.json()["name"])

				try: 
					numDeaths = str(leaguePull.json()["games"][0]["stats"]["numDeaths"])
				except KeyError:
					numDeaths = str("0")

				try: 
					champsKilled = str(leaguePull.json()["games"][0]["stats"]["championsKilled"])
				except KeyError:
					champsKilled = str("0")

				try: 
					assists = str(leaguePull.json()["games"][0]["stats"]["assists"])
				except KeyError:
					assists = str("0")

				await bot.say(
					"**Latest Match History**\n\n" + 
					"```" +
					winStatus +
					"\nChampions killed: " + champsKilled +
					"\nNumber of deaths: " + numDeaths +
					"\nAssists: " + assists +
					"\nLength of game: " + str(gameLength) + " minutes" +
					"\nChampion used: " + championUsed +
					"```")

				#pulling stats from the second to last game played
				if leaguePull.json()["games"][1]["stats"]["win"] == True:
					winStatus = "****Game Won!****"
				else:
					winStatus = "****Game Lost****"
					gameLength = (int(leaguePull.json()["games"][1]["stats"]["timePlayed"]) / 60)
					championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/"+str(leaguePull.json()["games"][1]["championId"])+"?champData=info,recommended&"+private.leagueApi)
					championUsed = str(championPull.json()["name"])

				try: 
					str(leaguePull.json()["games"][1]["stats"]["numDeaths"])
					numDeaths = str(leaguePull.json()["games"][1]["stats"]["numDeaths"])
				except KeyError:
					numDeaths = str("0")

				try: 
					str(leaguePull.json()["games"][1]["stats"]["championsKilled"])
					champsKilled = str(leaguePull.json()["games"][1]["stats"]["championsKilled"])
				except KeyError:
					champsKilled = str("0")

				try: 
					str(leaguePull.json()["games"][1]["stats"]["assists"])
					assists = str(leaguePull.json()["games"][1]["stats"]["assists"])
				except KeyError:
					assists = str("0")

				await bot.say(
					"**Previous Match History**\n\n" + 
					"```" +
					winStatus +
					"\nChampions killed: " + champsKilled +
					"\nNumber of deaths: " + numDeaths +
					"\nAssists: " + assists +
					"\nLength of game: " + str(gameLength) + " minutes" +
					"\nChampion used: " + championUsed +
					"```")

	@bot.command()
	async def stats(summoner, region:str):
		summoner = summoner.lower()

	    #Defaulting to NA. If only a summoner name and no region is input.
		if region == "na":
	        #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
			try:
				int(summoner)
			except ValueError:
			#finding the ID from the username
				leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
				if leaguePull.status_code == 200:
					summoner = str(leaguePull.json()[summoner]["id"])
				else:
					await bot.say(leaguePull.status_code)
				#pulling the stats
				leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/"+summoner+"/summary?season=SEASON2015&"+private.leagueApi)
				aNumber = 0
				unranked = []
				rankedSolo = []
				rankedTeam = []
				rankedTeamTest = 0
				statsLength = len(leaguePull.json()["playerStatSummaries"])
				#Cycling through the dict, then pull the stats
				while str(leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"]) != "Unranked":
					aNumber += 1

			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))
	        
			rankedCheck = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/"+summoner+"/ranked?season=SEASON2015&"+private.leagueApi)
			if rankedCheck.status_code == 200:
				aNumber = 0
				while str(leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"]) != "RankedSolo5x5":
					aNumber += 1

				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))

				aNumber = 0
				while aNumber != statsLength:
					##client.send_message(message.channel, aNumber)
					##client.send_message(message.channel, leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"])
					aNumber += 1
					if aNumber != statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) == "RankedTeam5x5":
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))

						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", rankedTeam[1], rankedTeam[2], rankedTeam[0]]]
						await bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength

					elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
						await bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength
			else:
				table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
				await bot.say("```" +
				str(tabulate(table, headers="firstrow", tablefmt="rst") +
				"```")
				)

		else:
			summonerRegion = region
			#checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
			try:
				int(summoner)
			except ValueError:
				#finding the ID from the username
				leaguePull = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
				if leaguePull.status_code == 200:
					summoner = str(leaguePull.json()[summoner]["id"])
				else:
					await bot.say(leaguePull.status_code)
			#pulling the stats
			leaguePull = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.3/stats/by-summoner/"+summoner+"/summary?season=SEASON2015&"+private.leagueApi)
			aNumber = 0
			unranked = []
			rankedSolo = []
			rankedTeam = []
			rankedTeamTest = 0
			statsLength = len(leaguePull.json()["playerStatSummaries"])
			#Cycling through the dict, then pull the stats
			while str(leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"]) != "Unranked":
				aNumber += 1

			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
			unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))

			rankedCheck = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.3/stats/by-summoner/"+summoner+"/ranked?season=SEASON2015&"+private.leagueApi)
			if rankedCheck.status_code == 200:
				aNumber = 0
				while str(leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"]) != "RankedSolo5x5":
					aNumber += 1

				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
				rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))

				aNumber = 0
				while aNumber != statsLength:
					##client.send_message(message.channel, aNumber)
					##client.send_message(message.channel, leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"])
					aNumber += 1
					if aNumber != statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) == "RankedTeam5x5":
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
						rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))

						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", rankedTeam[1], rankedTeam[2], rankedTeam[0]]]
						await bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength

					elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
						await bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength
			else:
				table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
				await bot.say("```" +
				str(tabulate(table, headers="firstrow", tablefmt="rst") +
				"```")
				)

fun()
mod()
misc()
steam()
leagueOfLegends()

bot.loop.set_debug(True)
bot.run(private.email, private.password)
