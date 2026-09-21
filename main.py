"""
ThatsSick
First draft SIR simulation, for use in education.
Made at the Hanze university of Applied Sciences.

Version: 1
Author: Loes Oldhoff
"""
import pygame
import pygame_widgets
from hud import Hud
from world import World
import asyncio

# pygame setup
pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
DT = 0  # delta time

thishud = Hud(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
world = World(thishud, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)


async def main(sim):
#def main(sim):
    running = True
    # This while loop handles the display and runs the simulation
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                # checks if mouse position is over the button
                if sim.hud.get_restart_rect().collidepoint(mouse_pos):
                    sim = World(thishud, SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT)
                    #print(sim.hud.settings)
        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("black")
        # sim = World Object. Controls and draws the simulated entities.
        sim.run()
        sim.draw_entities()
        sim.hud.draw_hud()
        pygame_widgets.update(events)
        pygame.display.update()
        # Control frames per second by changing global parameter DT (delta time)
        DT = clock.tick(60) / 1000
        #await asyncio.sleep(0)

#main(world)
asyncio.run(main(world))
#pygame.quit()