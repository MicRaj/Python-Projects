# Sudoku by Michal Rajzer
import pygame.freetype
import copy
from PygameUI import *
from enum import Enum
import pickle

'''
 - WHen solve is running buttons don't work
 - Red boxes around wrong things
 - reset spot.x and spot.y when window has been resized
 - add levels
'''

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

WIN_WIDTH, WIN_HEIGHT = 800, 700
WIDTH = 500
ROWS = 9
GAP = WIDTH / ROWS

# Save files
save_file = 'saves.txt'
level_file = 'levels.txt'

# OFFSET_X = (WIN_WIDTH - WIDTH) // 2
# OFFSET_Y = (WIN_HEIGHT - WIDTH) // 2
OFFSET_X = 50
OFFSET_Y = 150


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    PLAY = 1
    MAKEGRID = 2
    LOAD = 3
    SAVE = 4


def menu():
    pygame.init()

    # Window Init
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(pygame.image.load("sudoku-icon.PNG"))

    game_state = GameState.TITLE
    spot_grid = None
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(WIN)

        if game_state == GameState.LOAD:
            game_state, spot_grid = load_screen(WIN)

        if game_state == GameState.PLAY:
            game_state, spot_grid = play(WIN, spot_grid)

        if game_state == GameState.MAKEGRID:
            game_state, spot_grid = make_sudoku(WIN)

        if game_state == GameState.SAVE:
            game_state = save(WIN, spot_grid)

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
        centrePos=(400, 300),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Start',
        action=GameState.LOAD
    )

    create_button = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Create',
        action=GameState.MAKEGRID
    )
    quit_button = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='QUIT',
        action=GameState.QUIT
    )

    buttons = [start_button, create_button, quit_button]

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
        pygame.display.update()


def load_screen(screen):
    title = Heading(
        centrePos=(400, 100),
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='SUDOKU'
    )
    level1 = UIElement(
        centrePos=(400, 150),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Level 1',
        action=GameState.PLAY
    )
    level2 = UIElement(
        centrePos=(400, 200),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Level 2',
        action=GameState.PLAY
    )
    level3 = UIElement(
        centrePos=(400, 250),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Level 3',
        action=GameState.PLAY
    )

    save1 = UIElement(
        centrePos=(400, 300),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Save 1',
        action=GameState.PLAY
    )
    save2 = UIElement(
        centrePos=(400, 350),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Save 2',
        action=GameState.PLAY
    )
    save3 = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Save 3',
        action=GameState.PLAY
    )

    return_button = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Return',
        action=GameState.TITLE
    )

    buttons = [level1, level2, level3, save1, save2, save3, return_button]
    levels = [level1, level2, level3]
    saves = [save1, save2, save3]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(WHITE)
        spot_grid = None
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                if button in levels:
                    saved_grids = get_pickled(level_file)
                    spot_grid = saved_grids[levels.index(button)]

                if button in saves:
                    saved_grids = get_pickled(save_file)
                    spot_grid = saved_grids[saves.index(button)]

                return ui_action, spot_grid
            button.draw(screen)
        title.draw(screen)
        pygame.display.update()


