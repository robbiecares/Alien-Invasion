class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #Ship settings
        self.ship_limit = 2

        #Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3000
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 10

        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quickly the alien point values increase
        self.score_scale = 1.5

        # Set game's default difficulty
        self.Easy = (2, 3, .5)
        self.Medium = (1.5, 3, .75)
        self.Hard = (1, 3, 1)

        self.starting_settings = self.Easy

        #Set the initial values for the choosen difficulty (game defaults to easy)
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed, self.bullet_speed, self.alien_speed = self.starting_settings

        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)