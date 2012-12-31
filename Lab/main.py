from pygame import *
import pygame._view
import sys
import math
import entity

SCREEN = (400, 400) # Resolution
FPS = 30

class Main:

	def __init__(self, SCREEN):
		# Initiate pygame and display.
		init()
		display.init()
		# Create fps and set main display.
		self.fpsClock = time.Clock()
		self.mainDisplay = display.set_mode(SCREEN)
		size = 32
		tile1 = entity.Static(50, 300, size, size)
		tile2 = entity.Static(50+size, 300, size, size)
		tile3 = entity.Static(50+(2*size), 300, size, size)
		tile4 = entity.Static(50+(3*size), 300, size, size)
		tile5 = entity.Static(50+(4*size), 300-size, size,size)
		self.tileGroup = sprite.Group()
		self.tileGroup.add(tile1)
		self.tileGroup.add(tile2)
		self.tileGroup.add(tile3)
		self.tileGroup.add(tile4)
		self.tileGroup.add(tile5)

		self.boxGroup = sprite.Group()

		self.goHorizontal = 0

	# All events from mouse/keyboard/gamepad?
	def playerEvent(self):
		for eventput in event.get():
			if eventput.type == KEYDOWN and eventput.key == K_ESCAPE:
				return 'QUIT'
			(l, m, r) = mouse.get_pressed()
			if l:
				(x, y) = mouse.get_pos()
				box = entity.Movable(x, y, 16, 16)
				self.boxGroup.add(box)

			if eventput.type == KEYDOWN and eventput.key == K_a:
				self.boxGroup.empty()

			if eventput.type == KEYDOWN and eventput.key == K_RIGHT:
				self.goHorizontal += 3
			if eventput.type == KEYDOWN and eventput.key == K_LEFT:
				self.goHorizontal -= 3

			

	# Updates variables
	def update(self):
		for box in self.boxGroup:
			box.motion(self.tileGroup, self.goHorizontal)

	# Draws to the screen when finished
	def draw(self):
		self.mainDisplay.fill((0,0,0))
		for tile in self.tileGroup:
			draw.rect(self.mainDisplay, (0,0,255), tile.rect)
		for box in self.boxGroup:
			draw.rect(self.mainDisplay, (175, 0, 0), box.rect)


	# Main loop. Everything in order.
	def loop(self,FPS):
		while True:
			if (self.playerEvent() == 'QUIT'):
				quit()
				sys.exit()

			self.update()
			self.draw()
			display.update()
			self.fpsClock.tick(FPS)


main = Main(SCREEN) # Creates the Main Class with SCREEN
main.loop(FPS) # Loops with n FPS