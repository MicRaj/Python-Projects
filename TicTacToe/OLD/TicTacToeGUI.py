import pygame
from PygameUI import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
RED = (255,0,0)

pygame.init()

screen = pygame.display.set_mode((800, 600))

square_width = 200
square_height = 200
margin = 5
# Get square coordinates func
# Render func




while True:
    screen.fill(WHITE)
    screen.fill(BLUE,(margin,margin,square_height,square_width))
    pygame.display.flip()
