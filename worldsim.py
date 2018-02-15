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
		self.newraces = [Race("Skerran", "Avian")]
		self.year = 1
		self.name = random.choice(self.worldprefixes) + random.choice(self.worldsuffixes)
		self.empires = [Empire(0, "Skerran", self.newraces[0], random.randrange(7, 10), "F", 45, 226), Empire(1, "Ravakan", self.newraces[0], random.randrange(7, 10), "P", 60, 196), Empire(2, "Ahn'litend", self.newraces[0], random.randrange(7, 10), "F", 245, 129), Empire(3, "Ixx'ra Swarm", self.newraces[0], random.randrange(6, 10), "A", 245, 52), Empire(4, "Orkathi", self.newraces[0], random.randrange(7, 10), "P", 245, 214)]
		self.settlements = []
	def generateMap(self):
		for x in range(0, self.width):
			self.tiles.append([])
			for y in range(0, self.height):
				index = random.randrange(0, len(self.tileTypes) - 1)
				self.tiles[x].append(Tile(x + y, x, y, "~", 0, random.randrange(1, self.lushness), random.randrange(1, self.richness)))
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
						biome += random.randrange(30, 120)
					elif(y >= self.height - 10):
						biome -= random.randrange(80, 120)
					elif(y < 10):
						biome -= random.randrange(80, 120)
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
		for r in range(len(self.empires)):
			spawned = 0
			numSuitableTiles = 0
			suitableTiles = []
			for x1 in range(len(self.tiles)):
				for y1 in range(len(self.tiles[x1])):
					if(self.tiles[x1][y1].type != "~" and self.tiles[x1][y1].type != "^"):
						numSuitableTiles += 1
						suitableTiles.append(self.tiles[x1][y1])
			if(len(suitableTiles) == 0):
				continue
			else:
				originTile = random.choice(suitableTiles)
				
			while(spawned < self.empires[r].population):
				tile = random.choice(random.choice(self.tiles))
				x = next((i for i, sublist in enumerate(self.tiles) if tile in sublist), -1)
				y = self.tiles[x].index(tile)
				if(self.getDistance(x, y, originTile.x, originTile.y) <= 7 and tile.type != "~" and tile.type != "^"):
					tile.settlement = Settlement(x, y, random.choice(self.empires[r].citynames), "%", random.randrange(150, 300), r)
					tile.color = ""
					tile.colorX = self.empires[r].color
					tile.settlement.controller = self.empires[r]
					self.settlements.append(tile.settlement)
					spawned += 1
	
	def generateEmpires(self, numEmpires, numRaces):
		self.empires = []
		self.newraces = []
		for i in range(numRaces):
			race = Race("Human", "Humanoid")
			race.randomize()
			self.newraces.append(race)
		for r in range (numEmpires):
			race = Empire(r, "Human", random.choice(self.newraces), 1, "F", 70, 1)
			race.random()
			self.empires.append(race)
	
	def getDistance(self, x1, y1, x2, y2):
		dist = math.hypot(x2 - x1, y2 - y1)
		return dist
	def getEmpireDistance(self, e1, e2):
		dists = [999999999]
		for i in range(len(self.settlements)):
			if(self.settlements[i].controller == e1):
				for i2 in range(len(self.settlements)):
					if(self.settlements[i2].controller == e2):
						dist = math.hypot(self.settlements[i].x - self.settlements[i2].x, self.settlements[i].y - self.settlements[i2].y)
						dists.append(dist)
						continue
		return min(dists)
	
	def doTick(self, ticks):
		for i in range(ticks):
			self.history = ""
			for r2 in range(len(self.empires)):
				race = self.empires[r2]
				if(self.empires[r2].population <= 0):
					self.history += str(self.year) + ": The " + race.name + " have been completely purged by their enemies\n"
				for r3 in range(len(self.empires)):
					if(self.getEmpireDistance(self.empires[r2], self.empires[r3]) <= 25 and self.empires[r2].population > self.empires[r3].population and random.randrange(1, 100) <= 3):
						self.empires[r2].warTarget = self.empires[r3]
						self.empires[r3].warTarget = self.empires[r2]
						self.history += str(self.year) + ": The " + self.empires[r2].name + " declared war on the " + self.empires[r3].name
					else:
						continue
						
			self.year += 1
			for r in range(len(self.settlements)):
				if(self.settlements[r].controller.warTarget != None):
					for c in range(len(self.settlements)):
						dists = []
						settlements = []
					
						dist = math.hypot(self.settlements[r].x - self.settlements[c].x, self.settlements[r].y - self.settlements[c].y)
						dists.append(dist)
						settlements.append(self.settlements[c])
						dist = min(dists)
						if(self.settlements[c].controller == self.settlements[r].controller.warTarget):
							declarer = self.empires[self.settlements[r].raceID]
							defender = settlements[dists.index(dist)]
							self.settlements[r].warTarget = defender
							defender.warTarget = self.settlements[r]
				if(self.settlements[r].warTarget != None):
					warTarget = self.settlements[r].warTarget
					self.settlements[r].population -= int(self.settlements[r].warTarget.population * 0.03)
					if(self.settlements[r].population < 100):
						self.tiles[self.settlements[r].x][self.settlements[r].y].colorX = self.empires[warTarget.raceID].color
						self.settlements[r].warTarget = None
						self.settlements[r].raceID = warTarget.raceID
						self.settlements[r].warTarget = None
						self.settlements[r].population = 100
						self.settlements[r].controller.population -= 1
						warTarget.controller.population += 1
				tile = self.tiles[self.settlements[r].x][self.settlements[r].y]
				if(self.settlements[r].population <= 5000 and self.settlements[r].warTarget == None):
					self.settlements[r].population += (self.settlements[r].population) * 0.05
				self.settlements[r].wealth += random.randrange(25, 100)
				if(self.settlements[r].population >= 1600 and self.settlements[r].controller.warTarget == None and random.randrange(1, 100) <= 25):
					isSpawned = "NONE"
					while(isSpawned == "NONE"):
						tile2 = random.choice(random.choice(self.tiles))
						if(tile2.biome == self.empires[self.settlements[r].raceID].biomePref):
							x = next((i for i, sublist in enumerate(self.tiles) if tile2 in sublist), -1)
							y = self.tiles[x].index(tile2)
							dist = math.hypot(self.settlements[r].x - x, self.settlements[r].y - y)
							if(dist <= 15):
								tile2.settlement = Settlement(x, y, random.choice(self.empires[self.settlements[r].raceID].citynames), "%", 500, self.settlements[r].raceID)
								tile2.color = ""
								tile2.colorX = self.empires[self.settlements[r].raceID].color
								self.settlements.append(tile2.settlement)
								isSpawned = True
								self.settlements[r].population -= int(self.settlements[r].population / 3)
								self.empires[self.settlements[r].raceID].population += 1
								self.history += str(self.year) + ": the " + self.empires[self.settlements[r].raceID].name + " city of " + self.settlements[r].name + " settled a new city called " + tile2.settlement.name + "\n"
					isSpawned = "NONE"
					continue
				
				
