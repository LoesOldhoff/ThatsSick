import random
from pygame.locals import Color


class Entity:
    """
    Models an entity (human) in the SIR model.
    Entity contains information about its own position in the 'World'
    (aka on the screen) but besides that contains only information about its own status.
    Needs to be given Screen width and height upon initiation in order to generate correct coordinates.
    It is unable to interact with other Entity object.
    Each Entity has a destination it will try to move towards. Once its destination is reached
    a new destination will be generated.
    """
    def __init__(self, screen_width, screen_height, size=4, color=Color(0, 255, 255)):
        # Position and destination
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.x_destination = random.randint(10, screen_width - 10)
        self.y_destination = random.randint(10, screen_height - 10)
        # Speed and velocity
        self.vx = 0
        self.vy = 0
        self.maxspeed = 3
        self.minspeed = 0.5
        self.drag = 0.5
        # Looks
        self.size = size
        self.color = color
        # Status
        self.infected = False
        self.immune = False
        self.active_spread = 0
        self.infection_time = random.randint(500, 5000)
        self.hp = random.randint(500, 5000)
        self.alive = True

    def update_status(self, cure_speed, deadliness):
        """
        Updates the Entities' status. This function should only be called on
        entities that have been infected to check the growth of their infection
        radius and count down their time-till-cured.
        Will render entities 'immune' once their timers run out.
        """
        self.hp -= deadliness
        if self.hp < 0:
            self.die()
            return

        self.infection_time -= cure_speed
        if self.infection_time <= 0:
            self.immune = True
            self.color = Color(0, 100, 200)
            self.infected = False

    def manual_move(self, x, y):
        """ Applies force to Entity """
        self.x += x
        self.y += y

    def go_to_destination_w_velocity(self):
        #TODO implement a different random walk (Maybe each entity has a home location they return to)
        """
        Implements a 'random walk' by assigning Entity a 'destination' to move to.
        Destinations are randomly assigned within the boundaries of the screen
        (minus a small margin). Once an Entity gets close enough to its destination
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
        """ Infect the entity, changing its color (to orange, currently) """
        self.infected = True
        self.color = Color(250, 200, 0)

    def die(self):
        """ Kill the entity, changing its color (to grey, currently) """
        self.alive = False
        self.immune = False
        self.infected = False
        self.color = Color(100, 100, 100)