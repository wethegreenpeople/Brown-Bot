import discord
import json
import requests
from tabulate import tabulate
import datetime as dt
import private

client = discord.Client()
client.login(private.botEmail, private.botPassword)

if not client.is_logged_in:
    print("Logging into discord failed")
    exit(1)

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
def on_message(message):
    if message.content.startswith('!christmas'):
        a = dt.datetime(2013,12,30,23,59,59)
        b = dt.datetime(2013,12,31,23,59,59)
        d = b-a
        client.send_message(message.channel, d.hour())

    if message.content.startswith('!join'):
        invite = message.content.replace("!join ", "")
        client.accept_invite(invite)

    if message.content.startswith("!serverlist"):
        serverList = []
        for s in client.servers:
            serverList.append(s.name)
        client.send_message(message.author, serverList)

    admins = ["87250476927549441", "87250476927549440"]
    if message.content.startswith("?flood"):
        if message.author.id in admins:
            client.send_message(message.channel, "\n" * 50)
        else:
            client.send_message(message.channel, message.author.id)

    if message.content.startswith("!joke"):
        content = requests.get("http://tambal.azurewebsites.net/joke/random")
        if content.status_code == 200:
            client.send_message(message.channel, "```" + str(content.json()["joke"]) + "```")

    if message.content.startswith("!swanson"):
        swansonPull = requests.get("http://ron-swanson-quotes.herokuapp.com/quotes")
        if swansonPull.status_code == 200:
            client.send_message(message.channel, swansonPull.json()["quote"])

    if message.content.startswith("!stats"):
        lolStats(message)

    if message.content.startswith("!teststats"):
        statsTest(message)

    if message.content.startswith("!id"):
        lolId(message)

    if message.content.startswith("!matchhistory"):
        lolMatchhistory(message)
        
    if message.content.startswith("!eumatchhistory"):
        lolMatchhistoryEU(message)

    if message.content.startswith("!freechamps"):
        lolFreeChampions(message)

    if message.content.startswith("!help"):
        helpFile = open("help.txt")
        fileContent = helpFile.read()
        client.send_message(message.author, fileContent)
        helpFile.close()

def join(message):

    client.accept_invite(line)

