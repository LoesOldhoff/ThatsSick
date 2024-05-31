"""
ThatsSick
First draft SIR simulation, for use in education.
Made at the Hanze university of Applied Sciences.

Version: 1
Author: Loes Oldhoff
"""
import random
import math
import pygame
import pygame_widgets
from pygame.locals import *  #Needed for Color() ??
from hud import Hud
from entity import Entity

# pygame setup
pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
DT = 0 #delta time


class World:
    """
    World controls the simulation.
    It contains a list of entities and handles controlling and
    displaying them, as well as regulating the interactions between
    them and the behaviour of the 'disease'.
    The disease has no class of its own, it's behaviour is handled
    by World, and individual Entity Objects regulate their own health.
    """
    def __init__(self, thehud):
        self.hud = thehud
        self.entities = []
        for _ in range(self.hud.settings['ENTITIES_TOTAL']):
            self.entities.append(Entity(SCREEN_WIDTH, SCREEN_HEIGHT,
                                        self.hud.settings['DISEASE_SPREAD'],
                                        self.hud.settings['ENTITY_CURE_SPEED']))
        for i in range(self.hud.settings['ENTITIES_START_INFECTED']):
            self.entities[i].infect()

    def run(self):
        """
        Runs the simulation. Moves all entities and updates their status
        each tick. Also spreads disease and applies social distancing.
        """
        for entity in self.entities:
            entity.go_to_destination_w_velocity()
            if entity.infected and not entity.immune:
                entity.update_status()
        self.social_distance()
        self.spread_disease()

    def draw_entities(self):
        """
        Draws all entities in the simulation
        """
        for entity in self.entities:
            pygame.draw.circle(SCREEN, entity.color, (entity.x, entity.y), entity.size)
            if entity.infected:
                pygame.draw.circle(SCREEN, entity.color, (entity.x, entity.y), entity.active_spread, 1)

    def spread_disease(self):
        """
        Can be used to spread the disease within a World simulation.
        """
        for entity in self.entities:
            if entity.infected:
                # If an entity is infected, check all other entities to find
                # the ones in the infected's radius
                for otherentity in self.entities:
                    if otherentity.immune:
                        continue
                    dx = entity.x - otherentity.x
                    dy = entity.y - otherentity.y
                    dist = math.sqrt(dx**2 + dy**2)
                    # Calculate infection chance for close entities
                    if dist < entity.active_spread and dist != 0:
                        if random.randint(0, 500) < self.hud.settings['INFECTION_CHANCE']:
                            # And infect em!
                            otherentity.infect()

    def social_distance(self):
        """
        Can be used to make Entities avoid each other.
        Change 'distancing_strength' to control the strength of this effect.
        Directly alters the velocity (and thus positions) of Entities in World.
        """
        # Check distance between all entities
        for entity in self.entities:
            for otherentity in self.entities:
                dx = entity.x - otherentity.x
                dy = entity.y - otherentity.y
                dist = math.sqrt(dx**2 + dy**2)
                # Apply force when two entities are too close
                if dist < self.hud.settings['SOCIAL_DISTANCING_DISTANCE']:
                    entity.vx += (entity.x - otherentity.x) * self.hud.settings['SOCIAL_DISTANCING_STRENGTH']
                    entity.vy += (entity.y - otherentity.y) * self.hud.settings['SOCIAL_DISTANCING_STRENGTH']