def play(screen, spot_grid):
    heading = Heading(
        centrePos=(WIN_WIDTH / 2, 75),
        text="SUDOKU",
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
    )
    save_button = UIElement(
        centrePos=(675, 470),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Save',
        action=GameState.SAVE
    )
    return_button = UIElement(
        centrePos=(675, 570),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Return',
        action=GameState.TITLE
    )
    buttons = [save_button, return_button]
    spot_grid = spot_grid
    while True:
        # Game Loop
        selected = None
        while True:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True

                if event.type == pygame.KEYDOWN:
                    for i in range(ROWS):
                        for j in range(ROWS):
                            spot_grid[i][j].reset()

                    if event.unicode in [str(i) for i in range(1, 10)] and selected:
                        selected.change_val(event.unicode)

                    if event.key == pygame.K_BACKSPACE:
                        # Clears selected space
                        if selected:
                            selected.change_val(0)

                    if event.key == pygame.K_RETURN:
                        # Checks which places are valid
                        check_grid(spot_grid)

                    if event.key == pygame.K_s:
                        # Solves and tells you which ones u got right
                        # Add show steps button
                        user_grid = copy.deepcopy(spot_grid)
                        for i in range(ROWS):
                            for j in range(ROWS):
                                spot_grid[i][j].reset_full()
                        # noinspection PyTypeChecker
                        solve(spot_grid, buttons + [heading], screen)
                        for i in range(ROWS):
                            for j in range(ROWS):
                                spot = spot_grid[i][j]
                                user_spot = user_grid[i][j]
                                if spot.get_val() == user_spot.get_val():
                                    spot.select_correct()

                    if event.key == pygame.K_r:
                        for i in range(ROWS):
                            for j in range(ROWS):
                                spot_grid[i][j].reset_full()

                    # Arrow Keys to select
                    if event.key == pygame.K_UP:
                        if selected:
                            spot = spot_grid[selected.row - 1][selected.col]
                            selected.unselect()
                            selected = spot
                            selected.select()

                    if event.key == pygame.K_DOWN:
                        if selected:
                            if selected.row + 1 < ROWS:
                                spot = spot_grid[selected.row + 1][selected.col]
                            else:
                                spot = spot_grid[0][selected.col]
                            selected.unselect()
                            selected = spot
                            selected.select()

                    if event.key == pygame.K_LEFT:
                        if selected:
                            spot = spot_grid[selected.row][selected.col - 1]
                            selected.unselect()
                            selected = spot
                            selected.select()

                    if event.key == pygame.K_RIGHT:
                        if selected:
                            if selected.col + 1 < ROWS:
                                spot = spot_grid[selected.row][selected.col + 1]
                            else:
                                spot = spot_grid[selected.row][0]
                            selected.unselect()
                            selected = spot
                            selected.select()

                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if get_clicked_spot(pos):
                        row, col = get_clicked_spot(pos)
                        spot = spot_grid[row][col]
                        if spot != selected:
                            if selected:
                                selected.unselect()
                            selected = spot
                            spot.select()
                            # print(selected.row, selected.col)

            screen.fill(WHITE)
            draw_grid(screen, spot_grid)
            heading.draw(screen)
            for button in buttons:
                ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
                if ui_action is not None:
                    return ui_action, spot_grid
                button.draw(screen)
            pygame.display.update()


def make_sudoku(screen):
    heading = Heading(
        centrePos=(WIN_WIDTH / 2, 75),
        text="SUDOKU",
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
    )
    play_button = UIElement(
        centrePos=(675, 370),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Start',
        action=GameState.PLAY
    )
    save_button = UIElement(
        centrePos=(675, 470),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Save',
        action=GameState.SAVE
    )
    return_button = UIElement(
        centrePos=(675, 570),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Return',
        action=GameState.TITLE
    )
    buttons = [play_button, save_button, return_button]
    spot_grid = create_spot_grid([[0 for _ in range(9)] for __ in range(9)])
    selected = None
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

            if event.type == pygame.KEYDOWN:
                for i in range(ROWS):
                    for j in range(ROWS):
                        spot_grid[i][j].reset()

                if event.unicode in [str(i) for i in range(1, 10)] and selected:
                    selected.change_val(event.unicode)

                if event.key == pygame.K_BACKSPACE:
                    # Clears selected space
                    if selected:
                        selected.change_val(0)

                if event.key == pygame.K_r:
                    for i in range(ROWS):
                        for j in range(ROWS):
                            spot_grid[i][j].reset_full()

                # Arrow Keys to select
                if event.key == pygame.K_UP:
                    if selected:
                        spot = spot_grid[selected.row - 1][selected.col]
                        selected.unselect()
                        selected = spot
                        selected.select()

                if event.key == pygame.K_DOWN:
                    if selected:
                        if selected.row + 1 < ROWS:
                            spot = spot_grid[selected.row + 1][selected.col]
                        else:
                            spot = spot_grid[0][selected.col]
                        selected.unselect()
                        selected = spot
                        selected.select()

                if event.key == pygame.K_LEFT:
                    if selected:
                        spot = spot_grid[selected.row][selected.col - 1]
                        selected.unselect()
                        selected = spot
                        selected.select()

                if event.key == pygame.K_RIGHT:
                    if selected:
                        if selected.col + 1 < ROWS:
                            spot = spot_grid[selected.row][selected.col + 1]
                        else:
                            spot = spot_grid[selected.row][0]
                        selected.unselect()
                        selected = spot
                        selected.select()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if get_clicked_spot(pos):
                    row, col = get_clicked_spot(pos)
                    spot = spot_grid[row][col]
                    if spot != selected:
                        if selected:
                            selected.unselect()
                        selected = spot
                        spot.select()
                        # print(selected.row, selected.col)

        screen.fill(WHITE)
        draw_grid(screen, spot_grid)
        heading.draw(screen)
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                for i in range(ROWS):
                    for j in range(ROWS):
                        if spot_grid[i][j].get_val():
                            spot_grid[i][j].make_unchangeable()
                            spot_grid[i][j].unselect()

                return ui_action, spot_grid
            button.draw(screen)
        pygame.display.update()


