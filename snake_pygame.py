#!/usr/bin/python3
from config import *
import pygame
import random

# Snake 
	# make a grid +
	# make a cube +
	# make a moving Cube +
	# add random Cube
	# make Snake be bigger when eat Cube
	# add score
class Cube:
	
	def __init__(self, posx, posy, color=GREEN):
		self.posx = posx
		self.posy = posy
		self.pos = (self.posx, self.posy)
		self.color = color

		self.dirnx = 0
		self.dirny = 1

	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny

		self.posx += self.dirnx 
		self.posy += self.dirny
		self.pos = (self.posx, self.posy)

	def draw(self, window):
		distance_btn_rows = SIZE // ROWS
		pygame.draw.rect(window, self.color ,(DIST_BTN_ROWS * self.posx, DIST_BTN_ROWS * self.posy, DIST_BTN_ROWS, DIST_BTN_ROWS))		

class Snake:
	body = []
	turns = {}
	def __init__(self, posx, posy, color=GREEN):
		self.posx = posx
		self.posy = posy
		self.dirnx = 0
		self.dirny = 0
		self.color = color
		self.head = Cube(posx, posy)
		self.body.append(self.head)
		self.pos = (self.posx, self.posy)

	def move(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()

			keys = pygame.key.get_pressed()

			if ( keys[pygame.K_LEFT] ):
				self.dirnx = -1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			if ( keys[pygame.K_RIGHT] ):
				self.dirnx = 1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
				

			if ( keys[pygame.K_UP] ):
				self.dirny = -1
				self.dirnx = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			if ( keys[pygame.K_DOWN] ):
				self.dirny = 1
				self.dirnx = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0], turn[1])
				if (i == len(self.body) - 1) == 1:
					self.turns.pop(p)

			else:
				if c.dirnx == 1 and c.posx >= ROWS - 1: 
					c.posx = 0
					c.posy = c.posy
					
				elif c.dirnx == -1 and c.posx <= 0:
					c.posx = ROWS - 1
					c.posy = c.posy
					
				elif c.dirny == 1 and c.posy >= ROWS - 1:
					c.posx = c.posx
					c.posy = 0
					
				elif c.dirny == -1 and c.posy <= 0:
					c.posx = c.posx
					c.posy = ROWS - 1
					
				else:
					c.move(c.dirnx, c.dirny)
					

	def draw(self, window):
		for c in self.body:
			c.draw(window)

	def add_cube(self):
		tail = self.body[-1]
		tail_x, tail_y = tail.dirnx, tail.dirny

		if tail_x == 1 and tail_y == 0:
			self.body.append(Cube(tail.posx - 1, tail.posy, color=GREEN))
		if ( tail_x == -1 and tail_y == 0 ):
			self.body.append(Cube(tail.posx + 1, tail.posy, color=GREEN))
		if ( tail_x == 0 and tail_y == 1 ):
			self.body.append(Cube(tail.posx, tail.posy - 1, color=GREEN))
		if ( tail_x == 0 and tail_y == -1):
			self.body.append(Cube(tail.posx, tail.posy + 1, color=GREEN)) 

		self.body[-1].dirnx = tail_x
		self.body[-1].dirny = tail_y
		

def randomCube(item):
	position = item.body
	while ( True ):
		x = random.randrange(ROWS)
		y = random.randrange(ROWS)
		
		if ( len(list(filter(lambda z: z.pos == (x, y), position))) > 0):
			print(lambda z: z.pos == (x, y), position)
			continue
		else:
			break
	return (x, y)

def randomCube_2(item):
	position = item.body

	while True:
		x = random.randrange(ROWS)
		y = random.randrange(ROWS)
		if ( position.posx == x and position.posy == y):
			continue
		else:
			break

	return (x, y)
def draw_grid(window):
	x = 0
	y = 0
	for line in range(ROWS):
		x += DIST_BTN_ROWS
		y += DIST_BTN_ROWS
		pygame.draw.line(window, WHITE, (x, 0), (x, SIZE))
		pygame.draw.line(window, WHITE, (0,y), (SIZE, y))


def redraw(window):
	global snake, randcube
	window.fill(BLACK)
	snake.draw(window)
	randcube.draw(window)
	draw_grid(window)
	pygame.display.update()


def main():
	global snake, randcube
	snake = Snake(15, 15)
	randcube = Cube(10, 10, color=RED)
	window = pygame.display.set_mode((500, 500))

	play = True

	clock = pygame.time.Clock()
	while play:
		
		pygame.time.delay(50)
		clock.tick(10)

		if ( snake.body[0].posx == randcube.posx and snake.body[0].posy == randcube.posy ):
			snake.add_cube()
			pos = randomCube(snake)
			randcube = Cube(15, 15, color=RED)
			print(pos)
		snake.move()

		redraw(window)

if __name__ == "__main__":
	main()