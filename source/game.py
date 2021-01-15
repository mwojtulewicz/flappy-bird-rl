import pygame
import sys
import time
from elements import Bird, Pipe
from agent import Agent
import matplotlib.pyplot as plt
import time
import numpy as np

GRAVITY = 0.8
WIDTH = 600
HEIGHT = 800
NEXT_PIPE = 300
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
		# restarting game
		bird = Bird((WIDTH, HEIGHT), grav=GRAVITY)
		pipes = [Pipe((WIDTH, HEIGHT), PIPE_GAP)]
		alive = True
		score = 0

		# game loop
		while alive:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					agent.dump_qvalues(True)
					return scores
					agent.dump_qvalues(True)
					plt.plot(scores)
					plt.show()
					pygame.quit()
					sys.exit()

				# real player's input
				# if event.type == pygame.KEYDOWN:
				# 	if event.key == pygame.K_SPACE:
				# 		bird.jump()

			# agent's action
			pc = [p.bottom for p in pipes if not p.passed][0]
			action = agent.act(bird.x, bird.y, bird.vel, pc)
			if action:
				bird.jump()

			# bird 
			# movement
			bird.move()
			# collinsions with ground and top
			if bird.y == screen.get_height():
				alive = False
			if bird.y == 0:
				alive = False

			# pipes
			for pipe in pipes:
				pipe.move()
				# collision
				if pipe.collide(bird):
					alive = False
				# passing
				if pipe.x + pipe.width < bird.x and not pipe.passed:
					pipe.passed = True
					score += 1

			# returning a reward to the agent
			agent.update_on_reward(alive)

			# generating next pipe (if last pipe is far enough)
			if screen.get_width() - pipes[-1].x >= NEXT_PIPE:
				pipes.append(Pipe((WIDTH, HEIGHT), PIPE_GAP))
			# removing first pipe if its out of the window
			if pipes[0].x < -pipes[0].width:
				pipes.pop(0)

			# display
			# clear background
			screen.fill((0, 0, 0))
			# drawinq game elements
			draw_window(screen, bird, pipes)

			pygame.display.update()
			# clock.tick(200)

			# terminate game if the agent can't die :))
			# note: without penalizing him with a -1000 reward for dying
			if(score > 10000):
				alive = False

		# score saving
		print(f"Game {n} final score {score}")
		scores.append(score)

		# exponentialy decaying agents epsilon (probability to act randomly - explore)
		agent.decay_eps()
		
		# time.sleep(0.1)
	
	# falling animation
	# bird.vel = 0
	# while bird.y < HEIGHT:
	# 	bird.move()
	# 	screen.fill((0, 0, 0))
	# 	draw_window(screen, bird, pipes)
	# 	pygame.display.update()
	# 	clock.tick(60)

	# saving qvalues to json file
	agent.dump_qvalues(True)
	return scores


if __name__ == '__main__':
	print('\nLearning starts...')
	
	scores = game(5000)
	np.savetxt("scores.csv", np.asarray(scores, dtype=np.int64), delimiter=";")
	plt.plot(scores)
	plt.savefig("scores.png")
	
	print(f'best score after learning: {max(scores)}')
