import pygame
import sys
import time
from elements import Bird, Pipe
from agent import Agent
import matplotlib.pyplot as plt
import time

GRAVITY = 0.8
WIDTH = 600
HEIGHT = 800
NEXT_PIPE = 270
PIPE_GAP = 240

agent = Agent()


def draw_window(scr, bird, pipes):
	for pipe in pipes:
		pipe.draw(scr)
	bird.draw(scr)


def game(generations):
	pygame.init()
	screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	# bird = Bird((WIDTH, HEIGHT), grav=GRAVITY)
	# pipes = [Pipe((WIDTH, HEIGHT), PIPE_GAP)]
	#
	# alive = True
	# score = 0
	scores = []

	for n in range(generations):
		print(f"Game {n}")
		bird = Bird((WIDTH, HEIGHT), grav=GRAVITY)
		pipes = [Pipe((WIDTH, HEIGHT), PIPE_GAP)]
		alive = True
		score = 0

		while alive:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					agent.dump_qvalues(True)
					pygame.quit()
					sys.exit()

				# real player's input
				# if event.type == pygame.KEYDOWN:
				# 	if event.key == pygame.K_SPACE:
				# 		bird.jump()

			# agent action
			pc = [p.bottom for p in pipes if not p.passed][0]
			action = agent.act(bird.x, bird.y, bird.vel, pc)
			if action:
				bird.jump()

			screen.fill((0, 0, 0))

			# bird
			bird.move()

			if bird.y == screen.get_height():
				print('hit the ground')
				alive = False
			if bird.y == 0:
				print('hit the ceiling')
				alive = False

			# pipes
			for pipe in pipes:
				pipe.move()
				# collision
				if pipe.collide(bird):
					print(f"collision with pipe at x={pipe.x}")
					alive = False
				# passing
				if pipe.x + pipe.width < bird.x and not pipe.passed:
					pipe.passed = True
					score += 1
					print(f'passed, score: {score}')

			# returning reward to the agent
			agent.update_on_reward(alive)

			# generating next pipe (if last pipe is far enough)
			if screen.get_width() - pipes[-1].x >= NEXT_PIPE:
				pipes.append(Pipe((WIDTH, HEIGHT), PIPE_GAP))
			# removing first pipe if its out of the window
			if pipes[0].x < -pipes[0].width:
				pipes.pop(0)

			draw_window(screen, bird, pipes)

			pygame.display.update()
			# clock.tick(200)

		screen.fill((0, 0, 0))
		print(f" -- score: {score}\n")
		scores.append(score)
		# time.sleep(0.1)
	
	# falling animation
	# bird.vel = 0
	# while bird.y < HEIGHT:
	# 	bird.move()
	# 	screen.fill((0, 0, 0))
	# 	draw_window(screen, bird, pipes)
	# 	pygame.display.update()
	# 	clock.tick(60)

	agent.dump_qvalues(True)
	return scores


if __name__ == '__main__':
	print('\nLearning starts...')
	ag_scores = game(5000)
	plt.plot(ag_scores)
	print(f'best score after learning: {max(ag_scores)}')
