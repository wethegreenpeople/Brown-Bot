[General Features](https://github.com/wethegreenpeople/BrownBot#general-features) | 
[League of Legends Commands](https://github.com/wethegreenpeople/BrownBot#league-of-legends-commands) | 
[Works in progress / Development plans](https://github.com/wethegreenpeople/BrownBot#planned-features--work-in-progress)

If you have BrownBot in your server you can use !help <commandname> to see specific information on how to use that command

General Features
--------
**!chuck**
Tells you a random chuck norris fact

**!wordcloud**
Make a wordcloud out of the last 500 messages sent in the channel

League of Legends Commands
------------
**!stats**
Gives you stats about a summoner. Currently it displays stats from their unranked, ranked solo, and ranked team games. It's really broken because if a summoner doesn't have stats for one of those gamemodes, then the whole thing breaks and won't display/displays the wrong information.

**!matchhistory**
Gives you stats about the last one or two games the summoner has played. It's 90% finished. The only bug I've come across is similar to !lol, but doesn't break the whole thing. If a summoner has no champion kills in the match, it won't display stats for that match.

**!summonerid**
Simple. Gives the ID of a summoner. It'd be better if people used their ID when using !lol and !matchhistory because it uses one less API call, but it's not a big deal and I don't expect anyone to memorise their ID. Mainly used for development purposes. Works 100%

**!freechamps**
Displays the current rotation of free champions

Steam commands
------------
**!steam** 
Pulls basic info about a steam account such as a user's last played game/play time and online status.

**!vanity**
Pulls the steam profile ID number out of a users vanity.

**!brawlhalla*
Posts some info about a users brawlhalla stats. Not very useful as the Brawlhalla API is pretty crap and I'm waiting on a better one.

Pokemon Commands
-----------
**!pokemon**
Shows you information about the Pokemon you want

**!sprites**
Shows you sprites for the pokemon you want


Planned Features / Work in progress
---------
**Graphic info**
Changing around some of the basic text tables to prettyfied pictures

**Twitter API**
Not exactly sure what I want to do with this yet, but I thought it'd be neat to incorperate twitter somehow.
