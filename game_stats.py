import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.starting_high_score = self.read_high_score()
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

    def read_high_score(self):
        with open('high_score.json') as f:
            self.starting_high_score = json.load(f)
        return int(self.starting_high_score)

    def write_high_score(self):
        filename = "high_score.json"
        with open(filename, "w") as f:
            json.dump(f"{self.current_high_score}", f)


