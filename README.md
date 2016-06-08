@@ -1,52 +0,0 @@
[General Features](https://github.com/wethegreenpeople/BrownBot#general-features) | 
[League of Legends Commands](https://github.com/wethegreenpeople/BrownBot#league-of-legends-commands) | 
[Works in progress / Development plans](https://github.com/wethegreenpeople/BrownBot#planned-features--work-in-progress)

# BrownBot
Brownbot is a simple bot that I made in python for Discord. This is a simple project for me to play around with Python
as well as getting a chance to work with API's. 

General Features
--------
**!flood**
Clears the screen of all messages. It doesn't delete anything, it just floods the chat with 50 newlines. Just a brute force way of clearing the screen. Useable only by admins.

**!joke**
Tells you a random joke (currently broken. Will be fixed in the near future)

**!chuck**
Tells you a random chuck norris fact

**!info**
Gives you a full list of the working commands.

League of Legends Commands
------------
**!stats**
Gives you stats about a summoner. Currently it displays stats from their unranked, ranked solo, and ranked team games. It's really broken because if a summoner doesn't have stats for one of those gamemodes, then the whole thing breaks and won't display/displays the wrong information.

**!matchhistory**
Gives you stats about the last one or two games the summoner has played. It's 90% finished. The only bug I've come across is similar to !lol, but doesn't break the whole thing. If a summoner has no champion kills in the match, it won't display stats for that match.

**!id**
Simple. Gives the ID of a summoner. It'd be better if people used their ID when using !lol and !matchhistory because it uses one less API call, but it's not a big deal and I don't expect anyone to memorise their ID. Mainly used for development purposes. Works 100%

**!freechamps**
Displays the current rotation of free champions

Steam commands
------------
**!steam** 
Pulls basic info about a steam account such as a user's last played game/play time and online status.

Planned Features / Work in progress
---------
**Pokemon API**
Useful for looking up quick pokemon stats

**Twitter API**
Not exactly sure what I want to do with this yet, but I thought it'd be neat to incorperate twitter somehow.

Legal
--------
Brownbot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
