from random import randint


class Settings:

    def __init__(self):

        # Window Settings
        self.screen_width = 1920
        self.screen_height = 900
        self.bg_colour = (0, 0, 0)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (125, 125, 250)
        self.bullets_allowed = 6

        # Star Settings
        self.star_width = randint(1, 4)
        self.star_height = randint(1, 4)
        self.star_color = (250, 255, 200)

        # Alien Settings
        self.fleet_drop_speed = 10

        # Game speed and score scaling
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2
        self.alien_speed = 1.0
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed and point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