class Tile:
	def __init__(self, id, x, y, type, elevation, food, metals):
		self.id = id
		self.type = type
		self.food = food
		self.metals = metals
		self.elevation = elevation
		self.color = 7
		self.biome = "B"
		self.settlement = None
		self.x = x
		self.y = y
class Empire:
	global world
	def __init__(self, id, name, type, population, biomePref, lifeSpan, color):
		self.id = id
		self.name = name
		self.type = type
		self.population = population
		self.biomePref = biomePref
		self.lifeSpan = lifeSpan
		self.color = color
		self.warTarget = None
		with open(os.getcwd() + "\\data\\names\\cities\\" + self.type.namelist + ".txt", "r+") as f:
			self.citynames = f.readlines()
		for i in range(len(self.citynames)):
			self.citynames[i] = self.citynames[i].strip("\n")
	def random(self):
		self.type = random.choice(world.newraces)
		self.name = random.choice(self.type.citynames)
		self.population = random.randrange(5, 32)
		self.lifeSpan = random.randrange(20, 200)
		self.biomePref = random.choice(["A", "T", "F", "F", "P", "P", "J", "D"])
		self.color = random.randrange(17, 229)
		if(self.population >= 25):
			self.name += random.choice([" Empire", " Glorious Empire", " Holy Empire", " Great Horde", " Kingdoms"])
		elif(self.population >= 15):
			self.name += random.choice([" Kingdom", " Horde", " Republic"])
		else:
			self.name += random.choice([" Clans", " Tribes", " Nomads", " Council", " City-States"])

class Race:
	def __init__(self, name, type):
		self.name = name
		self.type = type
		self.namelist = "avian"
		
	def randomize(self):
		if(self.type == "Machine"):
			self.namelist = "robot"
		else:
			self.namelist = random.choice(["avian", "insectoid", "reptile"])
		with open(os.getcwd() + "\\data\\names\\cities\\" + self.namelist + ".txt", "r+") as f:
			self.citynames = f.readlines()
		for i in range(len(self.citynames)):
			self.citynames[i] = self.citynames[i].strip("\n")
		self.name = random.choice(self.citynames).strip("\n")

