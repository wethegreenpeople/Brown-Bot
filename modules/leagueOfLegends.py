import discord
from discord.ext import commands
import requests
import json
from tabulate import tabulate
import private

class leagueOfLegends():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(description="Pulls a summoner's ID from their username")
	async def summonerid(self, summoner):
		summoner = summoner.lower()

		#pulls the summoners ID from his username
		leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
		if leaguePull.status_code == 200:
			await self.bot.say("Summoner ID\n\n" + "```" +
			str(leaguePull.json()[summoner]["id"]) + 
			"```")
		else:
			await self.bot.say(leaguePull.status_code)

	@commands.command(description="Gives you a list of the current free champs in LoL")
	async def freechamps(self):
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
			await self.bot.say(
			"```" + 
			"**Free to play champs**\n\n" + str(champList) + "\n" + "```"
			)
		else: 
			await self.bot.say(leaguePull.status_code)

	@commands.command(description="Gives a short match history for a summoner.")
	async def matchhistory(self, summoner, region:str):
		summoner = summoner.lower()
		region = region.lower()

		if region == "eu" or region == "euw":
			#finding the ID from the username
			leaguePull = requests.get("https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
			if leaguePull.status_code == 200:
				summoner = str(leaguePull.json()[summoner]["id"])
			else:
				await self.bot.say(leaguePull.status_code)
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

				await self.bot.say(
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

				await self.bot.say(
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
				await self.bot.say(leaguePull.status_code)
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

				await self.bot.say(
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

				await self.bot.say(
					"**Previous Match History**\n\n" + 
					"```" +
					winStatus +
					"\nChampions killed: " + champsKilled +
					"\nNumber of deaths: " + numDeaths +
					"\nAssists: " + assists +
					"\nLength of game: " + str(gameLength) + " minutes" +
					"\nChampion used: " + championUsed +
					"```")

	@commands.command(description="Gives some stats for a summoner")
	async def stats(self, summoner, region:str):
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
					await self.bot.say(leaguePull.status_code)
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
						await self.bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength

					elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
						await self.bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength
			else:
				table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
				await self.bot.say("```" +
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
						await self.bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength

					elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
						table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
						await self.bot.say("```" +
						str(tabulate(table, headers="firstrow", tablefmt="rst") +
						"```")
						)
						aNumber = statsLength
			else:
				table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
				await self.bot.say("```" +
				str(tabulate(table, headers="firstrow", tablefmt="rst") +
				"```")
				)

def setup(bot):
	bot.add_cog(leagueOfLegends(bot))