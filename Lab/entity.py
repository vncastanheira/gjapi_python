import pygame
import pyganim

# Entities of the game, objects containing sprites and a collision area
class Entity(pygame.sprite.Sprite):
	def __init__(self, x, y, width=1, height=1):
		# All sprite classes should extend pygame.sprite.Sprite.
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect((x, y), (width, height))
		# A dictionay of animations. It contains:
		# - the key, a string of the name
		# - the value, a Pyganim object
		self.animation = {}

	# Adds an animation on the dictionary
	def addAnimation(self, name, imageTuple):
		self.animation[name] = pyganim.PygAnimation([(frame, 0.2) for frame in imageTuple])

	# Play the animation with the given name to a pygame surface
	def playAnimation(self, name, surface):
		self.adjustRect(self.animation[name])
		self.animation[name].play()
		self.animation[name].blit(surface, (self.rect.x,self.rect.y))

	# Stop the animation with the given name to a pygame surface
	def stopAnimation(self, name, surface):
		self.adjustRect(self.animation[name])
		self.animation[name].getRect(self.rect.x, self.rect.y)
		self.animation[name].stop()
		self.animation[name].blit(surface, (self.rect.x,self.rect.y))

	# Flip all animations, on the horizontal side
	def flip(self):
		for key, value in self.animation.items():
			value.flip(True, False)

	# Function for ajusting the 'rect' area for new
	# animation sprites, setting them on the right position
	# and fixing bad position glitches
	def adjustRect(self, animation):
		newRect = animation.getRect(self.rect.x, self.rect.y)
		diff_width = self.rect.width - newRect.width
		diff_height = self.rect.height - newRect.height
		self.rect = newRect
		self.rect.x, self.rect.y += diff_width, diff_height

#--------------------------------------------------------

# Entities that remains at a single place in the map
# Used for ground and map in general
class Static(Entity):
	def __init__(self, x, y, width=0, height=0):
		super(Static, self).__init__(x, y, width, height)

#--------------------------------------------------------

# Entities that move around the map
# They are affected by gravity
class Movable(Entity):
	def __init__(self, x, y, width=0, height=0):
		super(Movable, self).__init__(x, y, width, height)
		self.vVelocity, self.hVelocity = 0
		self.gravity = 9
		self.onGround = False

	# Moves the object to x and y pixels from it's coordinate
	# Also handles collision?
	def motion(self, entityGroup, x_pixels=0):
		self.rect = self.rect.move(x_pixels, 0.98)
		# Conditions to be in the air
		if not self.onGround:
			if self.vVelocity < 9: 
				self.vVelocity += 0.98
			self.rect = self.rect.move(0, self.vVelocity)
		# Checky collision with entities of the entityGroup
		justCollide = False
		for entity in entityGroup:
			# True collision
			if pygame.sprite.collide_rect(self, entity):
				self.fixCollision(entity)
				justCollide = True

		if not justCollide:
			self.onGround = False

	# This method is a tedius checking for proper collsion behavior (almost)
	# Comparing tons of edges of two rectangular area of objects, assuming 
	# they are overlaping in an unknow position, this method discovers where it
	# is overlaping, how much (in pixels) and separate them, because they are
	# solid and cannot be in the same place.
	def fixCollision(self, other):
		# Comparisons of bot and top positions of each
		# element to each other
		top_to_top = self.rect.top - other.rect.top
		top_to_bot = self.rect.top - other.rect.bottom
		bot_to_top = self.rect.bottom - other.rect.top
		bot_to_bot = self.rect.bottom- other.rect.bottom
		# Collision of self on top of other
		if top_to_top < 0 and top_to_bot < 0 and bot_to_top > 0 and bot_to_bot < 0:
			self.rect = self.rect.move(0, -bot_to_top)
			self.onGround = True # The object is on top of the other
			self.vVelocity = 0.98 # Tricky velocity, to keep checking collision and granting that it
			# falls to the ground if no longer above other object
			return
		# Collision of self on bot of other
		if top_to_top > 0 and top_to_bot < 0 and bot_to_top > 0 and bot_to_bot > 0:
			self.rect = self.rect.move(0, -top_to_bot)
			return

		# Comparisons of right and left positions of each
		# element to each other
		right_to_right = self.rect.right - other.rect.right 
		right_to_left = self.rect.right - other.rect.left
		left_to_right = self.rect.left - other.rect.right
		left_to_left = self.rect.left - other.rect.left
		# Collision of self on right of other
		if left_to_left < 0 and left_to_right < 0 and right_to_right < 0 and right_to_left > 0:
			self.rect = self.rect.move(-right_to_left, 0)
		# Collision of self on left of other
		if left_to_left > 0 and left_to_right < 0 and right_to_right > 0 and right_to_left > 0:
			self.rect = self.rect.move(-left_to_right, 0)
