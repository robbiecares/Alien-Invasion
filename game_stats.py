import json
from pathlib import Path


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.score_file = Path('high_score.json')
        self.starting_high_score = json.load(self.score_file.open()) if self.score_file.exists() else 0
        self.current_high_score = self.starting_high_score

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.game_paused = False
        self.settings_menu = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def write_high_score(self):
        """Create a high score file and write the high score to it"""
        self.score_file.touch()
        json.dump(self.current_high_score, self.score_file.open(mode='w'))

