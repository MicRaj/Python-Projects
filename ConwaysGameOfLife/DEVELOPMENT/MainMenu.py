import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)


def createSurfaceWithText(text, fontSize, textRGB, bgRGB):
    font = pygame.freetype.SysFont("Courier", fontSize, bold=True)
    surface, rect = font.render(text=text, fgcolor=textRGB, bgcolor=bgRGB)
    return surface.convert_alpha()


class Heading:

    def __init__(self, centrePos, text, fontSize, bgRGB, textRGB):
        self.headingImage = createSurfaceWithText(text, fontSize, textRGB, bgRGB)
        self.headingRect = self.headingImage.get_rect(center=centrePos)

    def draw(self, surface):
        surface.blit(self.headingImage, self.headingRect)


class UIElement(Sprite):

    def __init__(self, centrePos, text, fontSize, bgRGB, textRGB, action=None):

        self.mouseOver = False

        defaultImage = createSurfaceWithText(text, fontSize, textRGB, bgRGB)

        highlightedImage = createSurfaceWithText(text, fontSize * 1.2, textRGB, bgRGB)

        self.images = [defaultImage, highlightedImage]
        self.rects = [
            defaultImage.get_rect(center=centrePos),
            highlightedImage.get_rect(center=centrePos)]

        self.action = action

        # calls the init method of the parent sprite class
        super().__init__()  # Calls Sprite.__init__()

    # properties that vary the image and its rect when the mouse is over the element
    @property
    def image(self):
        return self.images[1] if self.mouseOver else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouseOver else self.rects[0]

    def update(self, mousePos, mouseUp):
        if self.rect.collidepoint(mousePos):
            self.mouseOver = True
            if mouseUp:
                return self.action
        else:
            self.mouseOver = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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
        centrePos=(400,200),
        fontSize=60,
        bgRGB=BLUE,
        textRGB=WHITE,
        text='Conways Game Of Life'
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
