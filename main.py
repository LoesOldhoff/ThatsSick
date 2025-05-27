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
from hud import Hud
from entity import Entity
from typing import List

# pygame setup
pygame.init()
SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
SCREEN: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock: pygame.time.Clock = pygame.time.Clock()
running: bool = True
DT: float = 0  # delta time


class World:
    hud: Hud
    entities: List[Entity]
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
            self.entities.append(Entity(SCREEN_WIDTH, SCREEN_HEIGHT))
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
                if entity.active_spread < self.hud.settings["DISEASE_SPREAD"]:
                    entity.active_spread += 0.3
                entity.update_status(self.hud.settings['ENTITY_CURE_SPEED'])
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

    def spread_disease(self) -> None:
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
                    dx: float = entity.x - otherentity.x
                    dy: float = entity.y - otherentity.y
                    dist: float = math.sqrt(dx**2 + dy**2)
                    # Calculate infection chance for close entities
                    if dist < entity.active_spread and dist != 0:
                        if random.randint(0, 500) < self.hud.settings['INFECTION_CHANCE']:
                            # And infect em!
                            otherentity.infect()

    #TODO Reverse this behaviour in Infected for Zombie Mode
    def social_distance(self) -> None:
        """
        Can be used to make Entities avoid each other.
        Change 'distancing_strength' to control the strength of this effect.
        Directly alters the velocity (and thus positions) of Entities in World.
        """
        # Check distance between all entities
        for entity in self.entities:
            for otherentity in self.entities:
                dx: float = entity.x - otherentity.x
                dy: float = entity.y - otherentity.y
                dist: float = math.sqrt(dx**2 + dy**2)
                # Apply force when two entities are too close
                if dist < self.hud.settings['SOCIAL_DISTANCING_DISTANCE']:
                    entity.vx += (entity.x - otherentity.x) * self.hud.settings['SOCIAL_DISTANCING_STRENGTH']
                    entity.vy += (entity.y - otherentity.y) * self.hud.settings['SOCIAL_DISTANCING_STRENGTH']

thishud: Hud = Hud(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
sim: World = World(thishud)

# This while loop handles the display and runs the simulation
while running:
    events: list[pygame.event] = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos: tuple = event.pos  # gets mouse position
            # checks if mouse position is over the button
            if sim.hud.get_restart_rect().collidepoint(mouse_pos):
                sim: World = World(thishud)
                print(sim.hud.settings)
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