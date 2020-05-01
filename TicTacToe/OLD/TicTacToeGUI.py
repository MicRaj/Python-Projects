import pygame
from TicTacToe import *
from PygameUI import *

BLUE = (106, 159, 181)
WHITE = (220, 220, 220)
RED = (255, 0, 0)
GREY = (169, 169, 169)


# Get square coordinates func
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


# Render func
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


game_grid = [i for i in range(1, 10)]

pygame.init()
screen = pygame.display.set_mode((800, 600))

square_width = 200
square_height = 200
margin = 5
symbols = ['X', 'O']
symbol_colours = [BLUE, RED]
symbol = symbols[0]
win = False
locations = squareCoordinates(square_width, square_height, margin)

win_banner = Heading(
    centrePos=(400, 300),
    text='Win',
    fontSize=100,
    bgRGB=WHITE,
    textRGB=BLUE)
turn = Heading(
    centrePos=(740, 50),
    text='\'s turn',
    fontSize=25,
    bgRGB=WHITE,
    textRGB=BLUE
)
while True:
    mouseUp = False
    # print_grid(game_grid)

    mousePosx, mousePosy = pygame.mouse.get_pos()
    if not win:
        xIndex = mousePosx // (square_width + margin)
        yIndex = mousePosy // (square_height + margin)
        screen.fill(WHITE)
        screen.fill(symbol_colours[symbols.index(symbol)], (650, 35, 25, 25))

        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                if xIndex < 3 and yIndex < 3:
                    if game_grid[xIndex + yIndex * 3] not in symbols:
                        game_grid[xIndex + yIndex * 3] = symbol

                        if check_for_win(symbol, game_grid):
                            print(symbol + ' Win')
                            win = True
                            turn = Heading(
                                centrePos=(400, 300),
                                text='Win',
                                fontSize=200,
                                bgRGB=WHITE,
                                textRGB=symbol_colours[symbols.index(symbol)])

                        elif check_full(game_grid):
                            print("Draw")
                            win = True

                        if symbol == symbols[0]:
                            symbol = symbols[1]
                        else:
                            symbol = symbols[0]

    else:
        screen.fill(WHITE)

    render(game_grid, locations, screen, square_width, square_height, x_colour=symbol_colours[0],
           o_colour=symbol_colours[1], empty_colour=GREY)
    turn.draw(screen)
    pygame.display.flip()
