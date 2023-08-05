from Mind import Orientation, Existence
import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))

pygame.display.set_caption('test, arrows for moving')

gravity = Existence.gravity(0.1, 5)

def down(self, cld, obj):
    self.move(0, -cld)
    self.fy = 0

collision = Existence.collider([None, down, None, None, None], "wall")

player = Existence.mov_type(None, pygame.image.load("player.png"), logic=Existence.Subject+Existence.opt_size+gravity+collision)

Map = Orientation.tiled_map('first_level', [{}, {}, {"player": player}])

p = Map.clone_obj("player")

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
pygame.quit()
