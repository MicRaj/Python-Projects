# Sudoku by Michal Rajzer
import pygame
import pygame.freetype
import copy
from PygameUI import *

pygame.init()

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

WIN_WIDTH, WIN_HEIGHT = 800, 800
WIDTH = 600
ROWS = 9
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Sudoku")
GAP = WIDTH / ROWS

OFFSET_X = (WIN_WIDTH - WIDTH) // 2
# OFFSET_Y = (WIN_HEIGHT - WIDTH) // 2
# OFFSET_X = 50
OFFSET_Y = 150

sudoku_grid = [[0, 0, 0, 0, 0, 0, 2, 3, 4],
               [0, 1, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 8, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 7, 9, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 8, 0]]

'''
[5, 6, 7, 1, 8, 9, 2, 3, 4]
[2, 1, 3, 4, 5, 6, 7, 9, 8]
[4, 9, 8, 2, 3, 7, 1, 5, 6]
[1, 2, 4, 3, 6, 5, 8, 7, 9]
[3, 5, 9, 8, 7, 1, 4, 6, 2]
[8, 7, 6, 9, 2, 4, 3, 1, 5]
[9, 8, 1, 5, 4, 3, 6, 2, 7]
[6, 3, 2, 7, 9, 8, 5, 4, 1]
[7, 4, 5, 6, 1, 2, 9, 8, 3]
'''


class Spot:
    def __init__(self, val, x, y, changeable=True):
        self.val = val
        self.x = x
        self.y = y
        self.selected = False
        self.correct = False
        self.changeable = changeable

    def select_correct(self):
        self.correct = True

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    def change_val(self, val, priority=False):
        if self.changeable or priority:
            self.val = val

    def get_val(self):
        return int(self.val)

    def reset(self):
        self.correct = False

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
                spot_row.append(Spot(grid[i][j], (j * GAP) + OFFSET_X, (i * GAP) + OFFSET_Y, False))
            else:
                spot_row.append(Spot(grid[i][j], (j * GAP) + OFFSET_X, (i * GAP) + OFFSET_Y))

        spot_grid.append(spot_row)

    return spot_grid


def get_clicked_spot(pos):
    x, y = pos
    print("mouse x: ", x, "  mouse y: ", y)
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
    quadrantX = (x // 3) * 3  # Top left of the square x n y
    quadrantY = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if spot_grid[quadrantY + i][quadrantX + j].get_val() == n:
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


def solve(spot_grid):
    for y in range(9):
        for x in range(9):
            if spot_grid[y][x].get_val() == 0:
                for n in range(1, 10):
                    if possible(spot_grid, y, x, n):
                        spot_grid[y][x].change_val(n)
                        # WIN.fill(WHITE)
                        # draw_grid(WIN, spot_grid)
                        # pygame.display.update()
                        if solve(spot_grid):
                            return True
                        else:
                            spot_grid[y][x].change_val(0)
                return False
    return True


def main():
    spot_grid = create_spot_grid(sudoku_grid)

    def draw():
        WIN.fill(WHITE)
        draw_grid(WIN, spot_grid)
        drawUI(WIN)
        pygame.display.update()

    # Game Loop
    selected = None
    draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                for i in range(ROWS):
                    for j in range(ROWS):
                        spot_grid[i][j].reset()
                # Get entered num
                if event.unicode in [str(i) for i in range(1, 10)] and selected:
                    # selected.change_val(num)
                    selected.change_val(event.unicode)

                if event.key == pygame.K_BACKSPACE:
                    if selected:
                        selected.change_val(0)

                if event.key == pygame.K_RETURN:
                    check_grid(spot_grid)
                    # Check if done

                if event.key == pygame.K_s:
                    user_grid = copy.deepcopy(spot_grid)
                    spot_grid = create_spot_grid(sudoku_grid)
                    solve(spot_grid)
                    for i in range(ROWS):
                        for j in range(ROWS):
                            spot = spot_grid[i][j]
                            user_spot = user_grid[i][j]
                            if spot.get_val() == user_spot.get_val():
                                spot.select_correct()

                draw()

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
                    draw()


# UI
heading = Heading(
    centrePos=(WIN_WIDTH / 2, 75),
    text="SUDOKU",
    fontSize=100,
    bgRGB=WHITE,
    textRGB=BLACK,
)


def drawUI(display):
    heading.draw(display)


# def spossible(grid, y, x, n):
#     # Check if number is present in row
#     for i in range(9):
#         if grid[y][i] == n:
#             return False
#
#     # Check if number is present in column
#     for i in range(9):
#         if grid[i][x] == n:
#             return False
#
#     # Check if number is present in the square
#     quadrantX = (x // 3) * 3  # Top left of the square x n y
#     quadrantY = (y // 3) * 3
#     for i in range(3):
#         for j in range(3):
#             if grid[quadrantY + i][quadrantX + j] == n:
#                 return False
#
#     return True
#
#
# def check(grid):
#     for i in range(9):
#         for j in range(9):
#             t = grid[i][j]
#             grid[i][j] = 0
#             if not spossible(grid, i, j, t):
#                 return False
#             grid[i][j] = t
#     return True
#
#
# print(check(sudoku_grid))
main()
