import pygame
import random
import tkinter as tk
from tkinter import messagebox

class Cube(object):
	rows = 20
	size = 500
	def __init__(self, start, dirnx=1,dirny=0, color=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color


	def move(self, dirnx, dirny):
		self.dirnx = dirnx
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)#change our position

	def draw(self, window):
		dist = self.size // self.rows # Width and Height of each cube or distance between rows
		l = self.pos[0] # current row
		j = self.pos[1] # current col
		sizeCube = (l*dist+1, j*dist+1, dist-2,dist-2)
		pygame.draw.rect(window, self.color, sizeCube)
	
		#By multiplying the row and col of cube by the width and height 
		#of each cube we can determine where to draw it
	

		#It is not so interesting 
		#So I'll do it later
		#if eyes:
		#.....

class Snake(object):
	body = []
	turns = {}
	def __init__(self, color, pos):
		self.color = color
		# the head in the front of the snake
		self.head = Cube(pos)
		# add our head( which is the Cube(object)) to the body
		self.body.append(self.head)

		# Representation of direction
		self.dirnx = 0
		self.dirny = 1

	def move(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

			keys = pygame.key.get_pressed()

			for key in keys:
				if keys[ pygame.K_LEFT]:
					self.dirnx = -1
					self.dirny = 0 
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # ?

				elif keys[ pygame.K_RIGHT]:
					self.dirnx = 1
					self.dirny = 0
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # ?

				elif keys[ pygame.K_UP]:
					self.dirnx = 0
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # ?

				elif keys[ pygame.K_DOWN]:
					self.dirnx = 0
					self.dirny = 1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] # ?

		# ?
		for i, c in enumerate(self.body): # Loop through every cube in snake body
			p = c.pos[:] # stores the current position the cubes in the grid
			if p in self.turns: # if our position where We just turned
				turn = self.turns[p] # get the direction that We should turn
				c.move(turn[0], turn[1]) # move our cube in that direction
				if i == len(self.body) - 1: # if it is the last cube in our body
					self.turns.pop(p) # remove the turn from the direction

			else: # if p not in our turns and if we reach the edge of our window We will make it appear on the other side
				if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1] >= c.rows - 1: c.pos = (c.pos[0], 0)
				elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
				else: c.move(c.dirnx, c.dirny)

	# ?
	def draw(self, window):
		for i, c in enumerate(self.body):
			if i == 0:
				c.draw(window) # if first (mean head) draw eyes
			else:
				c.draw(window) # and than just draw other cubes

	def AddCube(self):
		tail = self.body[-1] #tail of the snake
		dirnx_tail, dirny_tail = tail.dirnx, tail.dirny

		if dirnx_tail == 1 and dirny_tail == 0:
			self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
		elif dirnx_tail == -1 and dirny_tail == 0:
			self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
		elif dirnx_tail == 0 and dirny_tail == 1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
		elif dirnx_tail == 0 and dirny_tail == -1:
			self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

		# set the cubes direction of the dir of snake
		self.body[-1].dirnx = dirnx_tail
		self.body[-1].dirny = dirny_tail

	def reset(self, pos):
		self.head = Cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1


def drawGrid(wind, size, rows):
	sizeBtnRows = size // rows
	x = 0
	y = 0
	for l in range(rows):
		x += sizeBtnRows
		y += sizeBtnRows
		pygame.draw.line(wind, (255,255,255), (x, 0), (x, size))
		pygame.draw.line(wind, (255,255,255), (0, y), (size, y))

def redraw(wind):
	global size, rows, snake, snack
	wind.fill((0,0,0))
	snake.draw(wind)
	snack.draw(wind)
	drawGrid(wind, size, rows)
	pygame.display.update()

def randomSnak(rows, item):
	positions = item.body # all positions of cubes in our snake

	while True: # Generate position while We have not right pos.
		x = random.randrange(rows)
		y = random.randrange(rows)

		# If pos occupied the snake start generate pos again
		if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
			continue
		else:
			break
	return (x, y)

def message_box(subject, content):
	root = tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try:
		root.destroy()
	except:
		pass


def main():
	global size, rows, snake, snack
	size = 500
	rows = 20
	window = pygame.display.set_mode((size, size))
	snake = Snake((255, 0, 0), (10, 10))
	snack = Cube(randomSnak(rows, snake), color=(0,255,0))

	play = True
	clock = pygame.time.Clock()
	while play:
		pygame.time.delay(50)
		clock.tick(10)
		snake.move()
		if snake.body[0].pos == snack.pos:
			snake.AddCube()
			snack = Cube(randomSnak(rows, snake), color=(0,255,0))

		for x in range(len(snake.body)):
			if snake.body[x].pos in list(map(lambda z:z.pos, snake.body[x+1:])):
				print("Score: ", len(snake.body))
				message_box("You lost", "Play AGAIN!!!")
				snake.reset((10,10))
				break
		
		redraw(window)
main()