from TicTacToe import *
from PygameUI import *
from TicTacToeMiniMax import *
from enum import Enum

'''
To Do :
-tidy up code:)
-tidy up UI
-Add difficulties
 - limit depth on mini max
 
'''
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
GREY = (169, 169, 169)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    TWOPLAYER = 1
    ONEPLAYER = 2


def menu():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    gameState = GameState.TITLE

    while True:
        if gameState == GameState.TITLE:
            gameState = titleScreen(screen)
        if gameState == GameState.TWOPLAYER:
            gameState = two_player(screen)
        if gameState == GameState.ONEPLAYER:
            gameState = one_player(screen)
        if gameState == GameState.QUIT:
            pygame.quit()


def titleScreen(screen):
    title = Heading(
        centrePos=(400, 200),
        fontSize=60,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Tic Tac Toe'
    )
    start_two_player_button = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='2 Player',
        action=GameState.TWOPLAYER
    )
    start_one_player_button = UIElement(
        centrePos=(400, 300),
        fontSize=50,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='1 Player',
        action=GameState.ONEPLAYER
    )
    quitButton = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Quit',
        action=GameState.QUIT
    )

    buttons = [start_one_player_button, start_two_player_button, quitButton]

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


def one_player(screen):
    overlay = Heading(
        # Placeholder
        centrePos=(0, 0),
        text='',
        fontSize=1,
        bgRGB=WHITE,
        textRGB=WHITE
    )
    turn_text = Heading(
        centrePos=(740, 50),
        text='\'s turn',
        fontSize=25,
        bgRGB=WHITE,
        textRGB=BLUE
    )
    resetButton = UIElement(
        centrePos=(700, 470),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Reset',
        action=GameState.ONEPLAYER
    )
    returnButton = UIElement(
        centrePos=(700, 570),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE
    )
    buttons = [resetButton, returnButton]

    game_grid = [i for i in range(1, 10)]
    square_width = 200
    square_height = 200
    margin = 5

    markers = ['X', 'O']
    symbol_colours = [BLUE, RED]
    symbol = markers[0]
    user_marker = markers[0]
    pc_marker = markers[1]

    game_end = False
    locations = squareCoordinates(square_width, square_height, margin)

    while True:
        move = False
        mouseUp = False
        mouse_pressed = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pressed = True
            elif event.type == pygame.QUIT:
                pygame.quit()

        if not game_end:
            if symbol == user_marker and mouse_pressed:
                xIndex = mouse_x // (square_width + margin)
                yIndex = mouse_y // (square_height + margin)
                if xIndex < 3 and yIndex < 3:
                    if game_grid[xIndex + yIndex * 3] not in markers:
                        game_grid[xIndex + yIndex * 3] = symbol
                        move = True

            elif symbol == pc_marker:
                move = findBestMove(symbol, game_grid)
                game_grid[move] = pc_marker
                move = True

            if move:
                if check_for_win(symbol, game_grid):
                    game_end = True
                    overlay = Heading(
                        centrePos=(400, 300),
                        text='Win',
                        fontSize=200,
                        bgRGB=WHITE,
                        textRGB=symbol_colours[markers.index(symbol)])

                elif check_full(game_grid):
                    # Draw
                    game_end = True
                    overlay = Heading(
                        centrePos=(400, 300),
                        text='DRAW',
                        fontSize=200,
                        bgRGB=WHITE,
                        textRGB=BLACK)

                if symbol == markers[0]:
                    symbol = markers[1]
                else:
                    symbol = markers[0]

        screen.fill(WHITE)
        screen.fill(symbol_colours[markers.index(symbol)], (650, 35, 25, 25))
        render(game_grid, locations, screen, square_width, square_height, x_colour=symbol_colours[0],
               o_colour=symbol_colours[1], empty_colour=GREY)
        turn_text.draw(screen)
        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                return uiAction
            button.draw(screen)
        if game_end:
            overlay.draw(screen)

        pygame.display.flip()


def two_player(screen):
    overlay = Heading(
        # Placeholder
        centrePos=(0, 0),
        text='',
        fontSize=1,
        bgRGB=WHITE,
        textRGB=WHITE
    )
    turn_text = Heading(
        centrePos=(740, 50),
        text='\'s turn',
        fontSize=25,
        bgRGB=WHITE,
        textRGB=BLUE
    )
    resetButton = UIElement(
        centrePos=(700, 470),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Reset',
        action=GameState.TWOPLAYER
    )
    returnButton = UIElement(
        centrePos=(700, 570),
        fontSize=30,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Return',
        action=GameState.TITLE
    )
    buttons = [resetButton, returnButton]

    game_grid = [i for i in range(1, 10)]
    square_width = 200
    square_height = 200
    margin = 5

    markers = ['X', 'O']
    symbol_colours = [BLUE, RED]
    symbol = markers[0]

    game_end = False
    locations = squareCoordinates(square_width, square_height, margin)

    while True:
        mouseUp = False
        mouse_pressed = False
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouseUp = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pressed = True
            elif event.type == pygame.QUIT:
                pygame.quit()

        if not game_end and mouse_pressed:
            xIndex = mouse_x // (square_width + margin)
            yIndex = mouse_y // (square_height + margin)
            screen.fill(symbol_colours[markers.index(symbol)], (650, 35, 25, 25))
            if xIndex < 3 and yIndex < 3:
                if game_grid[xIndex + yIndex * 3] not in markers:
                    game_grid[xIndex + yIndex * 3] = symbol

                    if check_for_win(symbol, game_grid):

                        game_end = True
                        turn_text = Heading(
                            centrePos=(400, 300),
                            text='Win',
                            fontSize=200,
                            bgRGB=WHITE,
                            textRGB=symbol_colours[markers.index(symbol)])

                    elif check_full(game_grid):
                        game_end = True
                        turn_text = Heading(
                            centrePos=(400, 300),
                            text='DRAW',
                            fontSize=200,
                            bgRGB=WHITE,
                            textRGB=BLACK)

                    if symbol == markers[0]:
                        symbol = markers[1]
                    else:
                        symbol = markers[0]

        screen.fill(WHITE)
        screen.fill(symbol_colours[markers.index(symbol)], (650, 35, 25, 25))
        render(game_grid, locations, screen, square_width, square_height, x_colour=symbol_colours[0],
               o_colour=symbol_colours[1], empty_colour=GREY)
        turn_text.draw(screen)
        for button in buttons:
            uiAction = button.update(pygame.mouse.get_pos(), mouseUp)
            if uiAction is not None:
                return uiAction
            button.draw(screen)
        pygame.display.flip()


def squareCoordinates(width, height, margin):
    locations = []
    yCord = margin
    xCord = margin
    for row in range(3):
        for item in range(3):
            locations.append((xCord, yCord))
            xCord += (margin + width)
        yCord += (margin + height)
        xCord = margin
    return locations


def render(grid, places, screen, width, height, x_colour, o_colour, empty_colour=None):
    for i in range(9):
        sym = grid[i]
        coord = places[i]
        if sym == 'X':
            screen.fill(x_colour, (coord[0], coord[1], width, height))
        elif sym == 'O':
            screen.fill(o_colour, (coord[0], coord[1], width, height))
        elif empty_colour is not None:
            screen.fill(empty_colour, (coord[0], coord[1], width, height))


if __name__ == '__main__':
    menu()
