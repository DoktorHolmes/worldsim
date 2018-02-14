#WorldSim by Victor Yuska
#For Python 3

import random
import sys
import os
import time
import noise
from noise import pnoise2, snoise2, snoise3
from colors import red, green, yellow, blue, magenta, cyan, white, color

#from faker import Faker #Temporary name generation module

class World:
	def __init__(self, width, height, lushness, richness, sealevel, temperature, seed):
		if(seed != None):
			self.seed = seed
		else:
			self.seed = random.randrange(1, 99999)
		self.height = height
		self.width = width
		self.lushness = lushness
		self.richness = richness
		self.temperature = temperature
		self.tileTypes = ["~", "#", "^", "J", "C"]
		self.tiles = []
		self.sealevel = sealevel
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
				if(self.tiles[x][y].color == "cyan"):
					sys.stdout.write(cyan(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "white"):
					sys.stdout.write(white(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "green"):
					sys.stdout.write(green(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "yellow"):
					sys.stdout.write(yellow(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "blue"):
					sys.stdout.write(blue(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "magenta"):
					sys.stdout.write(magenta(self.tiles[x][y].type))
				elif(self.tiles[x][y].color == "red"):
					sys.stdout.write(red(self.tiles[x][y].type))
				elif(self.tiles[x][y].colorX != None):
					sys.stdout.write(color(self.tiles[x][y].type, self.tiles[x][y].colorX))
				else:
					sys.stdout.write(self.tiles[x][y].type)
	def printBiomeMap(self):
		for y in range(0, self.height):
			print("")
			for x in range(0, self.width):
				sys.stdout.write(self.tiles[x][y].biome)
				
	
	def generatePerlinMap(self, octaves):
		freq = 16.0 * octaves
		for x in range(self.width):
			for y in range(self.height):	
				elevation = int(snoise3(x / freq, y / freq, self.seed, octaves) * 127.0 + 128.0)
				self.tiles[x][y].elevation = elevation
				if(elevation >= self.sealevel + 85):
					self.tiles[x][y].type = "^"
				elif(elevation >= self.sealevel):
					self.tiles[x][y].type = "#"
				else:
					self.tiles[x][y].type = "~"
	def generateBiomeMap(self, octaves):
		freq = 13.0 * octaves
		for x in range(self.width):
			for y in range(self.height):	
				biome = int(snoise3(x / freq, y / freq, self.seed, octaves) * 127.0 + 128.0)
				biome += self.temperature
				if(self.tiles[x][y].elevation >= self.sealevel):
					if(self.tiles[x][y].elevation >= self.sealevel + 85):
						self.tiles[x][y].biome = white("^")
						self.tiles[x][y].color = "white"
					elif(biome < 30):
						self.tiles[x][y].biome = cyan("A") #Arctic
						self.tiles[x][y].color = "cyan"
					elif(biome < 80):
						self.tiles[x][y].biome = white("T") #Tundra
						self.tiles[x][y].color = "white"
					elif(biome < 145):
						self.tiles[x][y].biome = green("F") #Forest
						self.tiles[x][y].color = "green"
					elif(biome < 165):
						self.tiles[x][y].biome = color("P", 154) #Plains
						self.tiles[x][y].colorX = 154
					elif(biome < 185):
						self.tiles[x][y].biome = color("W", 94) #Wetlands
						self.tiles[x][y].colorX = 94
					elif(biome < 225):
						self.tiles[x][y].biome = color("J", 64) #Jungle
						self.tiles[x][y].colorX = 64
					else:
						self.tiles[x][y].biome = color("D", 215) #Desert
						self.tiles[x][y].colorX = 215
				else:
					self.tiles[x][y].biome = blue("~") #Ocean
					self.tiles[x][y].color = "blue"
				
				
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
world = World(117, 50, 30, 20, 120, 0, None)
world.generateMap()
world.generatePerlinMap(2)
world.generateBiomeMap(1)

def clearScreen():
	os.system("cls")

	
def game():
	global world
	while True:
		clearScreen()
		world.printBiomeMap()
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
				world.printBiomeMap()
				print("\n\nCOMMANDS: biomes height generate seed back")
				inp2 = input(">: ")
				if(inp2 == "biomes"):
					clearScreen()
					world.printBiomeMap()
					print("\nKEY: \nA - Arctic\nT - Tundra\nF - Forest\nP - Plains\nW - Wetlands\nJ - Jungle\nD - Desert\n^ - Mountain")
					input("\nPRESS ENTER TO CONTINUE")
				elif(inp2 == "height"):
					clearScreen()
					world.printMap()
					input("\nPRESS ENTER TO CONTINUE")
				elif(inp2 == "seed"):
					clearScreen()
					print("Current map seed is " + str(world.seed))
					input("\nPRESS ENTER TO CONTINUE")
				elif(inp2 == "generate"):
					while True:
						clearScreen()
						try:
							width = int(input("Enter the width of the world: "))
							height = int(input("Enter the height of the world: "))
							sealevel = int(input("Enter the sea level (Suggested: 122 to 140):"))
							seed = input("Enter a seed if you want one, otherwise press enter for a random seed:")
							if(seed != ""):
								seed = int(seed)
							else:
								seed = None
							temperature = int(input("Enter temperature offset (Suggested: -20 to 20): "))
							octaves = int(input("Enter a number of octaves (Suggested: 1 to 4): "))
							print("Generating...")
							world = World(width, height, 30, 20, sealevel, temperature, seed)
							world.generateMap()
							world.generatePerlinMap(octaves)
							world.generateBiomeMap(1)
							print("Generation success!")
							time.sleep(1.0)
							break
						except ValueError:
							print("Please enter valid numbers for the width, height, sea level, seed, and octaves!")
							
					
				elif(inp2 == "back"):
					clearScreen()
					world.printBiomeMap()
					break
				else:
					print("Invalid command!")
		else:
			print("Invalid command!")
			print("COMMANDS: races map sim help")
			
			
game()
