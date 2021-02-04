from random import random

import pygame

from alien_invasion import AlienInvasion


class AIPlayer:

	def __init__(self, ai_game):
		"""Automatic player for Alien Invasion"""

		# Reference to the game object
		self.ai_game = ai_game

	def run_game(self):
		"""Replaces the original run_game(), so we can interject our own controls"""

		# Start out in an active state and hide the mouse
		self.ai_game.stats.game_active = True
		pygame.mouse.set_visible(False)

		# Speed up the game for development purposes

		self._modify_speed(5)

		# Get the full fleet size
		self.fleet_size = len(self.ai_game.aliens)

		# Start the main loop for the game
		while True:
			# Still call ai_game._check_events(), so keyboard can still be used to quit
			self.ai_game._check_events()
			if self.ai_game.stats.game_active:
				self.ai_game.ship.update()
				self.ai_game._update_bullets()
				self.ai_game._update_aliens()
				self._implement_strategy()

			self.ai_game._update_screen()

	def _implement_strategy(self):
		"""Implement an automated strategy for playing the game"""

		# Sweep right and left until half the fleet is destroyed, then stop
		if len(self.ai_game.aliens) >= 0.5 * self.fleet_size:
			self._sweep_right_left()
		else:
			self.ai_game.ship.moving_right = False
			self.ai_game.ship.moving_left = False

		# Fire a bullet whenever possible
		self._fire_random_bullet(0.5)

	def _sweep_right_left(self):
		"""Sweep the ship right and left continuously"""
		ship = self.ai_game.ship
		screen_rect = self.ai_game.screen.get_rect()

		if not ship.moving_right and not ship.moving_left:
			# Ship hasn't started moving, move to right
			ship.moving_right = True
		elif ship.moving_right and ship.rect.right > screen_rect.right - 10:
			# Ship about to hit right edge, move to left
			ship.moving_right = False
			ship.moving_left = True
		elif ship.moving_left and ship.rect.left < 10:
			# Ship about to left edge, move to right
			ship.moving_right = True
			ship.moving_left = False

	def _modify_speed(self, speed_factor):
		self.ai_game.settings.ship_speed *= speed_factor
		self.ai_game.settings.bullet_speed *= speed_factor
		self.ai_game.settings.alien_speed *= speed_factor

	def _fire_random_bullet(self, firing_frequency):
		if random() < firing_frequency:
			self.ai_game._fire_bullet()


if __name__ == '__main__':
	ai_game = AlienInvasion()

	ai_player = AIPlayer(ai_game)
	ai_player.run_game()
