#	pyRoguelib - v.1.1
#   A Python Module based on PyGame for developing Roguelikes
# by Vinicius Castanheira (vncastanheira@gmail.com)
# 
# Created on: 11/09/2012
# Updated on: 12/09/2012


# Importing pyGam
import pygame
# For the use of "min()" function
from operator import attrgetter
# Self-explained
import random

# The pyRoguelib (alpha)

# Constants
# Define the kind of object occuping the 
# coordinate in the map
EMPTY = 0
ENEMY = 1
PLAYER = 2
WALL = 3
MINER = 4

# ----------------------------------------------------------------------------
#
# Tilemap Class
# Creates a squared-tiled system
# Methods:
#
# @ initialize, with arguments for the map and for the screen individualy
# @ blitImage, put a image with tile-size in the map and set a constant for it
# @ getSurface, returns the pygame display initialized
# @ isWalkable, check if a (x,y) is not a WALL
# @ generateRandomCave, transforms the map in a random cave of WALLs and EMPTYs
#                       Must be called first.
# @ semisen & semincos, simulates sin and cos for 90 degrees angles
#
# - Pathfinding Class:
#     Inside class for dealing with pathfinding only. Sorry for the mess.
#     For a TileMapping object, 'tilemap' for exemple, the call must be:
#     tilemap.Pathfinding.calculate(tupleStart, tupleGoal, tilemap)
#     Where:
#      - tupleStart & tupleGoal, python's tuple with 2 int arguments
#      - tilemap is the TileMapping object, passed for the function
#
# ----------------------------------------------------------------------------

