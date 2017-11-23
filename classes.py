#########################################
# File name: Classes.py                 #
# Author: David Gurevich                #
# Course: ICS3U                         #
# Instructor: D. Mavrodin               #
# --------------------------------------#
# Date Created: November 6, 2017 18:03  #
# Date / Time last modified: 15/11/2017 #
#########################################

import pygame
import random
from pygame.locals import *

# Game speed
STARTING_FPS = 10
FPS_INCREMENT_FREQUENCY = 100

# Direction constants
DIRECTION_UP = 1
DIRECTON_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

# World size
WORLD_SIZE_X = 20
WORLD_SIZE_Y = 20

# Snake and food attributes
SNAKE_START_LENGTH = 3
DIRECTION_DICTIONARY = {
    K_UP: DIRECTION_UP, K_w: DIRECTION_UP,
    K_DOWN: DIRECTON_DOWN, K_s: DIRECTON_DOWN,
    K_LEFT: DIRECTION_LEFT, K_a: DIRECTION_LEFT,
    K_RIGHT: DIRECTION_RIGHT, K_d: DIRECTION_RIGHT
}


# Snake class
class Snake:
    def __init__(self, x, y, start_length):
        '''

        Initializes Snake Object

        :param x: Initial X Coordinate for Snake
        :param y: Inital Y Coordinate for Snake
        :param start_length: Initial Start Length for Snake
        '''
        self.startLength = start_length
        self.startX = x
        self.startY = y
        self.pieces = []
        self.direction = 1
        self.reset()

    def reset(self):
        '''
        Resets Snake back to its original state
        '''
        self.pieces = []
        self.direction = 1

        for n in range(0, self.startLength):
            self.pieces.append((self.startX, self.startY + n))

    def change_direction(self, direction):
        '''
        Changes the direction of the snake.

        ~WARNING~ The snake cannot reverse in on itself ~WARNING~
        :param direction: Desired Direction
        '''
        if self.direction == 1 and direction == 2: return
        if self.direction == 2 and direction == 1: return
        if self.direction == 3 and direction == 4: return
        if self.direction == 4 and direction == 3: return

        self.direction = direction

    def get_head(self):
        '''
        :return: Value of the head of the snake. Returns a tuple value (x, y)
        '''
        return self.pieces[0]

    def get_tail(self):
        '''
        :return: Value of the tail of the snake. Returns a tuple value (x, y)
        '''
        return self.pieces[len(self.pieces) - 1]

    def update(self):
        '''
        Updates Snake by moving it in desired direction.
        Temporarily adds an extra head piece, before removing tail piece.
        '''
        (headX, headY) = self.get_head()
        head = ()

        # Create new piece that is the new head of the snake
        if self.direction == 1:
            head = (headX, headY - 1)
        elif self.direction == 2:
            head = (headX, headY + 1)
        elif self.direction == 3:
            head = (headX - 1, headY)
        elif self.direction == 4:
            head = (headX + 1, headY)

        # Remove tail of the snake and add a new head
        self.pieces.insert(0, head)
        self.pieces.pop()
    def grow(self):
        '''
        Increses overall length of Snake.
        '''
        (tx, ty) = self.get_tail()
        piece = ()

        if self.direction == 1:
            piece = (tx, ty + 1)
        elif self.direction == 2:
            piece = (tx, ty - 1)
        elif self.direction == 3:
            piece = (tx + 1, ty)
        elif self.direction == 4:
            piece = (tx - 1, ty)

        self.pieces.append(piece)

    def eat_self(self):
        '''
        :return: Boolean checks whether or not two pieces of the snake are occupying the same block.
        '''
        return len([p for p in self.pieces if p == self.get_head()]) > 1


# SNAKE GAME CLASS

