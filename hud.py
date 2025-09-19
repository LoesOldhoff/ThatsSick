import pygame
from pygame.locals import Color, Rect
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


class Hud:
    """
    Hud handles displaying the Hud (All buttons/sliders in front of the simulation)
    Also holds the 'settings' and regulates user interaction with the simulation
    """
    def __init__(self, screen, screen_width, screen_height):
        # Get screen
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

        # Slider box
        self.slider_box_x = 0
        self.slider_box_y = 0
        self.slider_box_width = 0
        self.slider_box_height = 0

        # Find position of elements based on screen dimensions
        self.find_positions()

        #TODO function this
        self.sdstrength_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 20, 100, 5, min=1, max=10, step=1)
        self.sddistance_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 45, 100, 5, min=1, max=50, step=1)
        self.diseasespread_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 70, 100, 5, min=1, max=50, step=1)
        self.curespeed_slider = Slider(self.screen, self.slider_box_x + 10, self.slider_box_y + 95, 100, 5, min=1, max=30, step=1)
        #TODO (Maybe make custom sliders I don't trust this widgets library)

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
        rerunfont = pygame.font.Font(None, 30)
        text = rerunfont.render("Restart", True, Color(0, 20, 20))
        pygame.draw.rect(self.screen, Color(200, 0, 0), Rect(self.button_x, self.button_y, self.button_width, self.button_height))
        self.screen.blit(text, (self.button_x + 5, self.button_y + 5))

        # Draw Sliderbox
        pygame.draw.rect(self.screen, Color(200, 150, 150), Rect(self.slider_box_x, self.slider_box_y, self.slider_box_width, self.slider_box_height))

        # Draw Sliders
        #TODO function this as well
        labelfont = pygame.font.Font(None, 18)

        sddistancingtext = labelfont.render("Social Distancing", True, Color(0, 20, 20))
        sdsetting = labelfont.render(str(self.sdstrength_slider.getValue()), True, Color(0, 20, 20))
        self.settings['SOCIAL_DISTANCING_STRENGTH'] = self.sdstrength_slider.getValue() / 100
        self.screen.blit(sddistancingtext, (self.slider_box_x + 10, self.slider_box_y + 5))
        self.screen.blit(sdsetting, (self.slider_box_x + 125, self.slider_box_y + 15))


        sddistancetext = labelfont.render("Social Distance", True, Color(0, 20, 20))
        sddistancesetting = labelfont.render(str(self.sddistance_slider.getValue()), True, Color(0, 20, 20))
        self.settings['SOCIAL_DISTANCING_DISTANCE'] = self.sddistance_slider.getValue()
        self.screen.blit(sddistancesetting, (self.slider_box_x + 125, self.slider_box_y + 40))
        self.screen.blit(sddistancetext, (self.slider_box_x + 10, self.slider_box_y + 30))

        spreadtext = labelfont.render("Disease Spread", True, Color(0, 20, 20))
        spreadsetting = labelfont.render(str(self.diseasespread_slider.getValue()), True, Color(0, 20, 20))
        self.settings['DISEASE_SPREAD'] = self.diseasespread_slider.getValue()
        self.screen.blit(spreadsetting, (self.slider_box_x + 125, self.slider_box_y + 65))
        self.screen.blit(spreadtext, (self.slider_box_x + 10, self.slider_box_y + 55))

        curespeedtext = labelfont.render("Cure Speed", True, Color(0, 20, 20))
        curespeedsetting = labelfont.render(str(self.curespeed_slider.getValue()), True, Color(0, 20, 20))
        self.settings['ENTITY_CURE_SPEED'] = self.curespeed_slider.getValue()
        self.screen.blit(curespeedsetting, (self.slider_box_x + 125, self.slider_box_y + 90))
        self.screen.blit(curespeedtext, (self.slider_box_x + 10, self.slider_box_y + 80))

        #self.sddistance_output.setText(str(self.sddistance_slider.getValue()))
        #self.sdstrength_output.setText('Hello World')
        #self.diseasespread_output.setText(str(self.diseasespread_slider.getValue()))
        #self.curespeed_output.setText(str(self.curespeed_slider.getValue()))

    def get_restart_rect(self):
        """ Returns the location of the Restart Button """
        return Rect(self.button_x, self.button_y, self.button_width, self.button_height)
