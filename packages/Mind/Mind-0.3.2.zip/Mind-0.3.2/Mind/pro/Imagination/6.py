from Mind import Imagination
import pygame

screen = pygame.display.set_mode((800, 500))

pygame.init()

font = pygame.font.SysFont(None, 50)

Places = [Imagination.PLACE(True)] + [Imagination.PLACE()]

Game = Imagination.Game(Places[0])

Main_menu = Imagination.Vertical_menu(Places[0], 150)
keyboard = Main_menu.get_keyboard()
keyboard.extend([(pygame.K_ESCAPE, "quit")])

Main_menu.add_option(Imagination.text_option(font, "Start", (255, 0, 0), Main_menu, pos_do=Imagination.ch_color((0, 0, 0)), anti_pos_do=Imagination.reset()), True)
Main_menu.add_option(Imagination.text_option(font, "Options", (0, 255, 0), Main_menu, Imagination.link(Places[1]), pos_do=Imagination.ch_color((0, 0, 0)), anti_pos_do=Imagination.reset()))
Main_menu.add_option(Imagination.text_option(font, "Quit", (0, 0, 255), Main_menu, Imagination.Quit, pos_do=Imagination.ch_color((0, 0, 0)), anti_pos_do=Imagination.reset()))
Main_menu.set_options()

Main_menu.set_game(Game)

Options = Imagination.Vertical_menu(Places[1], 150, keyboard=keyboard)
Options.add_option(Imagination.text_option(font, "Sound", (255, 255, 0), Options, pos_do=Imagination.ch_color((0, 0, 0)), anti_pos_do=Imagination.reset()), True)
Options.add_option(Imagination.text_option(font, "Back", (255, 0, 255), Options, Imagination.link(Places[0]), pos_do=Imagination.ch_color((0, 0, 0)), anti_pos_do=Imagination.reset()))
Options.set_options()

Options.set_game(Game)

while Game.run():
    if keyboard.keys["quit"]:
        Game.kill()

    screen.fill((255, 255, 255))

    Game.blit()

    pygame.display.flip()

pygame.quit()
