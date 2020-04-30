import pygame
import pygame.freetype
from pygame.sprite import Sprite


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

    def __init__(self, centrePos, text, fontSize, bgRGB, textRGB, action=None, textEnlargeOnHighlight=1.2):
        self.mouseOver = False

        defaultImage = createSurfaceWithText(text, fontSize, textRGB, bgRGB)
        highlightedImage = createSurfaceWithText(text, fontSize * textEnlargeOnHighlight, textRGB, bgRGB)

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
