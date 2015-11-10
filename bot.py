python bot.py

import discord
import random
import json
import requests

client = discord.Client()
client.login('<BOT EMAIL>', "<BOT PASSWORD>")

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
    if message.content.startswith('!hello'):
        client.send_message(message.channel, 'Hello {}! How are you?'.format(message.author.name))

    if message.content.startswith("!flood"):
        client.send_message(message.channel, "\n" * 50)

    if message.content.startswith("!joke"):
        content = requests.get("http://tambal.azurewebsites.net/joke/random")
        if content.status_code == 200:
            client.send_message(message.channel, content.json()["joke"])

    if message.content.startswith("!swanson"):
        swansonPull = requests.get("http://ron-swanson-quotes.herokuapp.com/quotes")
        if swansonPull.status_code == 200:
            client.send_message(message.channel, swansonPull.json()["quote"])

    if message.content.startswith("!stats"):
        lolStats(message)

    if message.content.startswith("!id"):
        lolId(message)

    if message.content.startswith("!matchhistory"):
        lolMatchhistory(message)

    if message.content.startswith("!freechamps"):
        lolFreeChampions(message)

    if message.content.startswith("!help"):
        helpFile = open("/home/john/Desktop/Programming/Python/help.txt")
        fileContent = helpFile.read()
        client.send_message(message.channel, fileContent)
        helpFile.close()

def lolStats(message):
    #Removes !lol from the setence
    item = [message.content]
    words = ["!stats "]
    item1 = []
    for line in item:
        for w in words:
            line = line.replace(w, "")
        item1.append(line)
    #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
    try:
        int(line)
    except ValueError:
        #finding the ID from the username
        leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+line+"?<API KEY>")
        if leaguePull.status_code == 200:
            line = str(leaguePull.json()[line]["id"])
        else:
            client.send_message(message.channel, leaguePull.status_code)

    #pulling the stats
    leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/"+line+"/summary?season=SEASON2015&<API KEY>")
    if leaguePull.status_code == 200:
        client.send_message(message.channel,
            "**Unranked**\n\n" + 
            "```" +
            "Minion Kills: " + str(leaguePull.json()["playerStatSummaries"][13]["aggregatedStats"]["totalMinionKills"]) + 
            "\nChampion Kills: " + str(leaguePull.json()["playerStatSummaries"][13]["aggregatedStats"]["totalChampionKills"]) +
            "\nWins: " + str(leaguePull.json()["playerStatSummaries"][13]["wins"]) +
            "```")
        try: 
            str(leaguePull.json()["playerStatSummaries"][14]["aggregatedStats"]["totalMinionKills"])
            client.send_message(message.channel,
                "**Ranked Solo 5v5**" + 
                "\n\n"
                "```" +
                "Minion Kills: " + str(leaguePull.json()["playerStatSummaries"][14]["aggregatedStats"]["totalMinionKills"]) + 
                "\nChampion Kills: " + str(leaguePull.json()["playerStatSummaries"][14]["aggregatedStats"]["totalChampionKills"]) +
                "\nWins: " + str(leaguePull.json()["playerStatSummaries"][14]["wins"]) +
                "\nLosses: " + str(leaguePull.json()["playerStatSummaries"][14]["losses"]) +
                "```")
        except:
            client.send_message(message.channel, "This summoner doesn't have Ranked Solo 5v5 stats")

        client.send_message(message.channel,
             "**Ranked Team 5v5**" + 
            "\n\n"
            "```" +
            "Minion Kills: " + str(leaguePull.json()["playerStatSummaries"][5]["aggregatedStats"]["totalMinionKills"]) + 
            "\nChampion Kills: " + str(leaguePull.json()["playerStatSummaries"][5]["aggregatedStats"]["totalChampionKills"]) +
            "\nWins: " + str(leaguePull.json()["playerStatSummaries"][5]["wins"]) +
            "\nLosses: " + str(leaguePull.json()["playerStatSummaries"][5]["losses"]) +
            "```") 
    else:
        client.send_message(message.channel, leaguePull.status_code)

def lolId(message):
    #removes !id from the sentence
    item = [message.content]
    words = ["!id "]
    item1 = []
    for line in item:
        for w in words:
            line = line.replace(w, "")
        item1.append(line)
    #pulls the summoners ID from his username
    leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+line+"?<API KEY>")
    if leaguePull.status_code == 200:
        client.send_message(message.channel, "Summoner ID\n\n" + "```" +
            str(leaguePull.json()[line]["id"]) + 
            "```")
    else:
        client.send_message(message.channel, leaguePull.status_code)

def lolMatchhistory(message):
    #removes !matchhistory from the sentence
    item = [message.content]
    words = ["!matchhistory "]
    item1 = []
    for line in item:
        for w in words:
            line = line.replace(w, "")
        item1.append(line)
    #checks to see if the value inputted is a number or not. So you don't have to run two api calls needlessly
    try:
        int(line)
    except ValueError:
        #finding the ID from the username
        leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/"+line+"?<API KEY>")
        if leaguePull.status_code == 200:
            line = str(leaguePull.json()[line]["id"])
        else:
            client.send_message(message.channel, leaguePull.status_code)

    #pulling the game stats from the last game
    leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"+line+"/recent?<API KEY>")
    if leaguePull.status_code == 200:
        if leaguePull.json()["games"][0]["stats"]["win"] == True:
            winStatus = "****Game Won!****"
        else:
            winStatus = "****Game Lost****"
        
        gameLength = (int(leaguePull.json()["games"][0]["stats"]["timePlayed"]) / 60)
        #pulls champipn name from it's ID
        championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(leaguePull.json()["games"][0]["championId"])+"?champData=info,recommended&<API KEY>")
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
        championPull = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(leaguePull.json()["games"][1]["championId"])+"?champData=info,recommended&<API KEY>")
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

def lolFreeChampions(message):
    item = [message.content]
    words = ["!freechamps "]
    item1 = []
    for line in item:
        for w in words:
            line = line.replace(w, "")
        item1.append(line)
    #pulls free to play champs
    leaguePull = requests.get("https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&<API KEY>")
    #pulls champs info, so I can convert an ID to a name
    champList = []
    aNumber = 0
    draven = 0
    #cycle through the list of free champions, adding their ID's to the "champList"
    while aNumber < 10:
        championName = requests.get("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/"+str(leaguePull.json()["champions"][draven]["id"])+"?champData=info,recommended&<API KEY>")
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
