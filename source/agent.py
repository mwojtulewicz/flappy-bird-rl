import random
import json


class Agent:

	def __init__(self):
		# Q algorithm parameters
		self.discount = 1.0
		self.lr = 0.7
		self.eps = 0.1
		self.decay_rate = 0.9
		self.reward = {"alive": 0, "dead": -1000}

		# Q Learning initialization
		self.load_qvalues()
		self.init_state("0_0_0")
		self.history = {
			"prev": ("0_0_0", 0),
			"curr": ("0_0_0", 0)
		}
		# self.moves = []

	def load_qvalues(self):
		# load q values from a JSON
		self.qvalues = {}
		try:
			fil = open("qvalues.json", "r")
		except IOError:
			return
		self.qvalues = json.load(fil)
		fil.close()

	def act(self, x, y, vel, pipe):
		"""
		params x,y,vel,pipe as in self.get_state
		:return: action (1 for flap)
		"""
		state = self.get_state(x, y, vel, pipe)

		# action
		if random.random() > self.eps:
			action = 0 if self.qvalues[state][0] >= self.qvalues[state][1] else 1
		else:
			action = int(random.uniform(0, 1))

		self.history["prev"] = self.history["curr"]
		self.history["curr"] = (state, action)

		return action

	def get_state(self, x, y, vel, pipe):
		"""
		:param x: coordinate x of a player
		:param y: coordinate y of a player
		:param vel: player's velocity
		:param pipe: closest pipe (bottom pygame.Rect)
		:return: state as a formatted string

		state string format: 'x0_y0_v'
			x0: player's x difference to a pipe
			y0: player's y difference to a pipe
			v: current player's velocity
		"""

		x0 = max(pipe.x - x, 0)
		y0 = pipe.y - y

		# dividing the state space
		
		# x0
		if x0 < 50:
			x0 = int(x0) - (int(x0) % 2)
		elif x0 < 200:
			x0 = int(x0) - (int(x0) % 10)
		else:
			x0 = int(x0) - (int(x0) % 50)

		# y0
		if -200 < y0 < 200:
			y0 = int(y0) - (int(y0) % 10)
		else:
			y0 = int(y0) - (int(y0) % 50)

		# information if its going up or down
		vel = int(vel < 0)

		state = str(int(x0)) + '_' + str(int(y0)) + '_' + str(int(vel))
		self.init_state(state)

		return state

	def init_state(self, state):
		if self.qvalues.get(state) is None:
			self.qvalues[state] = [0, 0]

	def update_on_reward(self, alive=True):
		r = self.reward["alive"] if alive else self.reward["dead"]
		s, a = self.history["prev"]
		s_, a_ = self.history["curr"]

		# Q Learning algorithm
		self.qvalues[s][a] = (1 - self.lr)*self.qvalues[s][a] + self.lr*(r + self.discount*max(self.qvalues[s_]))

	def decay_eps(self):
		self.eps *= self.decay_rate

	def dump_qvalues(self, force=False):
		print("Saving Q-Table\n")
		if force:
			fil = open("qvalues.json", "w")
			json.dump(self.qvalues, fil)
			fil.close()
