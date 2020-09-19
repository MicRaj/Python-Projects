import pygame

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window Init
pygame.init()
WIN_WIDTH, WIN_HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Mouse Track")


# pygame.display.set_icon(pygame.image.load())


def main():
    game_run = True
    pointer_x, pointer_y = 500, 500
    while game_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif pygame.mouse.get_pressed()[0]:
                pointer_x, pointer_y = pygame.mouse.get_pos()
                pygame.mouse.set_visible(False)
                print(pointer_x, pointer_y)

            else:
                pygame.mouse.set_visible(True)

        WIN.fill(BLACK)

        # Draw Pointer
        pygame.draw.line(WIN, RED, (pointer_x - 10, pointer_y), (pointer_x + 10, pointer_y), 3)
        pygame.draw.line(WIN, RED, (pointer_x, pointer_y - 10), (pointer_x, pointer_y + 10), 3)

        pygame.display.update()


def send_point(x, y):
    pass


main()
