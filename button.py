import pygame.font
import settings


class Button():

    def __init__(self, ai_game):
        """Initialize button attributes"""

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dims for and properties of the button
        self.width, self.height = 200, 50
        self.default_button_color = (0, 255, 0)
        self.selected_button_color = (128, 0, 128)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object & center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

    def _prep_msg(self, msg):
        """Turn a message into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, msg, color=""):
        """Draw a button on the screen & place its message on it"""

        # The button message needs to be prepped only once
        self._prep_msg(msg)

        # Draw a blank button and then draw the message on it
        self.screen.fill(self.default_button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    """
    def choice_conf(self, button_group, mouse_pos):
        #Defines the color of buttons when a button is selected from a group
        # default = self.default_button_color
        # selected = self.selected_button_color

        for button_name, button_obj in button_group.items():
            button_clicked = button_obj.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.draw_button(button_name, color=(0,128,0))

        # copy button group
        # pop/remove current button from copy
        # change color of all remaining buttons in group
    """

    """
    def confirm_click(self):
        if button_clicked:
            if button not selected:
                button color = selected
                wait .5 sec
                button color = default
    """
