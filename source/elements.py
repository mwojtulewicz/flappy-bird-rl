import pygame


class Bird:
	def __init__(self, screen_size, size=20, grav=0.8):
		self.x = screen_size[0]/5
		self.y = screen_size[1]/2
		self.color = (0, 222, 100)
		self.size = size

		self.grav = grav
		self.vel = 0

	def get_position(self):
		return self.x, self.y

	def move(self, screen_height):
		self.vel += self.grav
		self.y += self.vel
		self.y = max(0, min(self.y, screen_height))

	def draw(self, screen):
		self.move(screen.get_height())
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

	def jump(self):
		self.vel = -14


class Pipe:
	def __init__(self, screen_size, height):
		self.screen_height = screen_size[1]
		self.x = screen_size[0]
		self.width = screen_size[0]/10
		self.speed = -5
		self.color = (100, 100, 100)
		self.gap = screen_size[1]/5
		self.height = height

	def draw(self, screen):
		self.x += self.speed
		pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.height))
		pygame.draw.rect(screen, self.color, (self.x, self.height + self.gap, self.width, self.screen_height))

	def check_collision(self, bird):
		bx, by = bird.get_position()
		br = bird.size
