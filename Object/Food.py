import pygame

from constants import WHITE, SIZE_WALL, YELLOW, MARGIN


class Food:
    def __init__(self, row, col, width, height, color):
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.row = row
        self.col = col

        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        if color == YELLOW:
            self.rect.top += SIZE_WALL // 2 - height // 2
            self.rect.left += SIZE_WALL // 2 - width // 2

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

    def getRC(self):
        return [self.row, self.col]
