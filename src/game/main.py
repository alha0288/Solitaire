from button import Button
import pygame
import sys
from game import Game
from main_menu import main_menu

pygame.init()
SCREEN = pygame.display.set_mode((670, 700))
Icon = pygame.image.load('cards/logo.png')
pygame.display.set_icon(Icon)
BG = pygame.image.load("cards/Background.png")


def get_font(size):
    return pygame.font.Font("cards/font1.ttf", size)


def play():
     while True:
         g = Game()
         g.start()


def Rules():
    while True:
        RULES_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(12).render("TO  WIN  THE GAME, YOU  NEED TO ARRANGE THE ( 52 ) CARDS   FROM ASE TO  KING. "
                                           "TO   REFRESH  THE  GAME  JUST  HIT  THE ( R )  KEY", True, "BLACK")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(335, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(335, 460),
                              text_input="BACK", font=get_font(75), base_color="Red", hovering_color="Green")

        OPTIONS_BACK.changeColor(RULES_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(RULES_MOUSE_POS):
                    main_menu(SCREEN)

        pygame.display.update()


main_menu(SCREEN)
