from PygameUI import *
from GameOfLife import *
from enum import Enum
from time import sleep
import copy

'''
To Do :
- CreateGrid 
- add a button to go back to start and edit - In progress, goesd back to last edited grid
- add a button to clear
- Add a save
- let user adjust size of grid
'''
# Colours
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (52, 1, 255)
LIGHTPURPLE = (174, 92, 255)
LIGHTGREEN = (0, 255, 0)
GREEN = (0, 200, 0)
SHADOW = (192, 192, 192)
RED = (200, 0, 0)
LIGHTRED = (255, 100, 100)
YELLOW = (204, 204, 0)

width = 15
height = 15
margin = 2
size = (35, 47)
speed = 0.001


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    RUNSIM = 1
    CREATE = 2


def main():
    pygame.init()
    pygame.display.set_caption('Conways Game Of Life')
    icon = pygame.image.load('Bombom.png')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((800, 600))
    gameState = GameState.TITLE
    grid = None
    while True:
        if gameState == GameState.TITLE:
            grid = None
            gameState = titleScreen(screen)

        if gameState == GameState.RUNSIM:
            gameState, grid = runSimulation(screen, grid)

        if gameState == GameState.CREATE:
            gameState, grid = createGrid(screen, grid)

        if gameState == GameState.QUIT:
            pygame.quit()


def titleScreen(screen):
    title = Heading(
        centrePos=(400, 200),
        fontSize=60,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Conways Game Of Life'
    )
    generateRandomButton = UIElement(
        centrePos=(400, 300),
        fontSize=50,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Generate Random',
        action=GameState.RUNSIM
    )
    createGridButton = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Create',
        action=GameState.CREATE
    )
    quitButton = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [generateRandomButton, createGridButton, quitButton]

    while True:
        mouseUp = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BLUE)

        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                return uiAction
            button.draw(screen)

        title.draw(screen)
        pygame.display.flip()


def createGrid(screen, cellGrid=None):
    startButton = UIElement(
        centrePos=(700, 370),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='Start',
        action=GameState.RUNSIM,
        textEnlargeOnHighlight=1.05
    )
    returnButton = UIElement(
        centrePos=(700, 570),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE,
        textEnlargeOnHighlight=1.05
    )
    clearButton = UIElement(
        centrePos=(700, 470),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='Clear',
        action=None,
        textEnlargeOnHighlight=1.05
    )

    buttons = [startButton, returnButton]
    if cellGrid is None:
        cellGrid = Culture(size[0], size[1])
    cellCoordinates = cellLocations(width, height, margin, cellGrid.grid)

    while True:
        mouseUp = False
        mousePosx, mousePosy = pygame.mouse.get_pos()
        xIndex = mousePosx // (width + margin)
        yIndex = mousePosy // (height + margin)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
            if pygame.mouse.get_pressed()[0]:
                if xIndex < len(cellGrid.grid[0]) and yIndex < len(cellGrid.grid):
                    cellGrid.grid[yIndex][xIndex] = 1
            if pygame.mouse.get_pressed()[2]:
                if xIndex < len(cellGrid.grid[0]) and yIndex < len(cellGrid.grid):
                    cellGrid.grid[yIndex][xIndex] = 0
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(WHITE)
        render(cellGrid.grid, cellCoordinates, screen, width, height, BLACK, SHADOW)

        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                return uiAction, cellGrid
            button.draw(screen)

        startButton.draw(screen)
        returnButton.draw(screen)
        pygame.display.flip()


def runSimulation(screen, cellGrid=None):
    returnButton = UIElement(
        centrePos=(700, 570),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE,
        textEnlargeOnHighlight=1.05
    )
    editButton = UIElement(
        centrePos=(700, 470),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='Stop & Edit',
        action=GameState.CREATE,
        textEnlargeOnHighlight=1.05
    )
    backButton = UIElement(
        centrePos=(700, 370),
        fontSize=30,
        bgRGB=BLACK,
        textRGB=WHITE,
        text='back',
        action=GameState.CREATE,
        textEnlargeOnHighlight=1.05
    )

    buttons = [returnButton, editButton, backButton]
    if cellGrid is None:
        cellGrid = Culture(size[0], size[1])
        cellGrid.createRandom()

    ogCellGrid = copy.deepcopy(cellGrid)
    cellCoordinates = cellLocations(width, height, margin, cellGrid.grid)

    while True:

        mouseUp = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(LIGHTPURPLE)

        render(cellGrid.grid, cellCoordinates, screen, width, height, YELLOW)
        cellGrid.grid = newGrid(cellGrid.grid)

        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                if button == backButton:
                    return uiAction, ogCellGrid
                else:
                    return uiAction, cellGrid
            button.draw(screen)

        pygame.display.update()
        sleep(speed)


def render(grid, places, screen, width, height, colour, secondaryColour=None):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            coordinate = places[y][x]
            if grid[y][x] == 1:
                screen.fill(colour, (coordinate[0], coordinate[1], width, height))
            elif secondaryColour is not None:
                screen.fill(secondaryColour, (coordinate[0], coordinate[1], width, height))


def cellLocations(width, height, margin, cellGrid):
    locations = []
    yCord = margin + 3
    xCord = margin
    for row in range(len(cellGrid)):
        rows = []
        for item in range(len(cellGrid[0])):
            rows.append((xCord, yCord))
            xCord += (margin + width)
        yCord += (margin + height)
        xCord = margin
        locations.append(rows)
    return locations


if __name__ == "__main__":
    main()