def statsTest(message):
   #removes alerting code, spaces, and makes summoner name lower case
    summoner = message.content.replace("!teststats ", "")
    summoner = summoner.lower()
    listCheck = summoner.split()
    summoner = str(listCheck[0])

    #Defaulting to NA. If only a summoner name and no region is input.
    if len(listCheck) == 1:
        #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
        try:
            int(summoner)
        except ValueError:
            #finding the ID from the username
            leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
            if leaguePull.status_code == 200:
                summoner = str(leaguePull.json()[summoner]["id"])
            else:
                client.send_message(message.channel, leaguePull.status_code)
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

                    table = [["Rank", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", rankedTeam[1], rankedTeam[2], rankedTeam[0]]]
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength

                elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
                    table = [["Rank", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "No", "Team", "Ranked"]]
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength
        else:
            table = [["Rank", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "No", "Ranked", "Stats"], ["Team Ranked", "No", "Ranked", "Stats"]]
            client.send_message(message.channel, "```" +
            str(tabulate(table, headers="firstrow", tablefmt="rst") +
            "```")
                )

    else:
        summonerRegion = str(listCheck[1])
        #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
        try:
            int(summoner)
        except ValueError:
            #finding the ID from the username
            leaguePull = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
            if leaguePull.status_code == 200:
                summoner = str(leaguePull.json()[summoner]["id"])
            else:
                client.send_message(message.channel, leaguePull.status_code)
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
        unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalNeutralMinionsKilled"]))
        unranked.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalAssists"]))

        rankedCheck = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.3/stats/by-summoner/"+summoner+"/ranked?season=SEASON2015&"+private.leagueApi)
        if rankedCheck.status_code == 200:
            aNumber = 0
            while str(leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"]) != "RankedSolo5x5":
                aNumber += 1

            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))
            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalNeutralMinionsKilled"]))
            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalAssists"]))
            rankedSolo.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["losses"]))

            aNumber = 0
            while aNumber != statsLength:
                ##client.send_message(message.channel, aNumber)
                ##client.send_message(message.channel, leaguePull.json()["playerStatSummaries"][aNumber]["playerStatSummaryType"])
                aNumber += 1
                if aNumber != statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) == "RankedTeam5x5":
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["wins"]))
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalMinionKills"]))
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalChampionKills"]))
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalNeutralMinionsKilled"]))
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["aggregatedStats"]["totalAssists"]))
                    rankedTeam.append(str(leaguePull.json()["playerStatSummaries"][aNumber]["losses"]))

                    "Queue", "Jungle Kills", "Assists", "Losses"
                    table = [["Queue", "Champ Kills", "Wins", "Losses"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", rankedTeam[1], rankedTeam[2], rankedTeam[0]]]
                    table2 = [["Queue", "Minion Kills", "JNG Kills", "Assists"],["Unranked", unranked[3], unranked[4], "N/A"], ["Solo Ranked", rankedSolo[3], rankedSolo[4], rankedSolo[5]], ["Team Ranked", rankedTeam[3], rankedTeam[4], rankedTeam[5]]]
                    client.send_message(message.channel, "```" + "\n" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") + "\n\n" +
                    str(tabulate(table2, headers="firstrow", tablefmt="rst") +
                    "```")
                        ))

                    aNumber = statsLength

                elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
                    table = [["Rank", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "No", "Team", "Ranked"]]
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength
        else:
            table = [["Queue", "Champ Kills", "Wins", "Losses"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
            table2 = [["Queue", "Minion Kills", "JNG Kills", "Assists"],["Unranked", unranked[3], unranked[4], "N/A"], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
            client.send_message(message.channel, "```" + "\n" +
            str(tabulate(table, headers="firstrow", tablefmt="rst") + "\n\n" +
            str(tabulate(table2, headers="firstrow", tablefmt="rst") +
            "```")
                ))

def lolStats(message):
   #removes alerting code, spaces, and makes summoner name lower case
    summoner = message.content.replace("!stats ", "")
    summoner = summoner.lower()
    listCheck = summoner.split()
    summoner = str(listCheck[0])

    #Defaulting to NA. If only a summoner name and no region is input.
    if len(listCheck) == 1:
        #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
        try:
            int(summoner)
        except ValueError:
            #finding the ID from the username
            leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
            if leaguePull.status_code == 200:
                summoner = str(leaguePull.json()[summoner]["id"])
            else:
                client.send_message(message.channel, leaguePull.status_code)
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
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength

                elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
                    table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength
        else:
            table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
            client.send_message(message.channel, "```" +
            str(tabulate(table, headers="firstrow", tablefmt="rst") +
            "```")
                )

    else:
        summonerRegion = str(listCheck[1])
        #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
        try:
            int(summoner)
        except ValueError:
            #finding the ID from the username
            leaguePull = requests.get("https://"+summonerRegion+".api.pvp.net/api/lol/"+summonerRegion+"/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
            if leaguePull.status_code == 200:
                summoner = str(leaguePull.json()[summoner]["id"])
            else:
                client.send_message(message.channel, leaguePull.status_code)
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
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength

                elif aNumber == statsLength and str(leaguePull.json()["playerStatSummaries"][aNumber - 1]["playerStatSummaryType"]) != "RankedTeam5x5":
                    table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", rankedSolo[1], rankedSolo[2], rankedSolo[0]], ["Team Ranked", "N/A", "N/A", "N/A"]]
                    client.send_message(message.channel, "```" +
                    str(tabulate(table, headers="firstrow", tablefmt="rst") +
                    "```")
                        )
                    aNumber = statsLength
        else:
            table = [["Queue", "Minion Kills", "Champion Kills", "Wins"],["Unranked", unranked[1], unranked[2], unranked[0]], ["Solo Ranked", "N/A", "N/A", "N/A"], ["Team Ranked", "N/A", "N/A", "N/A"]]
            client.send_message(message.channel, "```" +
            str(tabulate(table, headers="firstrow", tablefmt="rst") +
            "```")
                )

def lolId(message):
    #removes alerting code, spaces, and makes summoner name lower case
    summoner = message.content.replace("!id ", "")
    summoner = summoner.replace(" ", "")
    summoner = summoner.lower()

    #pulls the summoners ID from his username
    leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+summoner+"?"+private.leagueApi)
    if leaguePull.status_code == 200:
        client.send_message(message.channel, "Summoner ID\n\n" + "```" +
            str(leaguePull.json()[summoner]["id"]) + 
            "```")
    else:
        client.send_message(message.channel, leaguePull.status_code)

def lolMatchhistory(message):
   #removes alerting code, spaces, and makes summoner name lower case
    summoner = message.content.replace("!matchhistory ", "")
    summoner = summoner.lower()
    listCheck = summoner.split()
    summoner = str(listCheck[0])
    if "eu" in listCheck or "euw" in listCheck:
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

            client.send_message(message.channel,
                "**Latest Match History**\n\n" + 
                "```" +
                winStatus +
                "\nNumber of deaths: " + numDeaths +
                "\nChampions killed: " + champsKilled +
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

            client.send_message(message.channel,
                "**Previous Match History**\n\n" + 
                "```" +
                winStatus +
                "\nNumber of deaths: " + numDeaths +
                "\nChampions killed: " + champsKilled +
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

            client.send_message(message.channel,
                "**Latest Match History**\n\n" + 
                "```" +
                winStatus +
                "\nNumber of deaths: " + numDeaths +
                "\nChampions killed: " + champsKilled +
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

            client.send_message(message.channel,
                "**Previous Match History**\n\n" + 
                "```" +
                winStatus +
                "\nNumber of deaths: " + numDeaths +
                "\nChampions killed: " + champsKilled +
                "\nAssists: " + assists +
                "\nLength of game: " + str(gameLength) + " minutes" +
                "\nChampion used: " + championUsed +
                "```")

def lolMatchhistoryEU(message):
    client.send_message(message.channel, "Command changed. Please use !matchhistory <summoner name> <region> instead. Use !help for more info")

def lolFreeChampions(message):
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
        client.send_message(message.channel,
            "```" + 
            "**Free to play champs**\n\n" + str(champList) + "\n" + "```"
            )
    else: 
        client.send_message(message.channel, leaguePull.status_code)


client.run()
