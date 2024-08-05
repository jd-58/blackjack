import pygame
import random

"""
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    #Render Game here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()"""


class Card:
    """Creates a card object"""

    def __init__(self, value, suit):
        """Initializes a card object with a value and a suit/"""
        self._value = value
        self._suit = suit

    def get_card(self):
        """Returns the string card value and then suit"""
        return str(self._value) + str(self._suit)


class Deck:
    """Creates a deck object"""

    def __init__(self):
        """Initializes a standard 52 card deck."""
        self._cards = []

    def create_deck(self):
        """Creates 52 card objects and adds them to the deck"""
        for suit in ("spades", "diamonds", "clubs", "hearts"):
            for value in range(2, 15):
                self._cards.append(Card(value, suit))

    def get_deck(self):
        """Returns the current deck"""
        return self._cards


testcard = Card("3", "clubs")
print(testcard.get_card())

deck = Deck()
deck.create_deck()
finished_deck = deck.get_deck()
print(finished_deck[12].get_card())