class SnakeGame:

    def __init__(self, window, screen, clock, font):
        self.window = window
        self.screen = screen
        self.clock = clock
        self.font = font

        self.BACKGROUND = pygame.image.load('bg.png')
        self.RED_APPLE = pygame.image.load('red_apple.png').convert_alpha()
        self.GOLD_APPLE = pygame.image.load('golden_apple.png').convert_alpha()
        self.SNAKE_HEAD = pygame.image.load('snake_head.png').convert_alpha()
        self.SNAKE_BODY = pygame.image.load('snake_body.png').convert_alpha()

        self.fps = STARTING_FPS
        self.ticks = 0
        self.playing = False
        self.score = 0
        self.apples_eaten = 0

        self.attempts = 0

        self.timer = 20000

        self.nextDirection = DIRECTION_UP
        self.sizeX = WORLD_SIZE_X
        self.sizeY = WORLD_SIZE_Y
        self.food = []
        self.snake = Snake(WORLD_SIZE_X / 2, WORLD_SIZE_Y / 2, SNAKE_START_LENGTH)

        self.add_food()

        self.bgMusic = pygame.mixer.Sound('music.ogg')
        self.bgMusic.set_volume(0.2)
        pygame.mixer.Channel(0).play(self.bgMusic)

    def add_food(self):
        '''
        Adds a new piece of food in a random location NOT OCCUPIED BY THE SNAKE
        :return: None
        '''
        fx = None
        fy = None

        fx = random.randint(1, self.sizeX)
        fy = random.randint(1, self.sizeY)

        if (fx, fy) in self.snake.pieces:
            self.add_food() # Utilizes recursion
        else:
            self.food.append((fx, fy))

    def input(self, events):
        '''
        Designates direction that snake should move in based on input from the player.

        :param events: PyGame Events
        :return: False if player quits. Otherwise, True.
        '''
        for e in events:
            if e.type == QUIT:
                return False

            elif e.type == KEYDOWN:
                if e.key in DIRECTION_DICTIONARY:
                    self.nextDirection = DIRECTION_DICTIONARY[e.key]
                elif e.key == K_SPACE and not self.playing:
                    self.reset()

        return True

    def update(self):
        '''
        Update the game screen based on whether or not the snake has:
            a) eaten an Apple
            b) eaten a Golden Apple
            c) Direction of Snake changed
            d) Snake has collided with boundaries of window
        This function also processes the time.

        The timer is updated every tick, which happens approximately 1000 times per second, meaning that
        subtracting 1 from the timer every tick is an alternative to an external timer.

        '''
        self.snake.change_direction(self.nextDirection)
        self.snake.update()

        # If snake hits a food block, then "consume" the food, add new food and grow the snake
        for food in self.food:
            if self.snake.get_head() == food:
                self.food.remove(food)
                self.add_food()
                self.apples_eaten += 1
                self.timer += 2000
                print("Current Score", self.score+1)
                if self.apples_eaten % 5 == 1 and self.apples_eaten >= 1:
                    for i in range(3):
                        self.snake.grow()
                else:
                    self.snake.grow()
                self.score = self.apples_eaten
                self.fps += 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('chomp.ogg'))

        # If snake collides with self or the screen boundaries, then game over
        (hx, hy) = self.snake.get_head()
        if self.snake.eat_self() or hx < 1 or hy < 1 or hx > self.sizeX or hy > self.sizeY:
            self.attempts += 1
            self.playing = False

        self.timer -= 100
        if self.timer <= 0:
            self.playing = False
        self.second_timer = (self.timer - (self.timer%1000))/1000

    def reset(self):
        '''
        Reset the snake to its original values.
        '''
        self.playing = True
        self.nextDirection = DIRECTION_UP
        self.fps = STARTING_FPS
        self.score = 0
        self.apples_eaten = 0
        self.food.clear()
        self.add_food()
        self.timer = 20000
        self.snake.reset()
        print("------------------------------------------")

    def draw(self):
        '''
        This function draws all the elements on the screen in the following order:
            1. Background
            2. Pieces of the snake from Head to Tail
            3. Food Objects (Every 5th apple is a golden apple)
            4. Text for Score and then timer.

        It then flips the screen (updates entire screen rather than updating a certain portion.
        '''
        self.screen.blit(self.BACKGROUND, (0, 0))

        (width, height) = self.window.get_size()
        block_width = int(width / self.sizeX)
        block_height = int(height / self.sizeY)

        if self.second_timer <= 5:
            timer_color = (255,0,0)
        else:
            timer_color = (255,255,255)

        # Draw pieces of snake
        for (px, py) in self.snake.pieces:

            if (px, py) == self.snake.get_head():
                self.screen.blit(self.SNAKE_HEAD, (block_width * (px - 1), block_height * (py - 1)))
            else:
                self.screen.blit(self.SNAKE_BODY, (block_width * (px - 1), block_height * (py - 1)))

        # Draw food objects
        for (fx, fy) in self.food:
            if self.apples_eaten % 5 == 0:
                self.screen.blit(self.GOLD_APPLE, (block_width * (fx - 1), block_height * (fy - 1)))
            else:
                self.screen.blit(self.RED_APPLE, (block_width * (fx - 1), block_height * (fy - 1)))

        # Draw Score and Timer

        self.screen.blit(self.font.render("Score "+str(self.score),1, (255,255,255)),(660,10))
        self.screen.blit(self.font.render("Timer "+str(int(self.second_timer)),1,timer_color),(655, 30))

        pygame.display.flip()

    def draw_intro_end(self):
        '''
        Intro and exit screens are run with the same function.
        '''
        if not self.attempts == 0:
            self.screen.fill((255, 0, 0))
            self.screen.blit(self.font.render("Game  over! Press  Space  to  start  a  new  game", 1, (255, 255, 255)),
                             (100, 300))
            self.screen.blit(self.font.render("Your score is    %d" % self.score, 1, (255, 255, 255)), (300, 340))
        else:
            self.screen.fill((0, 255, 0))
            self.screen.blit(self.font.render("Press Space to start playing!", 1, (255, 255, 255)), (200, 370))
        pygame.display.flip()

    # Run the main game loop
    def run(self, events):
        '''
        Function that essentially controls everything.

        :param events: PyGame events
        :return: Return False if game not playing, otherwise, return True.
        '''
        if not self.input(events):
            return False

        if self.playing:
            self.update()
            self.draw()
        else:
            self.draw_intro_end()

        self.clock.tick(self.fps)

        self.ticks += 1
        if self.ticks % FPS_INCREMENT_FREQUENCY == 0:
            self.fps += 1

        return True
