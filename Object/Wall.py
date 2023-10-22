import pygame

from constants import SIZE_WALL, MARGIN


class Wall:
    def __init__(self, row, col, color):
        self.image = pygame.Surface([SIZE_WALL, SIZE_WALL])
        # self.image.fill(color)
        pygame.draw.rect(self.image, color, (0, 0, SIZE_WALL, SIZE_WALL), 1)

        self.row = row
        self.col = col

        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))
