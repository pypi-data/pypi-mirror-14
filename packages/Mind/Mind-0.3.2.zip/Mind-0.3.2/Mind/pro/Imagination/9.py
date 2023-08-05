from Mind import Imagination
import pygame

screen = pygame.display.set_mode((800, 500))

pygame.init()

font = pygame.font.SysFont(None, 50)

Places = [Imagination.PLACE(True)] + [Imagination.PLACE()]

Game = Imagination.Game(Places[0])

definition = {"type": Imagination.text_option, "font": font, "pos_do": Imagination.joined([Imagination.ch_color((0, 0, 0)), Imagination.ch_pos((10, 0))]), "anti_pos_do": Imagination.reset()}
Game.define(**definition)
declaration = {"type": Imagination.Vertical_menu, "off": (-30, 0), "off_type": "%", "distance": 150}
Game.declare(**declaration)

Main_menu = Game.set_from(places=Places[0])
keyboard = Main_menu.get_keyboard()
keyboard.extend([(pygame.K_ESCAPE, "quit")])

Main_menu.set_from(True, text="Start", color=(255, 0, 0))
Main_menu.set_from(text="Options", color=(0, 255, 0), do=Imagination.link(Places[1]))
Main_menu.set_from(text="Quit", color=(0, 0, 255), do=Imagination.Quit)
Main_menu.set_options()

Options = Game.set_from(places=Places[1], keyboard=keyboard)

Options.set_from(True, text="Sound", color=(255, 255, 0))
Options.set_from(text="Back", color=(255, 0, 255), do=Imagination.link(Places[0]))
Options.set_options()

while Game.run():
    if keyboard.keys["quit"]:
        Game.kill()

    screen.fill((255, 255, 255))

    Game.blit()

    pygame.display.flip()

pygame.quit()
