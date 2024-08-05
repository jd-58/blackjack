import pygame
import random


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
        """Initializes a standard 52 card deck and creates an unshuffled deck."""
        self._cards = []
        self.create_deck()

    def create_deck(self):
        """Creates 52 card objects (un-shuffled) and adds them to the deck"""
        for suit in ("spades", "diamonds", "clubs", "hearts"):
            for value in range(2, 15):
                self._cards.append(Card(value, suit))

    def get_deck(self):
        """Returns the current deck"""
        return self._cards

    def shuffle_deck(self):
        """Takes a list of cards and shuffles them."""
        return random.shuffle(self._cards)

    def draw_card(self):
        """Draws a card and removes it from the deck"""
        return self._cards.pop()


class User:
    """Creates a user"""

    def __init__(self, username):
        """Initializes a user object with a given username and empty hand"""
        self._username = username
        self._hand = []

    def draw_user_card(self, game_deck, number_of_cards):
        """Adds a specified number of cards to the user's hand from the deck. Make sure the deck is shuffled."""
        i = 0
        while i < number_of_cards:
            self._hand.append(game_deck.draw_card())
            i += 1

    def get_hand(self):
        """Returns the user's hand"""
        return self._hand

    def show_hand(self):
        """Returns the user's hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._hand:
            readable_card_list.append(card.get_card())
        return readable_card_list


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Render Game here

    pygame.display.flip()

    clock.tick(60)

pygame.quit()