import pygame
from pygame.locals import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class Hud:
    """
    Hud handles displaying the Hud (All buttons/sliders in front of the simulation)
    Also hold the 'settings' and regulates user interaction with the simulation
    """
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        # Settings
        self.settings = {
            'SOCIAL_DISTANCING_STRENGTH': 0.1,  # Works best between 0 and 1
            'SOCIAL_DISTANCING_DISTANCE': 10,  # Radius in pixels
            'INFECTION_CHANCE': 5,  # in 1000 per frame
            'ENTITIES_TOTAL': 250,
            'ENTITIES_START_INFECTED': 5,  # Must be less than ENTITIES_TOTAL
            'DISEASE_SPREAD': 30,  # Radius in pixels
            'ENTITY_CURE_SPEED': 10,
        }

        # Restart button
        self.button_y = 0
        self.button_x = 0
        self.button_width = 80
        self.button_height = 30
        self.color = Color(200, 0, 0)

        # Slider box
        self.slider_box_x = 0
        self.slider_box_y = 0
        self.slider_box_width = 0
        self.slider_box_height = 0

        # Find position of elements based on screen dimensions
        self.find_positions()

        self.sdstrength_text = TextBox(self.screen, self.slider_box_x + 10, self.slider_box_y + 20, 100, 1, fontSize=15)
        self.sdstrength_text.setText("Social Distancing")
        self.sdstrength_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 20, 100, 5, min=1, max=10, step=1)
        self.sdstrength_output = TextBox(self.screen, self.slider_box_x + 120, self.slider_box_y + 5, 25, 25, fontSize=15)

        self.sddistance_text = TextBox(self.screen, self.slider_box_x + 10, self.slider_box_y + 45, 100, 1, fontSize=15)
        self.sddistance_text.setText("Social Distance")
        self.sddistance_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 45, 100, 5, min=1, max=50, step=1)
        self.sddistance_output = TextBox(self.screen, self.slider_box_x + 120, self.slider_box_y + 30, 25, 25, fontSize=15)

        self.diseasespread_text = TextBox(self.screen, self.slider_box_x + 10, self.slider_box_y + 70, 100, 1, fontSize=15)
        self.diseasespread_text.setText("Disease Spread")
        self.diseasespread_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 70, 100, 5, min=1, max=50, step=1)
        self.diseasespread_output = TextBox(self.screen, self.slider_box_x + 120, self.slider_box_y + 55, 25, 25, fontSize=15)

        self.curespeed_text = TextBox(self.screen, self.slider_box_x + 10, self.slider_box_y + 95, 100, 1, fontSize=15)
        self.curespeed_text.setText("Cure Speed")
        self.curespeed_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 95, 100, 5, min=1, max=30, step=1)
        self.curespeed_output = TextBox(self.screen, self.slider_box_x + 120, self.slider_box_y + 80, 25, 25, fontSize=15)

    def find_positions(self):
        """
        Uses the dimensions of the screen to find the coordinates for various hud
        elements. Currently positions:
        - Restart button
        - Slider box

        Meant to be run once upon Instance Creation
        """
        # Restart button
        self.button_y = self.screen_height - self.button_height - 10
        self.button_x = self.screen_height/2 - (self.button_width/3)

        # Slider Box
        self.slider_box_x = int(self.screen_width/100)
        self.slider_box_y = int(self.screen_height - (self.screen_height/3))
        self.slider_box_width = self.screen_width/6
        self.slider_box_height = self.screen_height - int(self.screen_height - (self.screen_height/3)) - 10

    def draw_hud(self):
        """
        Draws the various hud elements. Currently draws:
        - Rerun Button
        - Sliderbox
        - Sliders & slider elements (4)
        """

        # Draw Rerun Button
        font = pygame.font.Font(None, 30)
        text = font.render("Restart", True, Color(0, 20, 20))
        pygame.draw.rect(self.screen, self.color, Rect(self.button_x, self.button_y, self.button_width, self.button_height))

        # Draw Sliderbox
        pygame.draw.rect(self.screen, Color(200, 150, 150), Rect(self.slider_box_x, self.slider_box_y, self.slider_box_width, self.slider_box_height))

        # Draw Sliders
        self.sdstrength_output.setText(self.sdstrength_slider.getValue())
        self.settings['SOCIAL_DISTANCING_STRENGTH'] = self.sdstrength_slider.getValue() / 100
        self.sdstrength_slider.draw()
        self.sdstrength_output.draw()

        self.sddistance_output.setText(self.sddistance_slider.getValue())
        self.settings['SOCIAL_DISTANCING_DISTANCE'] = self.sddistance_slider.getValue()
        self.sddistance_slider.draw()
        self.sddistance_output.draw()

        self.diseasespread_output.setText(self.diseasespread_slider.getValue())
        self.settings['DISEASE_SPREAD'] = self.diseasespread_slider.getValue()
        self.diseasespread_slider.draw()
        self.diseasespread_output.draw()

        self.curespeed_output.setText(self.curespeed_slider.getValue())
        self.settings['ENTITY_CURE_SPEED'] = self.curespeed_slider.getValue()
        self.curespeed_slider.draw()
        self.curespeed_output.draw()

        # Blit it
        self.screen.blit(text, (self.button_x + 5, self.button_y + 5))

    def get_restart_rect(self):
        """ Returns the location of the Restart Button """
        return Rect(self.button_x, self.button_y, self.button_width, self.button_height)
