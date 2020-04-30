import pygame
import time
from GameOfLife import *

white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
blue = (0, 10, 255)

culture = Culture(100, 100)
culture.createRandom()


def main():
    width = 5
    height = 5
    margin = 1
    numGens = 1000
    speed = 0.05

    def render(grid, places, screen):
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 1:
                    colour = black
                else:
                    colour = white
                coordinate = places[y][x]
                screen.fill(colour, (coordinate[0], coordinate[1], width, height))

    # -------Initialise Window-----------
    pygame.init()
    gameDisplay = pygame.display.set_mode(
        (len(culture.grid) * (margin + width) + margin, len(culture.grid[0]) * (margin + height) + margin))
    pygame.display.set_caption('Conways Game Of Life')
    icon = pygame.image.load('Bombom.png')
    pygame.display.set_icon(icon)

    # ----------Main loop -------------
    locations = []
    running = True
    while running:
        # get locations:
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

        gameDisplay.fill(white)
        render(culture.grid, locations, gameDisplay, )
        pygame.display.update()
        for gen in range(numGens):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            time.sleep(speed)
            render(culture.grid, locations, gameDisplay)
            culture.new(newGrid(culture.grid))
            pygame.display.update()
        # ---------Comment this line if you want it to run forever----------------
        running = False


if __name__ == "__main__"   :
    main()
    pygame.quit()
