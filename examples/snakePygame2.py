import pygame

class Cube(object):
	rows = 20
	size = 500
	def __init__(self, start, color=(0,255,0), dirnx=1,dirny=0):
		self.pos = start
		self.color = color
		self.dirnx = 1
		self.dirny = 0

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

	def draw(self, window):
		distance = self.size // self.rows
		i = self.pos[0]
		j = self.pos[1]

		pygame.draw.rect(window, self.color, (distance*i, distance*j, distance-1, distance - 1))

class Snake(object):
	body = []
	turns = {}
	def __init__(self, pos, color):
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

				elif keys[ pygame.K_RIGHT ]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[ pygame.K_UP ]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

				elif keys[ pygame.K_DOWN ]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if i == len(self.body) - 1:
					self.turns.pop(p)
			else:
				if c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
				elif c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1]) 
				elif c.dirny == -1 and c.pos[1] <= 0:c.pos = (c.pos[0], c.rows-1)
				elif c.dirny == 1 and c.pos[1] >= c.rows - 1 : c.pos = (c.pos[0], 0)
				else:c.move(c.dirnx, c.dirny)

	def draw(self, window):
		for i, c in enumerate(self.body):
			c.draw(window)

def drawGrid(window, size, rows):
	sizeBtnRows = size // rows
	x = 0
	y = 0 
	for l in range(rows):
		x += sizeBtnRows
		y += sizeBtnRows
		pygame.draw.line(window, (255,255,255), (x, 0), (x, size))
		pygame.draw.line(window, (255,255,255), (0, y), (size, y))

def redraw(window):
	global rows, size, snake
	window.fill((0,0,0))
	snake.draw(window)
	drawGrid(window,size,rows)
	
	pygame.display.update() #? I wanna know about it more

def main():
	global rows, size, snake
	rows = 20
	size = 500
	window = pygame.display.set_mode((size, size))
	snake = Snake((18, 18), (0, 255, 0))

	play = True
	clock = pygame.time.Clock()

	while play:
		pygame.time.delay(50)
		clock.tick(10)

		snake.move()

		redraw(window)

main()