[General Features](https://github.com/wethegreenpeople/BrownBot#general-features) | 
[League of Legends Commands](https://github.com/wethegreenpeople/BrownBot#league-of-legends-commands) | 
[Works in progress / Development plans](https://github.com/wethegreenpeople/BrownBot#planned-features--work-in-progress)

# BrownBot
Brownbot is a simple bot that I made in python for Discord. This is a simple project for me to play around with Python
as well as getting a chance to work with API's. 

General Features
--------

**!hello**
Responds with hello to the user

**!flood**
Clears the screen of all messages. It doesn't delete anything, it just floods the chat with 50 newlines. 
Helpful because it keeps the messages in the history.

**!joke**
Tells you a random joke using this api: http://tambal.azurewebsites.net/joke/random

**!swanson**
Tells you a random Ron Swanson quote. Uses this api: http://ron-swanson-quotes.herokuapp.com/quotes

**!help**
Gives you a full list of the working commands.

League of Legends Commands
------------
**!lol**
Gives you stats about a summoner. Currently it displays stats from their unranked, ranked solo, and ranked team games. It's really broken because if a summoner doesn't have stats for one of those gamemodes, then the whole thing breaks and won't display/displays the wrong information.

**!matchhistory**
Gives you stats about the last one or two games the summoner has played. It's 90% finished. The only bug I've come across is similar to !lol, but doesn't break the whole thing. If a summoner has no champion kills in the match, it won't display stats for that match.

**!id**
Simple. Gives the ID of a summoner. It'd be better if people used their ID when using !lol and !matchhistory because it uses one less API call, but it's not a big deal and I don't expect anyone to memorise their ID. Mainly used for development purposes. Works 100%


Planned Features / Work in progress
---------
**Story time**
I wanted to add a couple of "forum games" to the bot. One of them is like a classic five word story game,
each user gets to contribute 5 words to continuing a story. Some of the feature is implemented, but I'm a bit stuck
with a good way to show context or the full story.

**Number game**
The other "forum game" that I thought would be fun to add to the bot is a simple counting game. Bot admin can
set a max number that he doesn't have to tell to anyone, and the other users count up to that number.

**League of Legends API**
LoL API has now been added. The code is messy and broken, but the concept is there and there are actually a couple of features that work just fine. Still in development.

**Twitter API**
Not exactly sure what I want to do with this yet, but I thought it'd be neat to incorperate twitter somehow.
