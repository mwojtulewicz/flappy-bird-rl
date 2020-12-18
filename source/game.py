import pygame
import sys
import time
from elements import Bird, Pipe

GRAVITY = 0.8
WIDTH = 600
HEIGHT = 800
NEXT_PIPE = 500
PIPE_GAP = 180


def draw_window(scr, bird, pipes):
	for pipe in pipes:
		pipe.draw(scr)
	bird.draw(scr)


def game():
	pygame.init()
	screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	bird = Bird((WIDTH, HEIGHT), grav=GRAVITY)
	pipes = [Pipe((WIDTH, HEIGHT), PIPE_GAP)]

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
			run = False
		if bird.y == 0:
			print('hit the ceiling')
			run = False

		# pipes
		for pipe in pipes:
			pipe.move()
			# collision
			if pipe.collide(bird):
				print(f"collision with pipe at x={pipe.x}")
				run = False
			# passing
			if pipe.x + pipe.width < bird.x and not pipe.passed:
				pipe.passed = True
				score += 1
				print(f'passed, score: {score}')

		# generating next pipe (if last pipe is far enough)
		if screen.get_width() - pipes[-1].x >= NEXT_PIPE:
			pipes.append(Pipe((WIDTH, HEIGHT), PIPE_GAP))
		# removing first pipe if its out of the window
		if pipes[0].x < -pipes[0].width:
			pipes.pop(0)

		draw_window(screen, bird, pipes)

		pygame.display.update()
		clock.tick(60)
	
	# falling animation
	bird.vel = 0
	while bird.y < HEIGHT:
		bird.move()
		screen.fill((0, 0, 0))
		draw_window(screen, bird, pipes)
		pygame.display.update()
		clock.tick(60)

	return score


if __name__ == '__main__':
	print('\nGame starts...')
	score = game()
	print(f'\nGAME OVER \n -- final score: {score}')
