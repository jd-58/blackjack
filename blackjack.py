import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
import random


class Card:
    """Creates a card object"""

    def __init__(self, value, suit):
        """Initializes a card object with a value and a suit/"""
        self._value = value
        self._suit = suit
        self._image = None

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
        self._bankroll = 1000

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


user1 = User("jacob")
deck = Deck()
deck.shuffle_deck()


def draw_cards_button():
    user1.draw_user_card(deck, 2)
    print(user1.show_hand())
    return user1.get_hand()


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
button = Button(
    screen,
    screen_width // 2 - 50,  # X coordinate of the top-left corner
    100,  # Y coordinate of the top-left corner
    150,
    75,
    text='Hello',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=draw_cards_button
)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Game code here
    button.draw()

    pygame.display.flip()

    pw.update(events)
    clock.tick(60)

pygame.quit()
