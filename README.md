# BrownBot
BrownBot is a Discord Bot built in Python by @wethegreenpeople, if you want to get a hold of me you can hit me up on the Discord Bots server here: https://discord.gg/0cDvIgU2voWn4BaD or [find me on social media](http://wethegreenpeople.xyz)

# Commands
You can find a full list of brownbots commands by either doing **!help** in a server with BrownBot or, you can [head over here](https://github.com/wethegreenpeople/Brown-Bot/blob/updated/commands.md) to check them out.

# Inviting / Setting up personal instance of BrownBot
If you'd like to invite BrownBot to your server you can follow this link: https://discordapp.com/oauth2/authorize?&client_id=168210514541936640&scope=bot&permissions=0 and you'll be able to invite BrownBot to any server you have proper permissions on.

If you'd like to run your own instance of BrownBot feel free to do so! Assuming you have the proper libraries installed, you should only have to edit three things to get it running.

1. secret_example.py
2. private_example.py
3. bot.py

Everything should be fairly straight forward. You need to remove "_example" from secret and private. You'll also need to put your bot token in secret.py, and if you'd like to use the LoL or Steam commands, you'll need API keys for those respective services.

In bot.py you need to edit `sys.path.insert(0, r'/home/ubuntu/brown/modules')` to point to the directory the modules are held in.

Legal
--------
Brownbot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
