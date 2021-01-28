from random import randint


class Settings:

    def __init__(self):

        # Window Settings
        self.screen_width = 1920
        self.screen_height = 900
        self.bg_colour = (0, 0, 0)

        # Ship Settings
        self.ship_speed = 1.5

        # Bullet Settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (250, 250, 250)
        self.bullets_allowed = 6

        # Star Settings
        self.star_width = randint(1, 4)
        self.star_height = randint(1, 4)
        self.star_color = (250, 255, 200)

        # Alien Settings
        self.alien_speed = 1.0