class Settlement:
	global world
	def __init__(self, x, y, name, type, population, raceID):
		self.x = x
		self.y = y
		self.name = name.strip("\n")
		self.type = type
		self.population = population
		self.raceID = raceID
		self.controller = world.empires[self.raceID]
		self.development = 1
		self.wealth = 100
		self.warTarget = None

def drawTable(data):
	for i, d in enumerate(data):
		line = '|'.join(str(x).ljust(22) for x in d)
		print(line)
		if i == 0:
			print('-' * (len(line) - 19))

		
global world
world = World(117, 50, 5, 8, 120, 0, None)
print("Generating...")
world.generateMap()
print("Generating heightmap...")
world.generatePerlinMap(3)
print("Generating biomes...")
world.generateBiomeMap(3)
print("Uplifting sapient life...")
world.generateEmpires(random.randrange(3, 5), random.randrange(1, 3))
print("Building cities...")
world.generateCities()

def clearScreen():
	os.system("cls")


def sim():
	global world
	while True:
		clearScreen()
		world.printBiomeMap()
		print("\nCOMMANDS: run cities empires back")
		inp = input(">: ")
		if(inp == "run"):
			try:
				ticks = int(input("Enter the number of ticks to run: "))
				ticks2 = int(input("Enter the number of years per tick: "))
				yearsDone = 0
				starttime=time.time()
				while (yearsDone < ticks):
					world.doTick(ticks2)
					clearScreen()
					world.printBiomeMap()
					print(world.name + ", in the year " + str(world.year))
					yearsDone += 1
					with open(os.getcwd() + "\\histories\\" + world.name + ".txt", "a+") as f:
						f.write(world.history)
						f.close()
					time.sleep(4.0 - ((time.time() - starttime) % 4.0))
			except ValueError as e:
				print("Please enter the numbers of years and ticks as numbers!")
				print(e)
				time.sleep(7)	
		elif(inp == "cities"):
			clearScreen()
			data = []
			titles = ["Name", "Empire", "Population", "Fighting", "Coordinates"]
			names = []
			empires = []
			pops = []
			warTargets = []
			numbers = []
			coords = []
			for r in range(len(world.settlements)):
				names.append(world.settlements[r].name.strip("\n"))
				empires.append(world.empires[world.settlements[r].raceID].name)
				pops.append(str(math.floor(world.settlements[r].population)))
				if(world.settlements[r].warTarget != None):
					warTargets.append(str(world.settlements[r].warTarget.name.strip("\n")))
				else:
					warTargets.append("Nobody")
				coords.append("(" + str(world.settlements[r].x) + ", " + str(world.settlements[r].y) + ")")
				numbers.append(str(r + 1))
				data = [titles] + list(zip(names, empires, pops, warTargets, coords, numbers))
			drawTable(data)
			input("PRESS ENTER TO CONTINUE")
		elif(inp == "empires"):
			clearScreen()
			data = []
			titles = ["Name", "Race", "At war with", "Lifespan", "Cities", "Map Color"]
			names = []
			types = []
			fighting = []
			lifeSpans = []
			colors = []
			pops = []
			for r in range(len(world.empires)):
				names.append(world.empires[r].name)
				types.append(world.empires[r].type.name)
				if(world.empires[r].warTarget != None):
					fighting.append(world.empires[r].warTarget.name)
				else:
					fighting.append("Nobody")
				lifeSpans.append(world.empires[r].lifeSpan)
				colors.append(color("%", world.empires[r].color))
				pops.append(world.empires[r].population)
				data = [titles] + list(zip(names, types, fighting, lifeSpans, pops, colors))
			drawTable(data)
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
		print("COMMANDS: map sim help")
		inp = input(">: ")
		if(inp == "sim"):
			sim()
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
							numRaces = int(input("Enter a number of sapient races (Suggested: 1-3: "))
							numEmpires = int(input("Enter a number of empires (Suggested: 2-12): "))
							octaves = int(input("Enter a number of octaves (Suggested: 3 to 4): "))
							print("Generating...")
							world = World(width, height, 30, 20, sealevel, temperature, seed)
							world.generateMap()
							world.generatePerlinMap(octaves)
							world.generateBiomeMap(3)
							world.generateEmpires(numEmpires, numRaces)
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
			print("COMMANDS: empires map sim help")
			
			
game()
