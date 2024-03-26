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
from pygame.locals import *
from entity import Entity

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
            self.entities.append(Entity(SCREEN_WIDTH, SCREEN_HEIGHT))
        for i in range(starting_N_infected):
            self.entities[i].infect()

    def run(self):
        """
        Runs the simulation. Moves all entities and updates their status
        each tick. Also spreads disease and applies social distancing.
        """
        for entity in self.entities:
            entity.go_to_destination_w_velocity()
            if entity.infected:
                entity.update_status()
        self.social_distance()
        self.spread_disease()

    def draw_entities(self):
        """
        Draws all entities in the simulation
        """
        for entity in self.entities:
            #entity.draw()
            pygame.draw.circle(screen, entity.color, (entity.x, entity.y), entity.size)
            if entity.infected:
                pygame.draw.circle(screen, entity.color, (entity.x, entity.y), entity.active_spread, 1)

    def spread_disease(self):
        """
        Can be used to spread the disease within a World simulation.
        """
        # Set chance of infection
        infection_chance = 5 #in 1000 per frame
        for entity in self.entities:
            if entity.infected:
                # If an entity is infected, check all other entities to find
                # the ones in the infected's radius
                for otherentity in self.entities:
                    dx = entity.x - otherentity.x
                    dy = entity.y - otherentity.y
                    dist = math.sqrt(dx**2 + dy**2)
                    # Calculate infection chance for close entities
                    if dist < entity.active_spread and dist != 0:
                        if random.randint(0, 500) < infection_chance:
                            # And infect em!
                            otherentity.infect()

    def social_distance(self):
        """
        Can be used to make Entities avoid each other.
        Change 'distancing_strength' to control the strength of this effect.
        Directly alters the velocity (and thus positions) of Entities in World.
        """
        distancing_strength = 0.01
        # Check distance between all entities
        for entity in self.entities:
            for otherentity in self.entities:
                dx = entity.x - otherentity.x
                dy = entity.y - otherentity.y
                dist = math.sqrt(dx**2 + dy**2)
                # Apply force when two entities are too close
                if dist < 30:
                    entity.vx += (entity.x - otherentity.x) * distancing_strength
                    entity.vy += (entity.y - otherentity.y) * distancing_strength

#Creating the 'World' object. Parameters control the number of entities in the simulation
#as well as the amount of entities that start the simulation 'infected'
#(In this example, we start with 100 entities, 10 of which are infected)
sim = World(100, 10)

# This while loop handles the display and runs the simulation
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # sim = World Object. Controls and draws the simulated entities.
    sim.run()
    sim.draw_entities()
    pygame.display.flip()
    # Control frames per second by changing global parameter DT (delta time)
    DT = clock.tick(60) / 1000

pygame.quit()