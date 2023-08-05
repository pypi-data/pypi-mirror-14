from Mind import Orientation
import pygame


class player(Orientation.Subject):
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, picture, Map, obj)
        self.picture = pygame.font.SysFont(None, 50).render('A', 1, (255, 0, 0))

pygame.init()

screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption('test, arrows for moving')

Map = Orientation.tiled_map('first_level', [{}, {}, {"player": player}])

p = Map.clone_obj("player")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p.move(0, -10)
            if event.key == pygame.K_RIGHT:
                p.move(10, 0)
            if event.key == pygame.K_DOWN:
                p.move(0, 10)
            if event.key == pygame.K_LEFT:
                p.move(-10, 0)
    screen.fill((255, 255, 255))
    Map.blit()
    pygame.display.flip()
pygame.quit()
