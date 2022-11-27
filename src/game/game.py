import pygame
import sys

import self as self
from objects import *
from settings import Settings
from pygame.locals import *
import random
from main_menu import main_menu
from button import Button
from src.game.objects import Repository, MainPile, SuitPile, StartPile, Card


class DoubleClick:
    def __init__(self):
        self.double_click = pygame.time.Clock()
        self.time = 0  # Necessary to temporary store time passed after checking second down click
        self.first_click = True  # Is this the first click in the double click
        self.wasDoubleClick = False  # Was the last call to isDoubleClick() a double click

    # Implementing double click
    def isDoubleClick(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            click_time = self.double_click.tick()  # Check how long since the last click is done
            if not self.first_click:  # If it's the first click, exit function with False
                # If it's the second down click, make sure that a double click is still a possibility
                # If it is not, make this down click the first click
                # Since tick() was called, store time passed in self.time, to be added to the up click later
                if click_time > Settings.doubleSpeed:
                    self.first_click = True
                else:
                    self.time = click_time

        if event.type == MOUSEBUTTONUP and event.button == 1:
            if not self.first_click:  # If it's the second click
                click_time = self.double_click.tick()  # Get time since last click (the second down click)
                self.first_click = True  # The next click will again be first
                if click_time + self.time < Settings.doubleSpeed:  # Add the click_time and self. time and check if is it fast enough
                    self.wasDoubleClick = True
                    return True
            else:
                self.first_click = False  # If it was first up click, so the second_click is expected
        self.wasDoubleClick = False
        return False


class Game:
    def __init__(self):
        self.scoreValue = "0"
        self.OPTIONS_BACK = None
        pygame.init()  # start the game
        random.seed()  # randomly shuffle the cards

        self.screen = self.setDisplay()  # call setDisplay() function to display dimensions
        self.cards = self.loadCards()  # call loadCards() function to load all the cards
        self.piles = self.populatePiles()  # call populatePiles() to populate all the piles
        self.double_click = DoubleClick()  # call DoubleClick()  function to check the double click
        self.move_pile = Repository('Repository')  # For moving piles

    # The display dimensions are calculated given the wanted margins and card dimensions
    def setDisplay(self):
        return pygame.display.set_mode((670, 700))

    # Load the cards
    def loadCards(self):
        Card.loadBack(Settings.imageBack)
        cards = [Card(x, (0, 0)) for x in Settings.imageNames]
        random.shuffle(cards)
        return cards

    # Place the piles
    def populatePiles(self):
        piles = []
        suitpiles = []
        SuitPile.total_cards = 0

        marker = 0  # Keeps track of the last card added
        x = Settings.marginSpace  # The x_position of the pile
        y = Settings.marginSpace + Settings.imageResolution[1] + Settings.rowSpace + 60
        for i in range(1, 8):  # seven piles
            pile_name = 'Main' + str(i)
            cards = self.cards[marker: i + marker]
            piles.append(
                MainPile(pile_name, (x, y), Settings.imageBottom, Settings.tileSmallSpace, Settings.tileLargeSpace,
                         cards))

            # The suit piles are exactly above main piles (starting on the four one)
            if i > 3: suitpiles.append(SuitPile('Suit' + str(i - 3), (x, Settings.marginSpace), Settings.imageBottom))

            # tick along x and marker
            x += piles[-1].rect.w + Settings.startSpace
            marker = i + marker

        # Add the start pile
        cards = self.cards[marker: 52]  # The remaining cards
        piles.append(
            StartPile('Start', (Settings.marginSpace, Settings.marginSpace), Settings.startSpace, Settings.imageBottom,
                      cards))

        piles.extend(suitpiles)  # The last four piles always must be the suit piles
        return piles

    # simply gets the pile that was clicked
    def isClickedPile(self, event):
        for pile in self.piles:
            if pile.hasPosition(event.pos): return pile

    def get_font(self, size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("cards/font1.ttf", size)

    # The basic idea of the game loop is thus :
    # If a pile is clicked, onClick() is run
    # If onClick() returns cards, this means that these cards can be moved around (while mouse is held down)
    # The moving of cards is performed by self.move_pile
    # With a double click, the down, up, and click are read as single clicks (and still run as such)
    # The last up click will result in onDoubleClick being called
    def gameWay(self):
        SCREEN = pygame.display.set_mode((670, 700))
        pygame.display.set_caption("Press "R" to refresh the game")
        while True:
            RULES_MOUSE_POS = pygame.mouse.get_pos()
            self.OPTIONS_BACK = Button(image=None, pos=(75, 675),
                                       text_input="BACK", font=self.get_font(25), base_color="#FFD700",
                                       hovering_color="RED")
            self.OPTIONS_BACK.changeColor(RULES_MOUSE_POS)

            self.OPTIONS_Shuffel = Button(image=None, pos=(285, 675),
                                          text_input="Shuffel", font=self.get_font(25), base_color="#FFD700",
                                          hovering_color="RED")
            self.OPTIONS_Shuffel.changeColor(RULES_MOUSE_POS)

            self.OPTIONS_Score = Button(image=None, pos=(505, 675),
                                        text_input="Your Score: ", font=self.get_font(25), base_color="#FFD700",
                                        hovering_color="RED")
            self.OPTIONS_Score.changeColor(RULES_MOUSE_POS)

            self.Score = Button(image=None, pos=(600, 675),
                                text_input=self.scoreValue, font=self.get_font(25), base_color="#FFD700",
                                hovering_color="RED")
            self.Score.changeColor(RULES_MOUSE_POS)

            if self.winCondition():
                self.randomMotion(2)  # Move the piles around randomly if game has been won

            for event in pygame.event.get():
                # Check and store if a double click happened
                if (event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN) and event.button == 1:
                    self.double_click.isDoubleClick(event)

                # Check if the program is quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.OPTIONS_BACK.checkForInput(RULES_MOUSE_POS):
                        main_menu(SCREEN)
                    if self.OPTIONS_Shuffel.checkForInput(RULES_MOUSE_POS):
                        self.reset()

                # start a new game
                if event.type == KEYUP and event.key == K_r:  ########################
                    self.reset()  # call reset function to restart a new game

                # If the game has been won, reset it with a mouse click
                if self.winCondition():
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        self.reset()

                # the main of the game
                else:
                    if event.type == MOUSEBUTTONUP and event.button == 1:
                        # Is the user currently dragging cards
                        # store it as I need to recheck this variable later and the cards might have been released
                        movePileFull = self.move_pile.hasCards()

                        if movePileFull:  # If yes
                            # This finds the left most pile where the dropped cards are accepted
                            selectedPile = None
                            for pile in self.piles:
                                if pile.validAddCards(self.move_pile.cards):
                                    selectedPile = pile
                                    self.scoreValue = str(int(self.scoreValue) + 5)
                                    break

                            # If a valid pile is found, drop the cards there, otherwise return the cards
                            if selectedPile:
                                self.move_pile.addToPile(selectedPile)
                            else:
                                self.move_pile.returnCards()

                        # The double click must come after the move_pile is resolved so that no cards are even in the move_pile
                        if self.double_click.wasDoubleClick: self.onDoubleClick(event)

                        # If the move_pile was empty and no double click, just run a simple onClick on the pile
                        if not movePileFull and not self.double_click.wasDoubleClick:
                            clicked_pile = self.isClickedPile(event)

                            if clicked_pile:
                                clicked_pile.onClick(event)

                    # If mouse is held down, move those cards to the self.move_pile
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        clicked_pile = self.isClickedPile(event)

                        if clicked_pile:
                            cards_taken = clicked_pile.onClick(event)
                            if cards_taken: self.move_pile.addCards(cards_taken)

                    # if the mouse is moved, move the mouse_pile
                    if event.type == MOUSEMOTION:
                        if self.move_pile.hasCards(): self.move_pile.movePosition(event.rel)

            self.screen.fill('#013220')
            self.OPTIONS_BACK.update(SCREEN)
            self.OPTIONS_Shuffel.update(SCREEN)
            self.OPTIONS_Score.update(SCREEN)
            self.Score.update(SCREEN)
            self.draw()
            pygame.display.flip()

    # When a double click occurs, try to put that card in the suit piles
    def onDoubleClick(self, event):
        clicked_pile = self.isClickedPile(event)
        if clicked_pile:
            # onDoubleClick always returns only one card
            card_taken = clicked_pile.onDoubleClick(event)
            if card_taken:  # If a card is returned (double click was valid)
                noPlace = True  # This card right now has no home in the Suit piles
                for pile in self.piles[-4:]:  # Go through the four suit piles
                    # The False ensures that the card_taken does not have to contact the Suit piles
                    if pile.validAddCards(card_taken, False):
                        pile.addCards(card_taken)
                        noPlace = False
                    break
                # If no suit pile has been found, return the card that was double-clicked
                if noPlace: card_taken[0].pile.addCards(card_taken)

    # Draw is simple, just draw all the piles
    def draw(self):

        for pile in self.piles:
            pile.draw(self.screen)
        self.move_pile.draw(self.screen)

    def start(self):  ###############
        self.gameWay()

    # When all the cards are in the suit pile
    def winCondition(self):
        return SuitPile.total_cards == len(self.cards)

    # Moves the piles randomly in all directions
    def randomMotion(self, length):
        for pile in self.piles:
            x_move = random.randint(-length, length)
            y_move = random.randint(-length, length)
            pile.movePosition((x_move, y_move))

    def reset(self):  #############
        self.cards = self.loadCards()
        self.piles = self.populatePiles()
