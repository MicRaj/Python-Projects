import pygame
import time
from GameOfLife import *

white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
blue = (0, 10, 255)

culture = Culture(50, 50)
culture.createRandom()

# Initialise
pygame.init()
pygame.display.set_caption('Conways Game Of Life')
icon = pygame.image.load('Bombom.png')
pygame.display.set_icon(icon)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def gameIntro():
    title = "Conways Game Of Life"
    button1 = "Generate Random"
    button2 = "Make Grid"
    display_width = 800
    display_height = 600
    intro = True
    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay = pygame.display.set_mode((display_width, display_height))
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 50)
        smallText = pygame.font.Font('freesansbold.ttf', 20)
        TextSurf, TextRect = text_objects(title, largeText)
        buttonSurf1, buttonRect1 = text_objects(button1, smallText)
        buttonSurf2, buttonRect2 = text_objects(button2, smallText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        buttonRect1.center = (display_width / 3, display_height * 2 / 3)
        buttonRect2.center = (display_width * 2 / 3, display_height * 2 / 3)
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(buttonSurf1, buttonRect1)
        gameDisplay.blit(buttonSurf2, buttonRect2)
        pygame.display.update()


def gameLoop(cultureObj):
    width = 10
    height = 10
    margin = 2
    numGens = 1000
    speed = 0.05
    pygame.display.update()

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
    gameDisplay = pygame.display.set_mode(
        (len(cultureObj.grid) * (margin + width) + margin, len(cultureObj.grid[0]) * (margin + height) + margin))
    # ----------Main loop -------------
    locations = []
    running = True
    while running:
        # get locations:
        yCord = margin
        xCord = margin
        for row in range(len(cultureObj.grid)):
            rows = []
            for item in range(len(cultureObj.grid[0])):
                rows.append((xCord, yCord))
                xCord += (margin + width)
            yCord += (margin + height)
            xCord = margin
            locations.append(rows)

        gameDisplay.fill(white)
        render(cultureObj.grid, locations, gameDisplay, )
        pygame.display.update()
        for gen in range(numGens):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            time.sleep(speed)
            render(cultureObj.grid, locations, gameDisplay)
            cultureObj.new(newGrid(cultureObj.grid))
            pygame.display.update()
        # ---------Comment this line if you want it to run forever----------------
        running = False


if __name__ == "__main__":
    gameIntro()
    time.sleep(2)
    gameLoop(culture)
    pygame.quit()
