from random import randint

import pygame

from pygame.sprite import Sprite


class Star(Sprite):

    def __init__(self, ai_game):

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.star_color
        self.rect = pygame.Rect(randint(0, 1000), randint(5, 30), randint(3, 4), randint(3, 4))
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def draw_star(self):

        pygame.draw.rect(self.screen, self.color, self.rect)


