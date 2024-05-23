"""
ThatsSick
First draft SIR simulation, for use in education.
Made at the Hanze university of Applied Sciences.
U+1F604
\U0001F605

Version: 1
Author: Loes Oldhoff
"""
import random
import math
import pygame
from pygame.locals import *  #Needed for Color() ??
import pygame_widgets
from entity import Entity

# Arbitrary numbers needed for the simulation
SOCIAL_DISTANCING_STRENGTH = 0.5  # Works best between 0 and 1
SOCIAL_DISTANCING_DISTANCE = 10  # Radius in pixels
INFECTION_CHANCE = 5  # in 1000 per frame
ENTITIES_TOTAL = 250
ENTITIES_START_INFECTED = 5  # Must be less than ENTITIES_TOTAL
DISEASE_SPREAD = 30  # Radius in pixels
ENTITY_CURE_SPEED = 10

# pygame setup
pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
    def __init__(self, N_of_entities, starting_N_infected):
        self.entities = []
        self.starting_N_infected = starting_N_infected
        for _ in range(N_of_entities):
            self.entities.append(Entity(SCREEN_WIDTH, SCREEN_HEIGHT, DISEASE_SPREAD, ENTITY_CURE_SPEED))
        for i in range(starting_N_infected):
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
            pygame.draw.circle(screen, entity.color, (entity.x, entity.y), entity.size)
            if entity.infected:
                pygame.draw.circle(screen, entity.color, (entity.x, entity.y), entity.active_spread, 1)

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
                        if random.randint(0, 500) < INFECTION_CHANCE:
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
                if dist < SOCIAL_DISTANCING_DISTANCE:
                    entity.vx += (entity.x - otherentity.x) * SOCIAL_DISTANCING_STRENGTH
                    entity.vy += (entity.y - otherentity.y) * SOCIAL_DISTANCING_STRENGTH

class Hud:
    def __init__(self):
        self.button_y = 0
        self.button_x = 0
        self.button_width = 80
        self.button_height = 30
        self.color = Color(200, 0, 0)
        self.find_position()

    def find_position(self):
        self.button_y = SCREEN_HEIGHT - self.button_height - 10
        self.button_x = SCREEN_WIDTH/2 - (self.button_width/2)

    def draw_rerun_button(self):
        font = pygame.font.Font(None, 30)
        text = font.render("Restart", True, Color(0, 20, 20))
        pygame.draw.rect(screen, self.color, Rect(self.button_x, self.button_y, self.button_width, self.button_height))
        screen.blit(text, (self.button_x + 5, self.button_y + 5))

    def get_rect(self):
        return Rect(self.button_x, self.button_y, self.button_width, self.button_height)

#Creating the 'World' object. Parameters control the number of entities in the simulation
#as well as the amount of entities that start the simulation 'infected'
sim = World(ENTITIES_TOTAL, ENTITIES_START_INFECTED)
hud = Hud()

# This while loop handles the display and runs the simulation
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            # checks if mouse position is over the button
            if hud.get_rect().collidepoint(mouse_pos):
                sim = World(ENTITIES_TOTAL, ENTITIES_START_INFECTED)
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # sim = World Object. Controls and draws the simulated entities.
    sim.run()
    sim.draw_entities()
    hud.draw_rerun_button()
    pygame.display.flip()

    # Control frames per second by changing global parameter DT (delta time)
    DT = clock.tick(60) / 1000

pygame.quit()