# class Hud:
#     """
#     Hud handles displaying the Hud (All buttons/sliders in front of the simulation)
#     Also hold the 'settings' and regulates user interaction with the simulation
#     """
#     def __init__(self):
#         # Settings
#         self.settings = {
#             'SOCIAL_DISTANCING_STRENGTH': 0.1,  # Works best between 0 and 1
#             'SOCIAL_DISTANCING_DISTANCE': 10,  # Radius in pixels
#             'INFECTION_CHANCE': 5,  # in 1000 per frame
#             'ENTITIES_TOTAL': 250,
#             'ENTITIES_START_INFECTED': 5,  # Must be less than ENTITIES_TOTAL
#             'DISEASE_SPREAD': 30,  # Radius in pixels
#             'ENTITY_CURE_SPEED': 10,
#         }
#
#         # Restart button
#         self.button_y = 0
#         self.button_x = 0
#         self.button_width = 80
#         self.button_height = 30
#         self.color = Color(200, 0, 0)
#
#         # Slider box
#         self.slider_box_x = 0
#         self.slider_box_y = 0
#         self.slider_box_width = 0
#         self.slider_box_height = 0
#
#         self.find_positions()
#
#         self.sdstrength_text = TextBox(screen, self.slider_box_x + 10, self.slider_box_y + 20, 100, 1, fontSize=15)
#         self.sdstrength_text.setText("Social Distancing")
#         self.sdstrength_slider = Slider(screen, self.slider_box_x + 10, self.slider_box_y + 20, 100, 5, min=1, max=100, step=1)
#         self.sdstrength_output = TextBox(screen, self.slider_box_x + 120, self.slider_box_y + 5, 25, 25, fontSize=15)
#
#         self.sddistance_text = TextBox(screen, self.slider_box_x + 10, self.slider_box_y + 45, 100, 1, fontSize=15)
#         self.sddistance_text.setText("Social Distance")
#         self.sddistance_slider = Slider(screen, self.slider_box_x + 10, self.slider_box_y + 45, 100, 5, min=1, max=50, step=1)
#         self.sddistance_output = TextBox(screen, self.slider_box_x + 120, self.slider_box_y + 30, 25, 25, fontSize=15)
#
#         self.diseasespread_text = TextBox(screen, self.slider_box_x + 10, self.slider_box_y + 70, 100, 1, fontSize=15)
#         self.diseasespread_text.setText("Disease Spread")
#         self.diseasespread_slider = Slider(screen, self.slider_box_x + 10, self.slider_box_y + 70, 100, 5, min=1, max=50, step=1)
#         self.diseasespread_output = TextBox(screen, self.slider_box_x + 120, self.slider_box_y + 55, 25, 25, fontSize=15)
#
#         self.curespeed_text = TextBox(screen, self.slider_box_x + 10, self.slider_box_y + 95, 100, 1, fontSize=15)
#         self.curespeed_text.setText("Cure Speed")
#         self.curespeed_slider = Slider(screen, self.slider_box_x + 10, self.slider_box_y + 95, 100, 5, min=1, max=30, step=1)
#         self.curespeed_output = TextBox(screen, self.slider_box_x + 120, self.slider_box_y + 80, 25, 25, fontSize=15)
#
#     def find_positions(self):
#         # Restart button
#         self.button_y = SCREEN_HEIGHT - self.button_height - 10
#         self.button_x = SCREEN_WIDTH/2 - (self.button_width/3)
#
#         # Slider Box
#         self.slider_box_x = int(SCREEN_WIDTH/100)
#         self.slider_box_y = int(SCREEN_HEIGHT - (SCREEN_HEIGHT/3))
#         self.slider_box_width = SCREEN_WIDTH/6
#         self.slider_box_height = SCREEN_HEIGHT - int(SCREEN_HEIGHT - (SCREEN_HEIGHT/3)) - 10
#
#     def draw_hud(self):
#         # Draw Rerun Button
#         font = pygame.font.Font(None, 30)
#         text = font.render("Restart", True, Color(0, 20, 20))
#         pygame.draw.rect(screen, self.color, Rect(self.button_x, self.button_y, self.button_width, self.button_height))
#
#         # Draw Sliderbox
#         pygame.draw.rect(screen, Color(200, 150, 150), Rect(self.slider_box_x, self.slider_box_y, self.slider_box_width, self.slider_box_height))
#
#         # Draw Sliders
#         self.sdstrength_output.setText(self.sdstrength_slider.getValue())
#         self.settings['SOCIAL_DISTANCING_STRENGTH'] = self.sdstrength_slider.getValue() / 100
#         self.sdstrength_slider.draw()
#         self.sdstrength_output.draw()
#
#         self.sddistance_output.setText(self.sddistance_slider.getValue())
#         self.settings['SOCIAL_DISTANCING_DISTANCE'] = self.sddistance_slider.getValue()
#         self.sddistance_slider.draw()
#         self.sddistance_output.draw()
#
#         self.diseasespread_output.setText(self.diseasespread_slider.getValue())
#         self.settings['DISEASE_SPREAD'] = self.diseasespread_slider.getValue()
#         self.diseasespread_slider.draw()
#         self.diseasespread_output.draw()
#
#         self.curespeed_output.setText(self.curespeed_slider.getValue())
#         self.settings['ENTITY_CURE_SPEED'] = self.curespeed_slider.getValue()
#         self.curespeed_slider.draw()
#         self.curespeed_output.draw()
#
#         # Blit it
#         screen.blit(text, (self.button_x + 5, self.button_y + 5))
#
#     def get_rect(self):
#         return Rect(self.button_x, self.button_y, self.button_width, self.button_height)

#Creating the 'World' object. Parameters control the number of entities in the simulation
#as well as the amount of entities that start the simulation 'infected'
thehud = Hud(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
sim = World(thehud)

# This while loop handles the display and runs the simulation
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            # checks if mouse position is over the button
            if sim.hud.get_rect().collidepoint(mouse_pos):
                sim = World(thehud)
                print(thehud.settings)
    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill("black")
    # sim = World Object. Controls and draws the simulated entities.
    sim.run()
    sim.draw_entities()
    sim.hud.draw_hud()
    pygame_widgets.update(events)
    pygame.display.flip()

    # Control frames per second by changing global parameter DT (delta time)
    DT = clock.tick(60) / 1000

pygame.quit()