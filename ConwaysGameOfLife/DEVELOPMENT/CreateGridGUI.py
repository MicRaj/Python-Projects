import pygame
import time
from GameOfLife import *

white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
blue = (0, 10, 255)

width = 5
height = 5
margin = 1
numGens = 1000
speed = 0.05

culture = Culture(100, 100)


def render(grid, places, screen):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            coordinate = places[y][x]
            if grid[y][x] == 1:
                screen.fill(black, (coordinate[0], coordinate[1], width, height))
            else:
                screen.fill(blue, (coordinate[0], coordinate[1], width, height))



def cellLocations(width, height, margin, cellGrid):
    locations = []
    yCord = margin
    xCord = margin
    for row in range(len(culture.grid)):
        rows = []
        for item in range(len(culture.grid[0])):
            rows.append((xCord, yCord))
            xCord += (margin + width)
        yCord += (margin + height)
        xCord = margin
        locations.append(rows)
    return locations


# -------Initialise Window-----------
pygame.init()
# gameDisplay = pygame.display.set_mode(
#    (len(culture.grid) * (margin + width) + margin, len(culture.grid[0]) * (margin + height) + margin))
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Conways Game Of Life')

# ----------Main loop -------------
locations = cellLocations(width, height, margin, culture.grid)
while True:
    mousePosx, mousePosy = pygame.mouse.get_pos()
    xIndex = mousePosx // (width + margin)
    yIndex = mousePosy // (height + margin)
    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            if xIndex < len(culture.grid[0]) and yIndex < len(culture.grid):
                culture.grid[yIndex][xIndex] = 1
        if pygame.mouse.get_pressed()[2]:
            if xIndex < len(culture.grid[0]) and yIndex < len(culture.grid):
                culture.grid[yIndex][xIndex] = 0
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    gameDisplay.fill(white)
    render(culture.grid, locations, gameDisplay)
    pygame.display.update()
