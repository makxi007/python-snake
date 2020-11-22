#!/usr/bin/python3
from config import *
import pygame
import random

# Snake 
	# make a grid +
	# make a cube +
	# make a moving Cube
	# add random Cube
	# make Snake be bigger when eat Cube
	# add score
class Cube:
	def __init__(self, posx, posy, color=COLOR):
		self.posx = posx
		self.posy = posy
		self.pos = (self.posx, self.posy)
		self.color = color

	def move(self, dirnx, dirny):
		self.posx += dirnx 
		self.posy += dirny

	def draw(self, window):
		pygame.draw.rect(window, COLOR ,(DIST_BTN_ROWS * self.posx, DIST_BTN_ROWS * self.posy, DIST_BTN_ROWS, DIST_BTN_ROWS))		

class Snake:
	body = []
	turns = {}
	def __init__(self, posx, posy, color=COLOR):
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
				

			if ( keys[pygame.K_UP] ):
				self.dirny = -1
				self.dirnx = 0

			if ( keys[pygame.K_DOWN] ):
				self.dirny = 1
				self.dirnx = 0

			

			for i, c in enumerate(self.body):
				p_x = c.posx
				p_y = c.posy
				print(p_x)
				print(p_y)
				print(self.turns)

		self.head.move(self.dirnx, self.dirny)

	def draw(self, window):
		self.head.draw(window)

def draw_grid(window):
	x = 0
	y = 0
	for line in range(ROWS):
		x += DIST_BTN_ROWS
		y += DIST_BTN_ROWS
		pygame.draw.line(window, WHITE, (x, 0), (x, SIZE))
		pygame.draw.line(window, WHITE, (0,y), (SIZE, y))

def redraw(window):
	global snake
	window.fill(BLACK)
	snake.draw(window)
	draw_grid(window)

	pygame.display.update()


def main():
	global snake
	snake = Snake(15, 15)
	window = pygame.display.set_mode((500, 500))

	play = True

	clock = pygame.time.Clock()
	while play:
		
		pygame.time.delay(50)
		clock.tick(10)
		
		snake.move()

		redraw(window)

if __name__ == "__main__":
	main()