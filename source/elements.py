import pygame
import random


class Bird:
	def __init__(self, screen_size, size=20, grav=0.8):
		self.x = screen_size[0]/5
		self.y = screen_size[1]/2
		self.color = (0, 222, 100)
		self.size = size
		self.scr_height = screen_size[1]

		self.grav = grav
		self.vel = 0

	def get_position(self):
		return self.x, self.y

	def move(self):
		self.vel += self.grav
		self.y += self.vel
		self.y = max(0, min(self.y, self.scr_height))

	def draw(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

	def jump(self):
		self.vel = -14



class Pipe:
	def __init__(self, screen_size, gap):
		self.screen_height = screen_size[1]
		self.x = screen_size[0]
		self.width = screen_size[0]/10
		self.speed = -5
		self.color = (100, 100, 100)
		self.gap = gap
		self.passed = False
		self.height = self.set_height()
		b_height = screen_size[1] - self.height - self.gap
		self.top = pygame.Rect(self.x, 0, self.width, self.height)
		self.bottom = pygame.Rect(self.x, self.height+self.gap, self.width, b_height)

	def set_height(self):
		return random.randint(self.gap//2, self.screen_height-1.5*self.gap)

	def move(self):
		self.x += self.speed
		self.top.move_ip(self.speed, 0)
		self.bottom.move_ip(self.speed, 0)

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.top)
		pygame.draw.rect(screen, self.color, self.bottom)

	def collide(self, bird):
		bx, by = bird.get_position()
		br = bird.size

		# top
		# rectangle (x, 0) - (x+width, heigth)
		xn = max(self.x, min(bx, self.x + self.width))
		yn = max(0, min(by, self.height))
		top_collide = ((xn - bx) ** 2) + ((yn - by) ** 2) <= (br ** 2)
		# print(f'top: {top_collide}')

		# bottom
		# rectangle (x, height+gap) - (x+width, screen_height)
		xn = max(self.x, min(bx, self.x + self.width))
		yn = max(self.height+self.gap, min(by, self.screen_height))
		bottom_collide = ((xn - bx) ** 2 + (yn - by) ** 2) <= (br ** 2)
		# print(f'bottom: {bottom_collide}')

		if bottom_collide or top_collide:
			return True

		return False
