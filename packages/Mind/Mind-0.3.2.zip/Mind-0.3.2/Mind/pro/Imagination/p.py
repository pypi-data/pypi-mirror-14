import random

import pygame

screen = pygame.display.set_mode((800, 500))
running = True

pygame.init()

font = pygame.font.SysFont(None, 50)

while running:
    event_get = pygame.event.get()
    for event in event_get:
        if event.type == pygame.QUIT:
            running = False

    screen.fill(color)

    pygame.display.flip()

pygame.quit()
