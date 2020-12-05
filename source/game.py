import pygame
import sys
from source.elements import Bird, Pipe

GRAVITY = 0.8
HEIGHT = 600
WIDTH = 800
NEXT_PIPE = 200

pygame.init()
screen = pygame.display.set_mode(size=(HEIGHT, WIDTH))
clock = pygame.time.Clock()

bird = Bird((HEIGHT, WIDTH), grav=GRAVITY)
pipe = Pipe((HEIGHT, WIDTH), 100)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird.jump()

	screen.fill((0, 0, 0))

	bird.draw(screen)
	pipe.draw(screen)

	pygame.display.update()
	clock.tick(60)
