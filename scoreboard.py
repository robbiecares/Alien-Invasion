import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (255,215,0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_high_score()
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score below the highscore
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right
        self.score_rect.top = self.high_score_rect.bottom

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.current_high_score, -1)
        high_score_str = "Hi: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)

        # Display the high score in the top right corner of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the current level into a rendered image."""
        level_str = 'Level: {}'.format(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color)

        # Display the level below remaining lives
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left
        self.level_rect.top = self.screen_rect.top + 65

    def show_score(self):
        """Draw scores & level to the screen."""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        if self.stats.score < self.stats.current_high_score:
            self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.current_high_score:
            self.stats.current_high_score = self.stats.score
        self.prep_high_score()

    def check_endgame_highscore(self):
        if self.stats.current_high_score > self.stats.starting_high_score:
            self.stats.write_high_score()

    def prep_ships(self):
        """Show how many ships are left."""
        # todo: rotate ships in group to point up
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

