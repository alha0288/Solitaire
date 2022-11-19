import pygame
from button import Button
import sys


BG = pygame.image.load("cards/Background.png")

def get_font(size):
    return pygame.font.Font("cards/font1.ttf", size)

def main_menu(SCREEN):
    while True:
        SCREEN.blit(BG, (0, 0))
        pygame.display.set_caption("Welcome")
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(65).render("MENU", True, "#00FF00")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 75))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MENU", True, "#00FF00")
        MENU_RECT = MENU_TEXT.get_rect(center=(335, 75))

        PLAY_BUTTON = Button(image=pygame.image.load("cards/backRect.png"), pos=(335, 225),
                             text_input="NEW GAME", font=get_font(40), base_color="yellow", hovering_color="red")

        RULES_BUTTON = Button(image=pygame.image.load("cards/backRect.png"), pos=(335, 400),
                              text_input="Instructions", font=get_font(50), base_color="yellow", hovering_color="red")

        QUIT_BUTTON = Button(image=pygame.image.load("cards/backRect.png"), pos=(335, 575),
                             text_input="Exit", font=get_font(50), base_color="yellow", hovering_color="red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, RULES_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from main import play
                    play()
                if RULES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from main import Rules
                    Rules()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
