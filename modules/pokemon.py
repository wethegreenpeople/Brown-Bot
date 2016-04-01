import discord
from discord.ext import commands
import requests
import json

class pokemon():
	def __init__(self, bot):
		self.bot = bot

	# Pulls basic pokemon information, type, weight, etc
	@commands.command()
	async def pokemon(self, pokemon):
		pokemon = pokemon.lower()
		pokemonPull = requests.get("http://pokeapi.co/api/v2/pokemon/" + pokemon)
		speciesPull = requests.get("http://pokeapi.co/api/v2/pokemon-species/" + pokemon)
		

		# Pulling the evolution information requires an ID and not a pokemon's name.
		evolutionPull = requests.get(str(speciesPull.json()["evolution_chain"]["url"]))

		pokemonId = str(pokemonPull.json()["id"])
		weight = str(pokemonPull.json()["weight"])
		height = str(pokemonPull.json()["height"])
		basexp = str(pokemonPull.json()["base_experience"])
		sprite = str(pokemonPull.json()["sprites"]["front_default"])
		pokemonType = str(pokemonPull.json()["types"][0]["type"]["name"])
		isBaby = str(evolutionPull.json()["chain"]["is_baby"])
		evolvesTo = str(evolutionPull.json()["chain"]["evolves_to"][0]["species"]["name"])

		# Checks if the pokemon has a second type. Hackary because I'm tired
		try:
			pokemonTypeTwo = ", " + str(pokemonPull.json()["types"][1]["type"]["name"])
		except:
			pokemonTypeTwo = ""

		await self.bot.say(
			"```" +
			"Pokemon: " + pokemon + "\n"
			"ID: " + pokemonId + "\n" +
			"Weight: " + weight + "\n" +
			"Height: " + height + "\n" +
			"Base experience: " + basexp + "\n" +
			"Baby?: " + isBaby + "\n" +
			"Evolves to: " + evolvesTo + "\n"
			"Type: " + pokemonType + pokemonTypeTwo +
			"```" +
			sprite
			)

	# Pulls several sprites for the pokemon. Front, back, and front and back shiny.
	@commands.command()
	async def sprites(self, pokemon):
		pokemon = pokemon.lower()
		pokemonPull = requests.get("http://pokeapi.co/api/v2/pokemon/" + pokemon)

		sprite = str(pokemonPull.json()["sprites"]["front_default"])
		backSprite = str(pokemonPull.json()["sprites"]["back_default"])

		shinySprite = str(pokemonPull.json()["sprites"]["front_shiny"])
		shinyBackSprite = str(pokemonPull.json()["sprites"]["back_shiny"])

		await self.bot.say(
			sprite + "\n" +
			backSprite + "\n" +
			shinySprite + "\n" +
			shinyBackSprite
			)


def setup(bot):
	bot.add_cog(pokemon(bot))