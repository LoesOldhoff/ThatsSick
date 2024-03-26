import random
from pygame.locals import *


class Entity:
    """
    Models an entity (human) in the SIR model.
    Entity contains information about it's own position in the 'World'
    (aka on the screen) but besides that contains only information
    about it's own status.
    It is unable to interact with other Entity object.
    """
    def __init__(self, screen_width, screen_height, size=4, color=Color(0, 255, 255)):
        #Position and destination
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.x_destination = random.randint(10, screen_width - 10)
        self.y_destination = random.randint(10, screen_height - 10)
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

    # def draw(self):
    #     """ Draws the Entity, plus their radius of infection once infected """
    #     pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
    #     if self.infected:
    #         pygame.draw.circle(screen, self.color, (self.x, self.y), self.active_spread, 1)

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
        #pygame.draw.circle(screen, Color(10, 10, 10), (self.x_destination, self.y_destination), 2)
        dx = self.x_destination - self.x
        dy = self.y_destination - self.y
        if abs(dx) <= 20 and abs(dy) <= 20:
            self.x_destination = random.randint(0, self.screen_width)
            self.y_destination = random.randint(0, self.screen_height)
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
            self.x_destination = random.randint(10, self.screen_width-10)
            self.y_destination = random.randint(10, self.screen_height-10)
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