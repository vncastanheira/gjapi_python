import pygame, sys
from tilemap import *

FPS = 30

fpsClock = pygame.time.Clock()

pygame.display.init()
tilemap = TileMapping(8,50,50,100,50)
tilemap.generateRandomCave()

start = pygame.image.load("start.png")
goal = pygame.image.load("goal.png")
wallImg = pygame.image.load("blocky.png")
point = pygame.image.load("point.png")

pathList = tilemap.Pathfinding.calculate(((tilemap.mapWidth*3)//8,(tilemap.mapWidth*3)//8),((tilemap.mapWidth*5)//8,(tilemap.mapWidth*5)//8),tilemap)

camera = {'x': 0 , 'y': 0}

while True:
	tilemap.getDisplay().fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				camera['y'] -= 1
			elif event.key == pygame.K_DOWN:
				camera['y'] += 1
			elif event.key == pygame.K_RIGHT:
				camera['x'] += 1
			elif event.key == pygame.K_LEFT:
				camera['x'] -= 1
		
	if(pathList != None):
		for node in pathList:
			print(node," H:",node.estimatedLeftCost)
			tilemap.blitImage(point, node.x+camera['x'], node.y+camera['y'])
	tilemap.blitImage(start,((tilemap.mapWidth*3)//8)+camera['x'],((tilemap.mapWidth*3)//8)+camera['y'])
	tilemap.blitImage(goal,((tilemap.mapWidth*5)//8)+camera['x'],((tilemap.mapWidth*5)//8)+camera['y'])
	tilemap.blitMap(wallImg,camera['x'],camera['y'])

	pygame.display.update()
	fpsClock.tick(FPS)


