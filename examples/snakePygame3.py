import pygame
import random

class Cube(object):
	rows = 20
	size = 500
	def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
		self.pos = start
		self.color = color
		self.dirnx = dirnx
		self.dirny = dirny

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self, window):
		distance_btn = self.size // self.rows
		i_x = self.pos[0]
		j_y = self.pos[1]

		posDraw = (distance_btn*i_x+1, distance_btn*j_y+1, distance_btn-1, distance_btn-1)
		pygame.draw.rect(window, self.color, posDraw)


class Snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		self.head = Cube(pos)
		self.body.append(self.head)

		self.dirnx = 1
		self.dirny = 0

	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			keys = pygame.key.get_pressed()

			for key in keys:

				if keys[ pygame.K_LEFT ]:
					self.dirnx = -1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				if keys[ pygame.K_RIGHT ]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				if keys[ pygame.K_UP ]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				if keys[ pygame.K_DOWN ]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			pp = c.pos[:]
			if pp in self.turns:
				turn = self.turns[pp]
				c.move(turn[0], turn[1])
				if i == len(self.body) - 1:
					self.turns.pop(pp)
			else:
				if c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
				elif c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows - 1:c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
				else: c.move(c.dirnx, c.dirny)

	def draw(self, window):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(window)
			else:
				c.draw(window)

	def addCube(self):
		tail = self.body[-1]
		tail_dirnx, tail_dirny = tail.dirnx, tail.dirny



		if tail_dirnx == 1 and tail_dirny == 0:
			self.body.append(Cube((tail.pos[0] - 1, tail.pos[1]))) 
		elif tail_dirnx == -1 and tail_dirny == 0:
			self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
		elif tail_dirnx == 0 and tail_dirny == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
		elif tail_dirnx == 0 and tail_dirny == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

		self.body[-1].dirnx = tail_dirnx
		self.body[-1].dirny = tail_dirny
 

class MainLoop():
	def __init__(self):
		self.rows = 20
		self.size = 500
		self.snake = Snake((0,255,0), (5,5))
		self.randCube = Cube(self.randomCube(self.snake) ,color=(0,0,255))

	def randomCube(self, item):
		positions = item.body
		while True:
			x = random.randrange(self.rows)
			y = random.randrange(self.rows)

			if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
				continue
			else:
				break
		return (x, y)


	def drawGrid(self, window, size, rows):
		sizeBtn = size // rows
		x = 0
		y = 0
		for i in range(rows):
			x += sizeBtn
			y += sizeBtn
			pygame.draw.line(window, (255,255,255), (x, 0), (x, size))
			pygame.draw.line(window, (255,255,255), (0, y), (size, y))

	def redraw(self, window):
		window.fill((0,0,0))
		self.drawGrid(window, self.size, self.rows)
		self.snake.draw(window)
		self.randCube.draw(window)
		pygame.display.update()	

	def main(self):

		window = pygame.display.set_mode((self.size, self.size))

		play = True
		clock = pygame.time.Clock()
		while play:
			pygame.time.delay(50)
			clock.tick(10)

			if self.snake.body[0].pos == self.randCube.pos:
				self.snake.addCube()
				self.randCube = Cube(self.randomCube(self.snake), color=(0,0,255))

			self.snake.move()
			self.redraw(window)




main_loop = MainLoop()
main_loop.main()