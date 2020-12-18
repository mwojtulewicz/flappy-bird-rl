import pygame
import sys
from elements import Bird, Pipe

GRAVITY = 0.8
HEIGHT = 600
WIDTH = 800
NEXT_PIPE = 500
PIPE_GAP = 180


def draw_window(scr, bird, pipes):
	bird.draw(scr)
	for pipe in pipes:
		pipe.draw(scr)


def main():
	pygame.init()
	screen = pygame.display.set_mode(size=(HEIGHT, WIDTH))
	clock = pygame.time.Clock()

	bird = Bird((HEIGHT, WIDTH), grav=GRAVITY)
	pipes = [Pipe((HEIGHT, WIDTH), PIPE_GAP)]

	run = True
	score = 0

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.jump()

		screen.fill((0, 0, 0))

		# bird
		bird.move()

		if bird.y == screen.get_height():
			print('hit the ground')
		if bird.y == 0:
			print('hit the ceiling')

		# pipes
		for pipe in pipes:
			pipe.move()
			# collision
			if pipe.collide(bird):
				print(f"collision with pipe at x={pipe.x}")
			# passing
			if pipe.x + pipe.width < bird.x and not pipe.passed:
				pipe.passed = True
				score += 1
				print(f'passed, score: {score}')

		# generating next pipe (if last pipe is far enough)
		if screen.get_width() - pipes[-1].x >= NEXT_PIPE:
			pipes.append(Pipe((HEIGHT, WIDTH), PIPE_GAP))
		# removing first pipe if its out of the window
		if pipes[0].x < -pipes[0].width:
			pipes.pop(0)

		draw_window(screen, bird, pipes)

		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
