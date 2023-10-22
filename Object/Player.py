import pygame

from constants import SIZE_WALL, MARGIN


class Player:
    def __init__(self, row, col, fileImage):
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))

        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        self.row = row
        self.col = col

    def change_state(self, rotate, fileImage):
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))
        self.image = pygame.transform.rotate(self.image, rotate)

        self.rect = self.image.get_rect()
        self.rect.top = self.row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = self.col * SIZE_WALL + MARGIN["LEFT"]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

    def getRC(self):
        return [self.row, self.col]

    def setRC(self, row, col):
        self.row = row
        self.col = col
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def move(self, d_R, d_C):
        self.rect.top += d_R
        self.rect.left += d_C

    def touch_New_RC(self, row, col):
        return self.rect.top == row * SIZE_WALL and self.rect.left == col * SIZE_WALL
