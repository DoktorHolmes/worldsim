#WorldSim by Victor Yuska
#For Python 3

import random
import sys
import os
import time
import math
import noise
import msvcrt
from noise import pnoise2, snoise2, snoise3
from colors import red, green, yellow, blue, magenta, cyan, white, color

#from faker import Faker #Temporary name generation module

class World:
	def __init__(self, width, height, lushness, richness, sealevel, temperature, seed):
		self.worldprefixes = ["Rava","Tesse","Balgo","Fennda","Resha","Tendra","Teska","Ven","Vak'","Rend","Reth'","Dekk'"]
		self.worldsuffixes = ["nor","d","karr","ria","n","ara","re"]
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
		self.year = 1
		self.name = random.choice(self.worldprefixes) + random.choice(self.worldsuffixes)
		self.races = [Race(0, "Skerran", "Avian", 3, "F", 45, 226), Race(1, "Ravakan", "Reptilian", 4, "P", 60, 196), Race(2, "Ahn'litend", "Artificial", 2, "F", 245, 129)]
		self.settlements = []
	def generateMap(self):
		for x in range(0, self.width):
			self.tiles.append([])
			for y in range(0, self.height):
				index = random.randrange(0, len(self.tileTypes) - 1)
				self.tiles[x].append(Tile(x + y, "~", 0, random.randrange(1, self.lushness), random.randrange(1, self.richness)))
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
				if(self.tiles[x][y].settlement != None):
					sys.stdout.write(color(self.tiles[x][y].settlement.type, self.tiles[x][y].colorX))
				elif(self.tiles[x][y].color == "cyan"):
					sys.stdout.write(cyan(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "white"):
					sys.stdout.write(white(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "green"):
					sys.stdout.write(green(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "yellow"):
					sys.stdout.write(yellow(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "blue"):
					sys.stdout.write(blue(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "magenta"):
					sys.stdout.write(magenta(self.tiles[x][y].biome))
				elif(self.tiles[x][y].color == "red"):
					sys.stdout.write(red(self.tiles[x][y].biome))
				elif(self.tiles[x][y].colorX != None):
					sys.stdout.write(color(self.tiles[x][y].biome, self.tiles[x][y].colorX))
				else:
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
					if(y >= 50 and y <= self.height - 50):
						biome += 40
					elif(y >= self.height - 10):
						biome -= 80
					elif(y < 10):
						biome -= 80
					if(self.tiles[x][y].elevation >= self.sealevel + 85):
						self.tiles[x][y].biome = "^"
						self.tiles[x][y].color = "white"
					elif(biome < 30):
						self.tiles[x][y].biome = "A" #Arctic
						self.tiles[x][y].color = "cyan"
					elif(biome < 80):
						self.tiles[x][y].biome = "T" #Tundra
						self.tiles[x][y].color = "white"
					elif(biome < 145):
						self.tiles[x][y].biome = "F" #Forest
						self.tiles[x][y].color = "green"
					elif(biome < 195):
						self.tiles[x][y].biome = "P" #Plains
						self.tiles[x][y].colorX = 154
					elif(biome < 205):
						self.tiles[x][y].biome = "W" #Wetlands
						self.tiles[x][y].colorX = 94
					elif(biome < 225):
						self.tiles[x][y].biome = "J" #Jungle
						self.tiles[x][y].colorX = 64
					else:
						self.tiles[x][y].biome = "D" #Desert
						self.tiles[x][y].colorX = 215
					
				else:
					self.tiles[x][y].biome = blue("~") #Ocean
					self.tiles[x][y].color = "blue"
				
	def generateCities(self):
		for r in range(len(self.races)):
			spawned = 0
			while(spawned < self.races[r].population):
				tile = random.choice(random.choice(self.tiles))
				if(tile.biome == self.races[r].biomePref):
					x = next((i for i, sublist in enumerate(self.tiles) if tile in sublist), -1)
					y = self.tiles[x].index(tile)
					tile.settlement = Settlement(x, y, random.choice(self.worldprefixes) + random.choice(self.worldsuffixes), "%", random.randrange(150, 300), r)
					tile.color = ""
					tile.colorX = self.races[r].color
					self.settlements.append(tile.settlement)
					spawned += 1
	
	
	def doTick(self, ticks):
		self.year += 1 * ticks
		for r in range(len(self.settlements)):
			if(self.settlements[r].warTarget != None):
				warTarget = self.settlements[r].warTarget
				self.settlements[r].population -= math.floor(self.settlements[r].warTarget.population * 0.05) * ticks
				if(self.settlements[r].population < 100):
					self.tiles[self.settlements[r].x][self.settlements[r].y].colorX = self.races[warTarget.raceID].color
					self.settlements[r].warTarget = None
					self.settlements[r].raceID = warTarget.raceID
					self.settlements[r].warTarget = None
			else:
				tile = self.tiles[self.settlements[r].x][self.settlements[r].y]
				self.settlements[r].population += self.settlements[r].population * 0.05 * tile.food
				self.settlements[r].wealth += random.randrange(25, 100) * tile.metals
				if(self.settlements[r].population >= 1000 and self.settlements[r].warTarget == None and random.randrange(1, 100) <= 10):
					for c in range(len(self.settlements)):
						dist = math.hypot(self.settlements[c].x - self.settlements[r].x, self.settlements[c].y - self.settlements[r].y)
						if(dist <= 15):
							self.settlements[r].warTarget = self.settlements[c]
							self.settlements[c].warTarget = self.settlements[r]
				elif(self.settlements[r].population >= 1500 and self.settlements[r].warTarget == None):
					isSpawned = "NONE"
					while(isSpawned == "NONE"):
						tile2 = random.choice(random.choice(self.tiles))
						if(tile2.biome == self.races[self.settlements[r].raceID].biomePref):
							x = next((i for i, sublist in enumerate(self.tiles) if tile2 in sublist), -1)
							y = self.tiles[x].index(tile2)
							dist = math.hypot(self.settlements[r].x - x, self.settlements[r].y - y)
							if(dist <= 15):
								tile2.settlement = Settlement(x, y, random.choice(self.worldprefixes) + random.choice(self.worldsuffixes), "%", 500, self.settlements[r].raceID)
								tile2.color = ""
								tile2.colorX = self.races[self.settlements[r].raceID].color
								self.settlements.append(tile2.settlement)
								isSpawned = True
								self.settlements[r].population -= 500
					isSpawned = "NONE"
class Tile:
	def __init__(self, id, type, elevation, food, metals):
		self.id = id
		self.type = type
		self.food = food
		self.metals = metals
		self.elevation = elevation
		self.color = 7
		self.biome = "B"
		self.settlement = None
class Race:
	def __init__(self, id, name, type, population, biomePref, lifeSpan, color):
		self.id = id
		self.name = name
		self.type = type
		self.population = population
		self.biomePref = biomePref
		self.lifeSpan = lifeSpan
		self.color = color

class Settlement:
	def __init__(self, x, y, name, type, population, raceID):
		self.x = x
		self.y = y
		self.name = name
		self.type = type
		self.population = population
		self.raceID = raceID
		self.development = 1
		self.wealth = 100
		self.warTarget = None



global world
world = World(117, 50, 5, 8, 120, 0, None)
world.generateMap()
world.generatePerlinMap(2)
world.generateBiomeMap(2)
world.generateCities()

def clearScreen():
	os.system("cls")


def sim():
	global world
	while True:
		clearScreen()
		world.printBiomeMap()
		print("\nCOMMANDS: run cities races back")
		inp = input(">: ")
		if(inp == "run"):
			try:
				ticks = int(input("Enter the number of years to run: "))
				yearsDone = 0
				starttime=time.time()
				while (yearsDone < ticks):
					world.doTick(1)
					clearScreen()
					world.printBiomeMap()
					print(world.name + ", in the year " + str(world.year))
					yearsDone += 1
					time.sleep(1.0 - ((time.time() - starttime) % 1.0))
			except ValueError:
				print("Please enter the number of years as a number!")
		elif(inp == "cities"):
			clearScreen()
			print("CITIES:")
			for r in range(len(world.settlements)):
				print("\n" + world.settlements[r].name)
				print("Race: " + world.races[world.settlements[r].raceID].name)
				print("Population: " + str(world.settlements[r].population))
				if(world.settlements[r].warTarget != None):
					print(red("At war with " + str(world.settlements[r].warTarget.name)))
				print("Coordinates: (" + str(world.settlements[r].x) + ", " + str(world.settlements[r].y) + ")")
			input("PRESS ENTER TO CONTINUE")
		elif(inp == "races"):
			clearScreen()
			print("RACES:")
			for r in range(len(world.races)):
				print("\n\n" + world.races[r].name)
				print("Type: " + world.races[r].type)
				print("Biome Preference: " + world.races[r].biomePref)
				print("Average Lifespan: " + str(world.races[r].lifeSpan))
			input("PRESS ENTER TO CONTINUE")
		elif(inp == "back"):
			break
		else:
			print("Invalid command!")

		
def game():
	global world
	while True:
		clearScreen()
		world.printBiomeMap()
		print("\n\nWelcome to WorldSim! A simulation of a planet and its inhabitants")
		print("Enter a command below to navigate")
		print("COMMANDS: races cities map sim help")
		inp = input(">: ")
		if(inp == "races"):
			clearScreen()
			print("RACES:")
			for r in range(len(world.races)):
				print("\n\n" + world.races[r].name)
				print("Type: " + world.races[r].type)
				print("Biome Preference: " + world.races[r].biomePref)
				print("Average Lifespan: " + str(world.races[r].lifeSpan))
			input("PRESS ENTER TO CONTINUE")
		elif(inp == "sim"):
			sim()
		elif(inp == "cities"):
			clearScreen()
			print("CITIES:")
			for r in range(len(world.settlements)):
				print("\n" + world.settlements[r].name)
				print("Race: " + world.races[world.settlements[r].raceID].name)
				print("Population: " + str(world.settlements[r].population))
				if(world.settlements[r].warTarget != None):
					print(red("At war with " + str(world.settlements[r].warTarget.name)))
				print("Coordinates: (" + str(world.settlements[r].x) + ", " + str(world.settlements[r].y) + ")")
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
							octaves = int(input("Enter a number of octaves (Suggested: 3 to 4): "))
							print("Generating...")
							world = World(width, height, 30, 20, sealevel, temperature, seed)
							world.generateMap()
							world.generatePerlinMap(octaves)
							world.generateBiomeMap(2)
							world.generateCities()
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
