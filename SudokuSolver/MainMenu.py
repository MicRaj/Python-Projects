
from PygameUI import *
from enum import Enum
import SudokuPygame
# Colours

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


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
        fontSize=60,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='SUDOKU'
    )
    startButton = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Start',
        action=GameState.NEWGAME
    )
    quitButton = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [startButton, quitButton]

    while True:
        mouseUp = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True

        screen.fill(BLUE)

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