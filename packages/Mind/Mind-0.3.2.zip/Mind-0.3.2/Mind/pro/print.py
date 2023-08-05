import pygame
from Mind import Imagination

screen = pygame.display.set_mode((500, 500))

pygame.init()

printer = Imagination.printer(20, 30, pygame.font.SysFont("Arial", 30), 30)

print("Hello world!", file=printer)
print("How are you?", file=printer)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    printer.blit()

    pygame.display.update()

pygame.quit()
