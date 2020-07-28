
from PygameUI import *
from enum import Enum
# import SudokuPygame
# Colours

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1


def menu():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    gameState = GameState.TITLE

    while True:
        if gameState == GameState.TITLE:
            gameState = titleScreen(screen)
        if gameState == GameState.NEWGAME:
            gameState = playLevel(screen)
        if gameState == GameState.QUIT:
            pygame.quit()


def titleScreen(screen):
    title = Heading(
        centrePos=(400, 200),
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='SUDOKU'
    )
    startButton = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Start',
        action=GameState.NEWGAME
    )
    quitButton = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [startButton, quitButton]

    while True:
        mouseUp = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True

        screen.fill(WHITE)

        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                return uiAction
            button.draw(screen)

        title.draw(screen)
        pygame.display.flip()


def playLevel(screen):
    returnButton = UIElement(
        centrePos=(140, 570),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE
    )
    while True:
        mouseUp = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
        screen.fill(BLUE)

        uiAction = returnButton.update(pygame.mouse.get_pos(), mouseUp)
        if uiAction is not None:
            return uiAction
        returnButton.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    menu()