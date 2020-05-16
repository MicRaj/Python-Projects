# Snake by Michal Rajzer
import pygame
import random


class Snake:
    def __init__(self, start_vel=[0, 10], start_len=1):
        self.x_vel = start_vel[0]
        self.y_vel = start_vel[1]

        self.head = [200, 200]
        self.tail = [[200, 200 + ((i + 1) * sq_size)] for i in range(start_len)]  # [[200, 210], [200, 220]]
        self.tail_len = len(self.tail)

    def __str__(self):  # For debugging purposes
        return str(self.full_snake)

    @property
    def full_snake(self):
        body = self.tail.copy()
        body.insert(0, self.head)
        return body

    def move(self):
        snake_body = self.full_snake
        self.head = [self.head[0] + self.x_vel, self.head[1] + self.y_vel]
        self.tail = [snake_body[i] for i in range(self.tail_len)]

    def eat(self):
        self.tail_len += 1

    def collision(self):
        for x, y in self.tail:
            if [x, y] == [self.head[0], self.head[1]]:
                return True
        return False

    def draw(self, surface):
        for cube in self.full_snake:
            pygame.draw.rect(surface, (200, 0, 0,), (cube[0], cube[1], tile_size, tile_size))


class Food:
    def __init__(self):
        self.w_tiles = screen_width // sq_size
        self.h_tiles = screen_height // sq_size

        self.x = random.randint(0, self.w_tiles) * sq_size
        self.y = random.randint(0, self.h_tiles) * sq_size

    def new_place(self):
        self.x = random.randint(0, self.w_tiles) * sq_size
        self.y = random.randint(0, self.h_tiles) * sq_size

    @property
    def place(self):
        return [self.x, self.y]

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 200, 0), (self.x, self.y, tile_size, tile_size))


# Initialize pygame
screen_width = 600
screen_height = 600
tile_size = 20
spacing = 5
sq_size = tile_size + spacing

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake   Score : 0")

# Obj
snake = Snake(start_vel=[0, -sq_size], start_len=4)
food = Food()
clock = pygame.time.Clock()
score = 0
game_objects = [snake, food]

# Main loop
game_over = False
while not game_over:
    clock.tick(10)
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.y_vel == 0:
                    snake.x_vel = 0
                    snake.y_vel = -sq_size
                    break
            elif event.key == pygame.K_DOWN:
                if snake.y_vel == 0:
                    snake.x_vel = 0
                    snake.y_vel = sq_size
                    break
            elif event.key == pygame.K_RIGHT:
                if snake.x_vel == 0:
                    snake.x_vel = sq_size
                    snake.y_vel = 0
                    break
            elif event.key == pygame.K_LEFT:
                if snake.x_vel == 0:
                    snake.x_vel = -sq_size
                    snake.y_vel = 0
                    break
    '''
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        if snake.y_vel == 0:
            snake.x_vel = 0
            snake.y_vel = -sq_size
    elif keys[pygame.K_DOWN]:
        if snake.y_vel == 0:
            snake.x_vel = 0
            snake.y_vel = sq_size
    elif keys[pygame.K_RIGHT]:
        if snake.x_vel == 0:
            snake.x_vel = sq_size
            snake.y_vel = 0
    elif keys[pygame.K_LEFT]:
        if snake.x_vel == 0:
            snake.x_vel = -sq_size
            snake.y_vel = 0
    '''

    # Draw to the screen
    screen.fill((0, 0, 0))
    for obj in game_objects:
        obj.draw(screen)
    pygame.display.update()

    # Check for food
    if snake.head == food.place:
        snake.eat()
        food.new_place()
        while food.place in snake.full_snake:
            food.new_place()
        score += 1
        pygame.display.set_caption("Snake   Score : " + str(score))

    # Update Snake
    snake.move()

    # Check for collision with tail
    if snake.collision():
        game_over = True
    # Check for collision with window
    elif snake.head[0] < 0 or snake.head[0] > screen_width - tile_size or snake.head[1] < 0 or \
            snake.head[1] > screen_height - tile_size:
        game_over = True

pygame.quit()
