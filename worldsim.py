#WorldSim by Victor Yuska
#For Python 3

import random
import sys
import os
import noise
from noise import pnoise2, snoise2, snoise3

from faker import Faker #Temporary name generation module

class World:
	def __init__(self, width, height, lushness, richness):
		self.height = height
		self.width = width
		self.lushness = lushness
		self.richness = richness
		self.tileTypes = ["~", "#", "^", "J", "C"]
		self.tiles = []
		self.sealevel = 115
		self.races = [Race(0, "Skerran", "Avian", 1000, "W", 45), Race(0, "Ravakan", "Reptilian", 850, "P", 60), Race(0, "Ahn'litend", "Artificial", 350, "F", 245)]
	def generateMap(self):
		for x in range(0, self.width):
			self.tiles.append([])
			for y in range(0, self.height):
				index = random.randrange(0, len(self.tileTypes) - 1)
				self.tiles[x].append(Tile(x + y, "~", 0, random.randrange(0, self.lushness), random.randrange(0, self.richness)))
	def printMap(self):
		for y in range(0, self.height):
			print("")
			for x in range(0, self.width):
				sys.stdout.write(self.tiles[x][y].type)
	def printBiomeMap(self):
		for y in range(0, self.height):
			print("")
			for x in range(0, self.width):
				sys.stdout.write(self.tiles[x][y].biome)
				
	
	def generatePerlinMap(self, octaves):
		freq = 11.5 * octaves
		seed = random.randrange(1, 1000)
		for x in range(self.width):
			for y in range(self.height):	
				elevation = int(snoise3(x / freq, y / freq, seed, octaves) * 127.0 + 128.0)
				self.tiles[x][y].elevation = elevation
				if(elevation > 200):
					self.tiles[x][y].type = "A"
				elif(elevation > 140):
					self.tiles[x][y].type = "#"
				elif(elevation >= self.sealevel):
					self.tiles[x][y].type = "="
				else:
					self.tiles[x][y].type = "~"
	def generateBiomeMap(self, octaves):
		freq = 15.0 * octaves
		seed = random.randrange(1, 1000)
		for x in range(self.width):
			for y in range(self.height):	
				biome = int(snoise3(x / freq, y / freq, seed, octaves) * 127.0 + 128.0)
				if(self.tiles[x][y].elevation >= self.sealevel):
					if(biome > 170):
						self.tiles[x][y].biome = "A" #Arctic
					elif(biome > 160):
						self.tiles[x][y].biome = "T" #Tundra
					elif(biome > 135):
						self.tiles[x][y].biome = "F" #Forest
					elif(biome > 105):
						self.tiles[x][y].biome = "P" #Plains
					elif(biome > 85):
						self.tiles[x][y].biome = "W" #Wetlands
					elif(biome > 65):
						self.tiles[x][y].biome = "J" #Jungle
					elif(biome > 35):
						self.tiles[x][y].biome = "D" #Desert
					else:
						self.tiles[x][y].biome = "B" #Barren
				else:
					self.tiles[x][y].biome = "~" #Ocean
				
				
class Tile:
	def __init__(self, id, type, elevation, food, metals):
		self.id = id
		self.type = type
		self.food = food
		self.metals = metals
		self.elevation = elevation
		self.color = 7
		self.biome = "B"
class Race:
	def __init__(self, id, name, type, population, biomePref, lifeSpan):
		self.id = id
		self.name = name
		self.type = type
		self.population = population
		self.biomePref = biomePref
		self.lifeSpan = lifeSpan

global world
world = World(100, 30, 30, 20)
world.generateMap()
world.generatePerlinMap(1)
world.generateBiomeMap(1)

def clearScreen():
	os.system("cls")

	
def game(world):
	while True:
		world.printMap()
		print("\n\nWelcome to WorldSim! A simulation of a planet and its inhabitants")
		print("Enter a command below to navigate")
		print("COMMANDS: races map sim help")
		inp = input(">: ")
		if(inp == "races"):
			clearScreen()
			print("RACES:")
			for r in range(len(world.races) - 1):
				print("\n\n" + world.races[r].name)
				print("Type: " + world.races[r].type)
				print("Biome Preference: " + world.races[r].biomePref)
				print("Average Lifespan: " + str(world.races[r].lifeSpan))
			input("PRESS ENTER TO CONTINUE")
		elif(inp == "map"):
			while True:
				clearScreen()
				world.printMap()
				print("\n\nCOMMANDS: biomes height back")
				inp2 = input(">: ")
				if(inp2 == "biomes"):
					clearScreen()
					world.printBiomeMap()
					print("\nKEY: \nA - Arctic\nT - Tundra\nF - Forest\nP - Plains\nW - Wetlands\nJ - Jungle\nD - Desert\nB - Barren")
					input("\nPRESS ENTER TO CONTINUE")
				elif(inp2 == "height"):
					clearScreen()
					world.printMap()
					input("\nPRESS ENTER TO CONTINUE")
				elif(inp2 == "back"):
					clearScreen()
					break
				else:
					print("Invalid command!")
					print("COMMANDS: biomes height back")
		else:
			print("Invalid command!")
			print("COMMANDS: races map sim help")
			
game(world)
