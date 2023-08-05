from Mind import Orientation, Existence
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption('test, arrows for moving')

@Existence.logic_class
class Player:
    def down(self, cld, obj):
        self.move(0, -cld)
        self.fy = 0

    collide = [None, down, None, None, None]

gravity = Existence.gravity(0.1, 5)

collision = Existence.collider2("wall")

player = Existence.mov_type(None, pygame.font.SysFont(None, 50).render('A', 1, (255, 0, 0)), logic=Existence.Subject+Player+gravity+collision)

Map = Orientation.tiled_map('first_level', [{}, {}, {"player": player}])

p = Map.clone_obj("player")

Clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p.jump()
            if event.key == pygame.K_RIGHT:
                p.move(10, 0)
            if event.key == pygame.K_DOWN:
                p.move(0, 10)
            if event.key == pygame.K_LEFT:
                p.move(-10, 0)
    screen.fill((255, 255, 255))
    Map.blit()
    pygame.display.flip()
    Clock.tick(60)
pygame.quit()
