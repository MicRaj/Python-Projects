from PygameUI import *
from enum import Enum

# import SudokuPygame
# Colors

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
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        if game_state == GameState.NEWGAME:
            game_state = play(screen)
        if game_state == GameState.QUIT:
            pygame.quit()


def title_screen(screen):
    title = Heading(
        centrePos=(400, 200),
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='SUDOKU'
    )
    start_button = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Start',
        action=GameState.NEWGAME
    )
    quit_button = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [start_button, quit_button]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(WHITE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        title.draw(screen)
        pygame.display.flip()


def play(screen):
    return_button = UIElement(
        centrePos=(140, 570),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE
    )
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = return_button.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_button.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    menu()