def save(screen, spot_grid):
    title = Heading(
        centrePos=(400, 100),
        fontSize=100,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='SUDOKU'
    )
    save1 = UIElement(
        centrePos=(400, 200),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='1',
        action=GameState.TITLE
    )
    save2 = UIElement(
        centrePos=(400, 300),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='2',
        action=GameState.TITLE
    )
    save3 = UIElement(
        centrePos=(400, 400),
        fontSize=50,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='3',
        action=GameState.TITLE
    )
    return_button = UIElement(
        centrePos=(400, 500),
        fontSize=30,
        bgRGB=WHITE,
        textRGB=BLACK,
        text='Return',
        action=GameState.TITLE
    )

    buttons = [save1, save2, save3, return_button]
    saves = [save1, save2, save3]

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
                if button in saves:
                    saved_grids = get_pickled(save_file)
                    save_num = saves.index(button)
                    saved_grids[save_num] = spot_grid
                    pickle_grids(save_file, saved_grids)
                return ui_action
            button.draw(screen)
        title.draw(screen)
        pygame.display.update()


# Game Logic
class Spot:
    def __init__(self, val, x, y, row, col, changeable=True):
        self.val = val
        self.x = x
        self.y = y
        self.row = row
        self.col = col
        self.selected = False
        self.correct = False
        self.changeable = changeable

    def select_correct(self):
        self.correct = True

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def make_unchangeable(self):
        self.changeable = False

    def change_val(self, val, priority=False):
        if self.changeable or priority:
            self.val = val

    def get_val(self):
        return int(self.val)

    def reset(self):
        self.correct = False

    def reset_full(self):
        if self.changeable:
            self.val = 0

    @property
    def color(self):
        return GREY if self.changeable else BLACK

    def draw(self, display):
        if self.val:
            surf = createSurfaceWithText(str(self.val), textRGB=self.color)
            rect = surf.get_rect(center=(self.x + GAP / 2, self.y + GAP / 2))
            display.blit(surf, rect)

        if self.correct and self.changeable:
            # pygame.draw.line(display, GREEN, (self.x, self.y), (self.x + GAP, self.y), 10)
            # pygame.draw.line(display, GREEN, (self.x, self.y), (self.x, self.y + GAP), 10)
            # pygame.draw.line(display, GREEN, (self.x + GAP, self.y + GAP), (self.x + GAP, self.y), 10)
            # pygame.draw.line(display, GREEN, (self.x + GAP, self.y + GAP), (self.x, self.y + GAP), 10)
            pygame.draw.line(display, GREEN, (self.x + GAP // 4, self.y + 5), (self.x + 8, self.y + GAP // 4), 10)

        if self.selected:
            pygame.draw.line(display, RED, (self.x, self.y), (self.x + GAP, self.y), 7)
            pygame.draw.line(display, RED, (self.x, self.y), (self.x, self.y + GAP), 7)
            pygame.draw.line(display, RED, (self.x + GAP, self.y + GAP), (self.x + GAP, self.y), 7)
            pygame.draw.line(display, RED, (self.x + GAP, self.y + GAP), (self.x, self.y + GAP), 7)


def draw_grid(display, grid):
    # GRID LINES
    for i in range(1, ROWS):
        if i % 3 == 0:
            thickness = 5
        else:
            thickness = 2
        pygame.draw.line(display, BLACK, (i * GAP + OFFSET_X, 0 + OFFSET_Y), (i * GAP + OFFSET_X, WIDTH + OFFSET_Y),
                         thickness)
        pygame.draw.line(display, BLACK, (0 + OFFSET_X, i * GAP + OFFSET_Y), (WIDTH + OFFSET_X, i * GAP + OFFSET_Y),
                         thickness)

    # BORDER LINES
    pygame.draw.line(display, BLACK, (0 + OFFSET_X, 0 + OFFSET_Y), (0 + OFFSET_X, WIDTH + OFFSET_Y), 7)
    pygame.draw.line(display, BLACK, (0 + OFFSET_X, 0 + OFFSET_Y), (WIDTH + OFFSET_X, 0 + OFFSET_Y), 7)
    pygame.draw.line(display, BLACK, (WIDTH + OFFSET_X, WIDTH + OFFSET_Y), (WIDTH + OFFSET_X, 0 + OFFSET_Y), 7)
    pygame.draw.line(display, BLACK, (WIDTH + OFFSET_X, WIDTH + OFFSET_Y), (0 + OFFSET_X, WIDTH + OFFSET_Y), 7)

    # TEXT
    for i in range(ROWS):
        for j in range(ROWS):
            grid[i][j].draw(display)


def create_spot_grid(grid):
    spot_grid = []
    for i in range(ROWS):
        spot_row = []
        for j in range(ROWS):
            if grid[i][j]:
                spot_row.append(Spot(grid[i][j], (j * GAP) + OFFSET_X, (i * GAP) + OFFSET_Y, i, j, False))
            else:
                spot_row.append(Spot(grid[i][j], (j * GAP) + OFFSET_X, (i * GAP) + OFFSET_Y, i, j, True))

        spot_grid.append(spot_row)

    return spot_grid


def get_clicked_spot(pos):
    x, y = pos
    # print("mouse x: ", x, "  mouse y: ", y)
    if OFFSET_Y < y < WIDTH + OFFSET_Y and OFFSET_X < x < WIDTH + OFFSET_X:
        row = (y - OFFSET_Y) // GAP
        col = (x - OFFSET_X) // GAP
        return int(row), int(col)

    else:
        return None


# Sudoku Check Logic
def possible(spot_grid, y, x, n):
    # Check if number is present in row
    for i in range(9):
        if spot_grid[y][i].get_val() == n:
            return False

    # Check if number is present in column
    for i in range(9):
        if spot_grid[i][x].get_val() == n:
            return False

    # Check if number is present in the square
    quadrant_x = (x // 3) * 3  # Top left of the square x n y
    quadrant_y = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if spot_grid[quadrant_y + i][quadrant_x + j].get_val() == n:
                return False
    return True


def check_grid(spot_grid):
    solved = True
    for i in range(ROWS):
        for j in range(ROWS):
            temp = int(spot_grid[i][j].get_val())
            spot_grid[i][j].change_val(0, True)
            spot_ok = possible(spot_grid, i, j, temp)
            if not spot_ok:
                spot_grid[i][j].change_val(temp, True)
                solved = False
            else:
                spot_grid[i][j].select_correct()

            spot_grid[i][j].change_val(temp, True)

    return solved


def solve(spot_grid, ui_objects, screen=None):
    for y in range(9):
        for x in range(9):
            if spot_grid[y][x].get_val() == 0:
                for n in range(1, 10):
                    if possible(spot_grid, y, x, n):
                        spot_grid[y][x].change_val(n)

                        # DRAW
                        # screen.fill(WHITE)
                        # draw_grid(screen, spot_grid)
                        # for obj in ui_objects:
                        #     obj.draw(screen)
                        # pygame.display.update()

                        if solve(spot_grid, ui_objects, screen):
                            return True
                        else:
                            spot_grid[y][x].change_val(0)
                return False
    return True


# Pickle
def get_pickled(file_name):
    file = open(file_name, 'rb')
    grid_arr = pickle.load(file)
    file.close()
    return grid_arr


def pickle_grids(file_name, grid_arr):
    file = open(file_name, 'wb')
    # noinspection PyArgumentList
    pickle.dump(grid_arr, file)


if __name__ == '__main__':
    menu()
