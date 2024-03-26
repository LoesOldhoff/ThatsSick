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

class OldEntity:
    """
    Models an entity (human) in the SIR model.
    Entity contains information about it's own position in the 'World'
    (aka on the screen) but besides that contains only information
    about it's own status.
    It is unable to interact with other Entity object.
    """
    def __init__(self, size=4, color=Color(0, 255, 255)):
        #Position and destination
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.x_destination = random.randint(10, SCREEN_WIDTH-10)
        self.y_destination = random.randint(10, SCREEN_HEIGHT-10)
        #Speed and velocity
        self.vx = 0
        self.vy = 0
        self.maxspeed = 3
        self.minspeed = 0.5
        self.drag = 0.5
        #Looks
        self.size = size
        self.color = color
        #Status
        self.infected = False
        self.immune = False
        self.spread = 15
        self.active_spread = 0
        self.cure_speed = 0.01
        self.infection_time = random.randint(500, 5000)

    def draw(self):
        """ Draws the Entity, plus their radius of infection once infected """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        if self.infected:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.active_spread, 1)

    def update_status(self):
        """
        Updates the Entities' status. This function should only be called on
        entities that have been infected to check the growth of their infection
        radius and count down their time-till-cured.
        Will render entities 'immune' once their timers run out.
        """
        if self.active_spread < self.spread:
            self.active_spread += 0.3
        self.infection_time -= 1
        if self.infection_time < 0:
            self.infected = False
            self.immune = True
            self.color = Color(0, 100, 200)

    def manual_move(self, x, y):
        """ Applies force to Entity """
        self.x += x
        self.y += y

    def go_to_destination(self):
        """
        Implements a 'random walk' by assigning Entity a 'destination' to move to.
        Destinations are randomly assigned within the boundaries of the screen
        (minus a small margin). Once an Entity gets close enough to it's destination
        the location resets.
        Destinations can be visualized, or not. This does not change the random walk
        behaviour.
        DEPRECATED. This function can still be called in World.run()
        instead of go_to_destination_w_velocity(), but will prevent World.social_distance()
        from functioning properly.
        """
        pygame.draw.circle(screen, Color(10, 10, 10), (self.x_destination, self.y_destination), 2)
        dx = self.x_destination - self.x
        dy = self.y_destination - self.y
        if abs(dx) <= 20 and abs(dy) <= 20:
            self.x_destination = random.randint(0, SCREEN_WIDTH)
            self.y_destination = random.randint(0, SCREEN_HEIGHT)
        if abs(dx) > self.maxspeed:
            if dx < 0:
                dx = self.maxspeed * -1
            else:
                dx = self.maxspeed
        if abs(dy) > self.maxspeed:
            if dy < 0:
                dy = self.maxspeed * -1
            else:
                dy = self.maxspeed
        if abs(dx) < self.minspeed:
            if dx < 0:
                dx = self.minspeed * -1
            else:
                dx = self.minspeed
        if abs(dy) < self.minspeed:
            if dy < 0:
                dy = self.minspeed * -1
            else:
                dy = self.minspeed

        #self.vx += dx/100
        #self.vy += dy/100
        self.x += dx/5
        self.y += dy/5

    def go_to_destination_w_velocity(self):
        """
        Implements a 'random walk' by assigning Entity a 'destination' to move to.
        Destinations are randomly assigned within the boundaries of the screen
        (minus a small margin). Once an Entity gets close enough to it's destination
        the location resets.
        Destinations can be visualized, or not. This does not change the random walk
        behaviour.
        Also implements velocity, checking Entity velocity against their maximum speed
        and implementing 'drag' to fake air resistance.
        """
        #pygame.draw.circle(screen, Color(10, 10, 10), (self.x_destination, self.y_destination), 2)
        dx = self.x_destination - self.x
        dy = self.y_destination - self.y
        self.vx += dx/400
        self.vy += dy/400
        if abs(dx) <= 40 and abs(dy) <= 40:
            self.x_destination = random.randint(10, SCREEN_WIDTH-10)
            self.y_destination = random.randint(10, SCREEN_HEIGHT-10)
        if abs(self.vx) > self.maxspeed:
            if self.vx < 0:
                self.vx = self.maxspeed * -1
            else:
                self.vx = self.maxspeed
        if abs(self.vy) > self.maxspeed:
            if self.vy < 0:
                self.vy = self.maxspeed * -1
            else:
                self.vy = self.maxspeed

        if abs(self.vy) > self.drag:
            if self.vy < 0:
                self.vy += self.drag
            else:
                self.vy -= self.drag
        if abs(self.vx) > self.drag:
            if self.vx < 0:
                self.vx += self.drag
            else:
                self.vx -= self.drag

        self.x += self.vx
        self.y += self.vy

    def infect(self):
        """ Infect the entity, changing it's color (to orange, currently) """
        self.infected = True
        self.color = Color(250, 200, 0)

class World:
    """
    World controls the simulation.
    It contains a list of entities and handles controlling and
    displaying them, as well as regulating the interactions between
    them and the behaviour of the 'disease'.
    The disease has no class of it's own, it's behaviour is handled
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