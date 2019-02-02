import pygame
from load_functions import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, filename, pos, groups):
        super().__init__(groups)
        self.filename = filename
        self.button = load_image(filename + ".png")

        self.button_true = load_image(filename + "_True.png")

        self.image = self.button
        self.rect = self.image.get_rect().move(pos)

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.button_true
        else:
            self.image = self.button

    def apply(self, pos):
        if self.rect.collidepoint(pos):
            return self.filename

class BackGround(pygame.sprite.Sprite):


    def __init__(self,filename, groups, screen):
        super().__init__(groups)
        self.image = pygame.transform.scale(load_image(filename),
                               (int(screen.get_width()), int(screen.get_height())))
        self.rect = self.image.get_rect()