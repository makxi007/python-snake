#!/usr/bin/python3
from config import *
import pygame
import random

# Snake 
	# make a grid +
	# make a cube +
	# make a moving Cube +
	# add random Cube +
	# make Snake be bigger when eat Cube + 
	# add score
	# add pause quit buttons
	# add play again button
	# add smash area
	# add pause area
	# make reset of the game:
	# https://www.techwithtim.net/tutorials/game-development-with-python/snake-pygame/tutorial-4/

pygame.init()

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

	def reset(self, pos):
		self.head = Cube(pos[0], pos[1])
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = -1


	def move(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				pygame.quit()

			keys = pygame.key.get_pressed()

			if (keys[pygame.K_a]):
				self.dirnx = -1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			if (keys[pygame.K_d]):
				self.dirnx = 1
				self.dirny = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
				

			if (keys[pygame.K_w]):
				self.dirny = -1
				self.dirnx = 0
				self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

			if (keys[pygame.K_s]):
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

class gameEvent:
	def reset_game(self):
		global intro, snake
		print("Reset")
		intro = False
		snake.reset((15,15))

	def game_intro(self, window, msg):
		global intro
		intro = True
		clock = pygame.time.Clock()
		while (intro == True):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				keys = pygame.key.get_pressed()
				#Press w to continue the game
				if ( keys[pygame.K_t] ):
				 	intro = False
				 	break
				
			self.button(window,msg,150,100,100,100,PURPLE,DARK_PURPLE, self.reset_game)

			pygame.display.update()
			clock.tick(15)

	def smash(self, window, is_smashed):
		if (is_smashed == True):
			while (is_smashed):
				for event in pygame.event.get():
					if (event.type == pygame.QUIT):
						pygame.quit()
				
				self.button(window, "You was smashed!",150,100, 200,100,RED, DARK_RED)
				self.button(window, "Play again!",200, 400, 100,50, GREEN, LIME_GREEN, self.reset_game)

				pygame.display.update()

	def text_objects(self, text, font):
		text_surface = font.render(text, True, WHITE)
		return text_surface, text_surface.get_rect()

	def button(self,win, msg, x, y, w, h, ic, ac, action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if (x+w > mouse[0] > x and y+w > mouse[1] > y):
			pygame.draw.rect(win, ic, (x,y,w,h))
			if (click[0] == 1 and action != None):
				action()
		else:
			pygame.draw.rect(win, ac, (x,y,w,h))
		small_text = pygame.font.SysFont("Arial", 20)
		text_surface, text_rect = self.text_objects(msg, small_text)
		text_rect.center = ( (x+(w/2), (y+(h/2) )))
		win.blit(text_surface, text_rect)

def randomCube(item):
	position = item.body
	while ( True ):
		x = random.randrange(ROWS)
		y = random.randrange(ROWS)
		
		if ( len(list(filter(lambda z: z.pos == (x, y), position))) > 0):
			
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

def game_loop():
	global snake, randcube, game_event, game_intro, window, play
	play = True

	clock = pygame.time.Clock()
	while (play):
		
		pygame.time.delay(50)
		clock.tick(10)

		if (snake.body[0].posx == randcube.posx and snake.body[0].posy == randcube.posy):
			snake.add_cube()
			pos = randomCube(snake)
			randcube = Cube(pos[0], pos[1], color=RED)
		
		snake.move()

		keys = pygame.key.get_pressed()
		#Press q to pause the game
		if (keys[pygame.K_r]):
			pause = True
			#Press w to continue the game
			game_event.game_intro(window, "Pause")

		#Smash!
		if (keys[pygame.K_y]):
			game_event.smash(window, True)

		for c in range(len(snake.body) ):
			print(c)

			check_ifx = snake.body[c].posx in list(map(lambda z:z.posx, snake.body[c+1:]))
			check_ify = snake.body[c].posy in list(map(lambda z:z.posy, snake.body[c+1:]))
			if (check_ifx and check_ify):
				game_event.game_intro(window, "Smashed!")
				break

		redraw(window)

def main():
	global snake, randcube, game_event, window
	snake = Snake(15, 15)
	randcube = Cube(10, 10, color=RED)
	game_event = gameEvent()

	window = pygame.display.set_mode((500, 500))
	
	game_loop()
	
if __name__ == "__main__":
	main()