class TileMapping:

	# Sets the display surface with given options
	# Stores the size of the tile (in pixels)
	def __init__(self, tilesize, mapSizeX, mapSizeY, screenSizeX, screenSizeY):
		self.display = pygame.display.set_mode((tilesize*screenSizeX,tilesize*screenSizeY))
		self.map = [ [WALL for x in range(mapSizeX)] for y in range(mapSizeY)]
		self.tilesize = tilesize
		self.screenWidth = tilesize*screenSizeX
		self.screenHeight = tilesize*screenSizeY
		self.mapWidth = mapSizeX
		self.mapHeight = mapSizeY

	# Blit a image on the display at (x,y) coordinate
	# Images are considered Surfaces by the PyGame
	def blitImage(self,image,x,y,blockype = EMPTY):
		self.display.blit(image,(x*self.tilesize,y*self.tilesize))
		self.map[x][y] = EMPTY

	def blitMap(self, image, scrollX=0, scrollY=0 ):
		for y in range(self.mapHeight):
			for x in range(self.mapWidth):
				if (self.map[x][y] == WALL):
					self.display.blit(image,((x+scrollX)*self.tilesize,(y+scrollY)*self.tilesize))

	# If the display that was initialized is needed
	# For other PyGame calls
	def getDisplay(self):
		return self.display

	# Check if the coordinate is walkable. 
	# A 'MINER' block is considered walkable, since it's only relevant for the generation algorithm
	def isWalkable(self,x,y):
		if( (x>=0 and x < self.mapWidth) and (y>=0 and y < self.mapHeight) and (self.map[x][y] != WALL) ):
			return True
		return False

	def generateRandomCave(self):
		# The first 5 lines creates a MINER in the center and other fours places:
		# Superior left, superior right, inferior left and inferior right
		# Thease locations guarantee a more expanded and open cave, althought 
		self.map[self.mapWidth//2][self.mapHeight//2] = MINER
		self.map[(self.mapWidth*3)//8][(self.mapWidth*3)//8] = MINER
		self.map[(self.mapWidth*5)//8][(self.mapWidth*5)//8] = MINER
		self.map[(self.mapWidth*3)//8][(self.mapWidth*5)//8] = MINER
		self.map[(self.mapWidth*5)//8][(self.mapWidth*3)//8] = MINER
		totalMiners = 5
		# Limits the number of miners created. The more miners, the bigger are the cave
		# This number can be modified depending on the size of the caves wanted
		while(totalMiners <= 1000):
			for y in range(self.mapHeight):
				for x in range(self.mapWidth):
					# Finds a MINER in the self.map array.
					# If a miner was found, two things can happen
					if(self.map[x][y] == MINER):
						direction = round(random.randint(0,3))
						angle = direction*90
						dx = self.semisen(angle)
						dy = self.semicos(angle)
						probability = round(random.randint(0,100))
						# If it's a valid location (not outside of boundaries), 
						# a new MINER is created at a random location
						if( ((x+dx) >= 0 and (x+dx) < self.mapWidth) and ((y+dy) >= 0 and (y+dy) < self.mapHeight) ):
							self.map[x+dx][y+dy] = MINER
							totalMiners += 1
							# If probability is bigger than 20%, the old MINER location is deleted
							# It controls the number of MINERs spawned 
							# The original ideia isis that the MINER should be moving 
							# with a random percentage of spawning another
							if(probability > 20):
								self.map[x][y] = EMPTY

	# Simulates the cos of square angles only (in degrees)
	def semicos(self,angle):
		if(angle == 0): return 1
		if(angle == 90): return 0
		if(angle == 180): return -1
		if(angle == 270): return 0

	# Simulates the sin of square angles only (in degrees)
	def semisen(self,angle):
		if(angle == 0): return 0
		if(angle == 90): return 1
		if(angle == 180): return 0
		if(angle == 270): return -1

	# Pathfinding Class A* based
	class Pathfinding:

		class Node:

			def __init__(self, x, y):
				self.x = x
				self.y = y
				self.connection = []
				self.costSoFar = 0
				self.estimatedLeftCost = 0
	
		# Heuristic function
		# Estimates the cost of the path
		# Prefers a more direct diagonal path
		def heuristic(current, parent, start, goal):
			dx1 = current.x - goal.x
			dy1 = current.y - goal.y
			dx2 = start.x - goal.x
			dy2 = start.y - goal.y
			cross = abs(dx1*dy2 - dx2*dy1)
			return (parent.estimatedLeftCost + cross*0.001)

		# Check if nodes are in the same (x,y) position
		def equals(a,b):
			if(a.x == b.x) and (a.y == b.y):
				return True
			return False

		# Simulates the cos of square angles only (in degrees)
		def semicos(angle):
			if(angle == 0): return 1
			if(angle == 90): return 0
			if(angle == 180): return -1
			if(angle == 270): return 0

		# Simulates the sin of square angles only (in degrees)
		def semisen(angle):
			if(angle == 0): return 0
			if(angle == 90): return 1
			if(angle == 180): return 0
			if(angle == 270): return -1

		# Get all possible nodes from a given node
		# TileMapping should be passed as second argument
		def getAdjacentNodes(parentNode,tilemap, start, goal):
			connections = []
			for i in range(4):
				newX = parentNode.x + tilemap.Pathfinding.semicos(i*90)
				newY = parentNode.y + tilemap.Pathfinding.semisen(i*90)
				# If the new location isn't a wall or is outside of the boundaries
				# Creates a new node, with everything setted
				# Contais all information needed
				if( (newX >= 0 and newX < tilemap.mapWidth) and (newY >= 0 and newY < tilemap.mapHeight) and tilemap.isWalkable(newX,newY)):
					newNode = tilemap.Pathfinding.Node(newX , newY)
					newNode.costSoFar = parentNode.costSoFar + 1
					# Estimates a heuristic for the node
					newNode.estimatedLeftCost = tilemap.Pathfinding.heuristic(newNode, parentNode, start, goal)
					for lastConnection in parentNode.connection:
						newNode.connection.append(lastConnection)
					newNode.connection.append(parentNode)
					connections.append(newNode)
			return connections

		# Loops the list in search for the node
		# True if was found, False otherwise
		def containsNode(node,sequence, tilemap):
			for item in sequence:
				# If the both nodes are in the same location
				if tilemap.Pathfinding.equals(node,item):
					return True
			return False

		# Tries to replace the node if have a better costSoFar
		def tryReplacingNode(node,sequence, tilemap):
			# Always finds, because 'containsNode' is
			# called before it
			for item in sequence:
				if tilemap.Pathfinding.equals(node,item):
					if(node.costSoFar < item.costSoFar):
						sequence.remove(item)
						return True
					else:
						return False
			return False

		# Gives priority to nodes with the minor 'estimatedLeftCost'
		# so they can be processed first and guarantee a better
		# (and pretty) path

		# The main function for pathfinding
		# Receives a Tuple data type as starting  point
		# Receives a Tuple data type as goal point
		# Receives a TileMapping Class

		def calculate(tupleStart, tupleGoal, tilemap):

			own = tilemap.Pathfinding
			start = own.Node(tupleStart[0],tupleStart[1])
			goal = own.Node(tupleGoal[0],tupleGoal[1])

			# Estimates the heurist for the start node
			start.estimatedLeftCost = own.heuristic(start, goal, start, goal)
			
			# Initializing the processed list as heap queue
			processedlist = []
			openlist = []

			# Start node on the heap
			openlist.append(start)

			# Goal boolean
			goalFound = False
			path = []

			# Here is the core of the algorithm
			# It will loop until it finds the goal or until the
			# entire map is scanned and no possible path is found

			while (len(openlist) > 0):
				# Takes the node from the openlist
				# NOTE: Heuristics values makes difference in this
				# 'pop' method.. The node with the less
				# 'estimatedCost' will be processed first
				current = min(openlist,key=attrgetter('estimatedLeftCost'))
				openlist.remove(current)
				#current = openlist.pop(0)

				# Break if the goal was found
				if(current.x == goal.x and current.y == goal.y):
					goalFound = True
					path = current.connection
					break

				# Return a array with all possible nodes that
				# connects the node 'current'
				adjacentNodes = own.getAdjacentNodes(current, tilemap, start, goal)
				
				# For each adjacent node, it's necessary to see if 
				for adjacent in adjacentNodes:			
					# Processes the adjacent nodeself.x, other.s, replacing if needed
					# If was found the same node in the processed list
					if(own.containsNode(adjacent,processedlist, tilemap)):
						if(own.tryReplacingNode(adjacent,processedlist, tilemap) == False):
							continue
					# If was found in the open list
					if(own.containsNode(adjacent,openlist, tilemap)):
						if(own.tryReplacingNode(adjacent,openlist, tilemap) == False):
							continue
					# Was found in one of the lists
					# Adjacent will replace the old node
					openlist.append(adjacent)

				# Current was processed
				processedlist.append(current)

			# All nodes processed.
			# If the goal was found, return the path
			# containing a list of 'Node's. Each node
			# have it's own coordinates and that will
			# be enought for now
			if(goalFound == True):
				return path
			else:
				return None

#	Why there is 'tilemap' everywhere:
#
#		Since we got a Class inside a Class, the first class must be referencied 
#	first for the program to know where the functions are coming from.
#	The problem is that, when the functions of the second Class call themselves, 
#	the long path with the first class (TileMapping.Pathfinding.function) must
# be written again and again, for each call. So, the TileMapping object is 
# passed as argument in every function. It's really a f***ing mess. 
# Could've been simple. It wasn't. At least, the final calls are simple.
