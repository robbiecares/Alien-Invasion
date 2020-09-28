import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background
from game_stats import GameStats
from button import Button


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        # Set the background
        self.bg_color = self.settings.bg_color
        self.BackGround = Background('images/starfield.png', [0, 0])

        # Declare the game objects
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "Play")

        # Make the pause button
        self.pause_button = Button(self, "Pause")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active and not self.stats.game_paused:
                self._update_bullets()
                self._update_aliens()
                self.ship.update()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_events()

    def _start_game(self):
        """for starting a new game"""
        # Reset game stats
        self.stats.reset_stats()

        # clear out all active Aliens & bullets
        self.aliens.empty()
        self.bullets.empty()

        # create a new fleet & reset the ship location
        self._create_fleet()
        self.ship.center_ship()

        # set game statuses
        self.stats.game_active = True
        self.stats.game_paused = False

        # Hide the cursor
        pygame.mouse.set_visible(False)
        pygame.mouse.set_pos(0,0)

    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.stats.game_paused:
                self.stats.game_paused = False
            elif not self.stats.game_active:
                self._start_game()
            else:
                self._fire_bullet()
        elif event.key == pygame.K_p:
            if self.stats.game_paused:
                self.stats.game_paused = False
            elif self.stats.game_active:
                self._pause_game()
            elif not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_mouse_events(self):
        """Respond to mouse click."""
        mouse_pos = pygame.mouse.get_pos()
        self._check_play_button(mouse_pos)
        self._check_pause_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_pause_button(self, mouse_pos):
        """Unpause game when the player clicks pause"""
        button_clicked = self.pause_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.stats.game_paused = False
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to any bullet-alien collisions"""
        # Remove any bullets and aliens that have collied
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets & create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """"Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_width = self.ship.rect.width
        available_space_x = self.settings.screen_width - (3 * alien_width) - ship_width
        number_aliens_per_row = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_of_rows = available_space_y // (2 * alien_height) + 1

        # set the starting position for fleet creation
        x_starting_position = ship_width + (3 * alien_width)

        # Create the full fleet of aliens.
        for row_number in range(number_of_rows):
            for alien_number in range(number_aliens_per_row):
                self._create_alien(alien_number, row_number, x_starting_position)

    def _create_alien(self, alien_number, row_number, x_starting_position):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = x_starting_position + (alien_width + 2 * alien_width * alien_number)
        alien.rect.x = alien.x
        alien.y = alien.rect.height + (2 * alien.rect.height * row_number)
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_left()

    def _pause_game(self):
        """For pausing an active game"""
        self.stats.game_paused = True
        pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Redraw the screen during each pass through the loop"""
        self.screen.fill(self.bg_color)
        self.screen.blit(self.BackGround.image, self.BackGround.rect)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the pause button if the game is paused
        if self.stats.game_paused:
            self.pause_button.draw_button()

        # Draw the play button if the game is not active
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_left(self):
        """Check if any aliens have reached the left side of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                # treat this the same as if the ship got hit.
                self._ship_hit()
                break


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
