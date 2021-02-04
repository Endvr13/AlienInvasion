import sys
from time import sleep

import pygame
import numpy

from alien import Alien
from settings import Settings
from ship import Ship
from bullet import Bullet
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import sound_effects as se

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Create instance to store game statistics
        self.stats = GameStats(self)
        # Create instance to store game elements
        self.stars = pygame.sprite.Group()
        self._create_bg_stars()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # Draw score information
        self.sb = Scoreboard(self)
        # Draw play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            # Update game objects
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Check for inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Keydown events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Keyup events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            se.bullet_sound.set_volume(0.25)
            se.bullet_sound.play()

    def _update_bullets(self):
        self.bullets.update()
        # Remove bullets outside play area
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_highscore()
            se.alien_sound.set_volume(0.25)
            se.bullet_sound.play()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - float(1.33 * alien_width)
        number_aliens_x = available_space_x // float(1.33 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in numpy.arange(number_rows):
            for alien_number in numpy.arange(number_aliens_x):
                self._create_aliens(alien_number, row_number)

    def _create_aliens(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1.33 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_bg_stars(self):
        star = Star(self)

        available_space_y = self.settings.screen_height
        number_rows = available_space_y

        for row_number in numpy.arange(number_rows):
            for star_number in numpy.arange(5):
                self._create_stars(star_number, row_number)

    def _create_stars(self, star_number, row_number):
        star = Star(self)
        star_width, star_height = star.rect.x, star.rect.y
        star.x = star_width + star_width * star_number
        star.rect.x = star.x
        star.rect.y = star.rect.height + star.rect.height * row_number
        self.stars.add(star)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Remove remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create new fleet and centre player ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause to show player ship was hit
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when Play button is clicked"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game speed settings
            self.settings.initialize_dynamic_settings()
            # Reset stats and set game state to active
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # Remove all remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create new fleet and centre ship
            self._create_fleet()
            self.ship.center_ship()
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Updates screen"""
        # Redraw the screen during each pass through the loop.

        self.screen.fill(self.settings.bg_colour)

        for star in self.stars.sprites():
            star.draw_star()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.ship.blitme()
        # Draw the score info
        self.sb.show_score()
        # Draw play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
