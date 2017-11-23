#########################################
# File name: Game.py                    #
# Author: David Gurevich                #
# Course: ICS3U                         #
# Instructor: D. Mavrodin               #
# --------------------------------------#
# Date Created: November 6, 2017 17:27  #
# Last Modified: 12/11/2017 @ 20:32     # 
#########################################

import sys
from classes import *

pygame.init()
pygame.display.set_caption('PyGame Snake - David Gurevich')

window = pygame.display.set_mode((900, 900))
snake_window = pygame.display.set_mode((800, 800))
screen = pygame.display.get_surface()
clock = pygame.time.Clock()
font = pygame.font.Font('arcade_font.TTF', 30)

game = SnakeGame(snake_window, screen, clock, font)

while game.run(pygame.event.get()):
    pass

pygame.quit()
sys.exit()
