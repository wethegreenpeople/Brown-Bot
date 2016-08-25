import discord
from discord.ext import commands
import requests
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import shutil
from bs4 import BeautifulSoup
import pyscreenshot as ImageGrab
import os
from selenium import webdriver

class pokemon():
	def __init__(self, bot):
		self.bot = bot

	# Screenshot local
	@commands.command(pass_context=True)
	async def pgo(self):
                ImageGrab.grab_to_file("im.png")
                await self.bot.say("kk fam")
                
	
	# Pulls basic pokemon information, type, weight, etc
	@commands.command(pass_context=True)
	async def pokemon(self, ctx, pokemon:str):
		# Check if the pokemon exists in the cache (has been pulled up before)
		# If it has, use the image that already exists
		# If it hasn't, make a new one.
		try:
			pokedex = "/home/ubuntu/brown/modules/images/pokemon/cache/pokemon" + "_" + pokemon + ".png"
			await self.bot.send_file(ctx.message.channel, "/home/ubuntu/brown/modules/images/pokemon/cache/pokemon" + "_" + pokemon + ".png", filename="Pokemon.png", content=None, tts=False)
		except:
			pokemon = pokemon.lower()
			pokemonPull = requests.get("http://pokeapi.co/api/v2/pokemon/" + pokemon)
			speciesPull = requests.get("http://pokeapi.co/api/v2/pokemon-species/" + pokemon)

			test = str(speciesPull.json()["evolution_chain"]["url"])
			test = test.rsplit("/",2)[1]
			
			# Pulling the evolution information requires an ID and not a pokemon's name.
			evolutionPull = requests.get("http://pokeapi.co/api/v2/evolution-chain/" + test)

			pokemonId = str(pokemonPull.json()["id"])
			weight = str(pokemonPull.json()["weight"])
			height = str(pokemonPull.json()["height"])
			basexp = str(pokemonPull.json()["base_experience"])
			sprite = str(pokemonPull.json()["sprites"]["front_default"])
			pokemonType = str(pokemonPull.json()["types"][0]["type"]["name"])
			evolvesTo = []

			# Not all pokemon have three stages of evolution, if it is "missing" an evolution stage it'll insert a
			# empty spot into the array
			try:
				evo1 = str(evolutionPull.json()["chain"]["species"]["name"])
				evolvesTo.append(evo1)
			except:
				evo1 = "No evolutions"

			try:
				evo2 = str(evolutionPull.json()["chain"]["evolves_to"][0]["species"]["name"])
				evolvesTo.append(evo2)
			except:
				evo2 = ""
				evolvesTo.append(evo2)

			try:
				evo3 = str(evolutionPull.json()["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"])
				evolvesTo.append(evo3)
			except:
				evo3 = ""
				evolvesTo.append(evo3)

			# Checks if the pokemon has a second type. Hackary because I'm tired
			try:
				pokemonTypeTwo = ", " + str(pokemonPull.json()["types"][1]["type"]["name"])
			except:
				pokemonTypeTwo = ""

			# Saving the sprite locally, so we can paste it onto the pokedex image
			url = str(pokemonPull.json()["sprites"]["front_default"])
			response = requests.get(url, stream=True)
			with open("/home/ubuntu/brown/modules/images/pokemon/sprite.png", "wb") as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response

			# Saving the shiny sprite
			# Havie to make sure the pokemon has a shiny
			try:
				url = str(pokemonPull.json()["sprites"]["front_shiny"])
				response = requests.get(url, stream=True)
				with open("/home/ubuntu/brown/modules/images/pokemon/sprite_shiny.png", "wb") as out_file:
					shutil.copyfileobj(response.raw, out_file)
				del response
				shiny = Image.open("/home/ubuntu/brown/modules/images/pokemon/sprite_shiny.png")
			except:
				shiny = Image.open("/home/ubuntu/brown/modules/images/pokemon/unknown.png")

			card = Image.open("/home/ubuntu/brown/modules/images/pokemon/pokedex.png")
			draw = ImageDraw.Draw(card)
			font = ImageFont.truetype("/home/ubuntu/brown/modules/Pokemon.ttf", 23)

			# pasting the sprite into the poke dex
			img = Image.open("/home/ubuntu/brown/modules/images/pokemon/sprite.png")
			card.paste(img,(70,80),img.convert('RGBA'))

			# Pasting the shiny sprite
			card.paste(shiny,(318,178),shiny.convert('RGBA'))

			# Adding the pokemon's name
			draw.text((35,15), pokemon.capitalize(), (0,0,0), font=font)

			# Adding the ID number
			draw.text((282,18), "PokeDex #: " + pokemonId, (0,0,0), font=font)

			# Adding pokemon's type
			draw.text((30,235), "Type: " + pokemonType + pokemonTypeTwo, (0,0,0), font=font)

			# Base EXP
			draw.text((30,275), "Base EXP: " + basexp, (0,0,0), font=font)

			# Evolution chains
			draw.text((282,43), "Evolution Chain:", (0,0,0), font=font)
			draw.text((318,65), evolvesTo[0].capitalize(), (0,0,0), font=font)
			draw.text((318,85), evolvesTo[1].capitalize(), (0,0,0), font=font)
			draw.text((318,105), evolvesTo[2].capitalize(), (0,0,0), font=font)
			
			card.save("/home/ubuntu/brown/modules/images/pokemon/cache/pokemon" + "_" + pokemon + ".png")
			await self.bot.send_file(ctx.message.channel, "/home/ubuntu/brown/modules/images/pokemon/cache/pokemon" + "_" + pokemon + ".png", filename="Pokemon.png", content=None, tts=False)

			# Pure text info
			#await self.bot.say(
			#	"```" +
			#	"Pokemon: " + pokemon + "\n"
			#	"ID: " + pokemonId + "\n" +
			#	"Weight: " + weight + "\n" +
			#	"Height: " + height + "\n" +
			#	"Base experience: " + basexp + "\n" +
			#	"Evolution Chain: " + str(evolvesTo[0]) + "," + str(evolvesTo[1]) + "," + str(evolvesTo[2]) + "\n" +
			#	"Type: " + pokemonType + pokemonTypeTwo +
			#	"```" 
				#sprite
			#	)


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
