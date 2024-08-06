import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

import random
import pygame.freetype


class Card:
    """Creates a card object"""

    def __init__(self, value, suit, face_up=True):
        """Initializes a card object with a value and a suit/"""
        self._value = value
        self._suit = suit
        self._image = None
        self._face_up = face_up

    def get_card(self):
        """Returns the string card value and then suit"""
        if self._face_up is True:
            return str(self._value) + str(self._suit)
        else:
            return "Face Down"

    def get_face_up(self):
        """Returns a true value (default) if a card should be face up, and false if it should be face down"""
        return self._face_up

    def get_image(self):
        """Returns the image file name associated with the card"""
        return self._image

    def get_value(self):
        """Returns the value of the selected card"""
        return self._value

    def set_face_up(self, face_up_value):
        """Sets a card's face up value. True if face up, False if face down."""
        self._face_up = face_up_value

    def set_image(self, image_title):
        """Set's a card's image title."""
        self._image = image_title


class Deck:
    """Creates a deck object"""

    def __init__(self):
        """Initializes a standard 52 card deck and creates an un-shuffled deck."""
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
        self._score = 0

    def draw_user_card(self, game_deck, number_of_cards):
        """Adds a specified number of cards to the user's hand from the deck. Make sure the deck is shuffled."""
        i = 0
        while i < number_of_cards:
            self._hand.append(game_deck.draw_card())
            i += 1

    def get_hand(self):
        """Returns the user's hand"""
        return self._hand

    def get_score(self):
        """Returns the user's current score"""
        return self._score

    def get_hand_value(self):
        """Gets the value of the user's current hand"""
        current_value = 0
        for card in self._hand:
            current_value += card.get_value()
        return current_value

    def get_username(self):
        """Returns the user's current username"""
        return self._username

    def set_username(self, new_username):
        """Changes the user's username"""
        self._username = new_username

    def set_score(self, new_score):
        """Changes the user's score"""
        self._score = new_score

    def update_score(self):
        """Updates the user's score to reflect their current hand"""
        self._score = self.get_hand_value()

    def show_hand(self):
        """Returns the user's hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._hand:
            readable_card_list.append(card.get_card())
        return readable_card_list


user1 = User("jacob")
deck = Deck()
deck.shuffle_deck()

dealer = User("Dealer")

blackjack = 21


def draw_cards_button_func():
    user1.draw_user_card(deck, 2)
    dealer.draw_user_card(deck, 2)
    dealer_hand = dealer.get_hand()
    dealer_hand[1].set_face_up(False)


def check_dealer_score():
    """if dealer.get_hand_value() < 16:
        dealer.draw_user_card(deck, 1)
        print("Drawing card")"""
    if dealer.get_hand_value() > 17:
        for card in dealer.get_hand():
            card.set_face_up(True)


def hit():
    user1.draw_user_card(deck, 1)


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
deal_cards_button = Button(
    screen,
    screen_width // 2 - 50,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    125,
    25,
    text='Draw cards',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=draw_cards_button_func
)

hit_button = Button(
    screen,
    screen_width // 2 + 350,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    75,
    25,
    text='Hit',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=hit
)

white = (255, 255, 255)
blue = (0, 0, 128)

text_font = pygame.font.SysFont("Arial", 18)


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Game code here
    screen.fill("black")

    draw_text("Your cards are: ", text_font, white, screen_width//2 - 25, 550)
    draw_text(str(user1.show_hand()), text_font, white, screen_width//2 - 25, 600)

    draw_text("Your score: ", text_font, white, screen_width // 2 + 250, 550)
    draw_text(str(user1.get_hand_value()), text_font, white, screen_width // 2 + 350, 550)

    draw_text("Dealer's cards are: ", text_font, (255, 255, 255), screen_width // 2 - 25, 100)
    draw_text(str(dealer.show_hand()), text_font, (255, 255, 255), screen_width // 2 - 25, 150)

    draw_text("Dealer's score: ", text_font, white, screen_width // 2 + 250, 100)
    draw_text(str(dealer.get_hand_value()), text_font, white, screen_width // 2 + 350, 100)

    deal_cards_button.draw()
    hit_button.draw()

    pygame.display.flip()
    pygame.display.update()

    check_dealer_score()

    pw.update(events)
    clock.tick(60)

pygame.quit()
