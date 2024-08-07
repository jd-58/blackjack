import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

import random
import pygame.freetype


# To try and embedd my game in browser: https://pygame-web.github.io/#demos-on-itchio

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

    def draw_card(self, is_face_up):
        """Draws a card and removes it from the deck, defaults to face up card"""
        drawn_card = self._cards.pop()
        drawn_card.set_face_up(is_face_up)
        return drawn_card

    def add_card_to_deck(self, card_to_add):
        """Adds cards to the deck"""
        self._cards.append(card_to_add)

    def get_deck_size(self):
        """Returns the current size of the deck"""
        return len(self._cards)


class User:
    """Creates a user"""

    def __init__(self, username):
        """Initializes a user object with a given username and empty hand"""
        self._username = username
        self._hand = []
        self._bankroll = 1000
        self._score = 0
        self._turn_result = 'in-progress'

    def draw_user_card(self, game_deck, number_of_cards, is_face_up=True):
        """Adds a specified number of cards to the user's hand from the deck. Make sure the deck is shuffled."""
        i = 0
        while i < number_of_cards:
            self._hand.append(game_deck.draw_card(is_face_up))
            i += 1

    def get_hand(self):
        """Returns the user's hand"""
        return self._hand

    def get_turn_result(self):
        """Returns win if the user has won the hand, or loss if they have not"""
        return self._turn_result

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

    def set_turn_result(self, new_turn_result):
        """Changes the user's current turn result"""
        self._turn_result = new_turn_result

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

    def clear_hand(self):
        """Clears the user's hand, returns the cards to the deck, and shuffles the deck"""
        for card in self._hand:
            deck.add_card_to_deck(card)
        deck.shuffle_deck()
        self._hand = []


user1 = User("jacob")
deck = Deck()
deck.shuffle_deck()

dealer = User("Dealer")

blackjack = 21


def draw_cards_button_func():
    deck.shuffle_deck()
    user1.draw_user_card(deck, 2, True)
    dealer.draw_user_card(deck, 1, True)
    dealer.draw_user_card(deck, 1, False)
    dealer_hand = dealer.get_hand()
    initial_score_check()


def check_dealer_score():
    if dealer.get_hand_value() > 17:
        for card in dealer.get_hand():
            card.set_face_up(True)


def hit():
    user1.draw_user_card(deck, 1, True)
    if user1.get_hand_value() > 21:
        user1.set_turn_result('loss')
        dealer.set_turn_result('win')


def stand():
    dealer_hand = dealer.get_hand()
    dealer_hand[1].set_face_up(True)
    while dealer.get_hand_value() <= 16:
        dealer.draw_user_card(deck, 1, True)
    final_score_check()


def initial_score_check():
    if (dealer.get_hand_value() == 21 and user1.get_hand_value() != 21  # Dealer gets 21 and player does not
            or user1.get_hand_value() > 21):  # User busts
        dealer.set_turn_result('win')
        user1.set_turn_result('loss')
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:  # Player gets 21 and dealer does not
        dealer.set_turn_result('loss')
        user1.set_turn_result('win')


def clear_table():
    user1.set_turn_result('in-progress')
    user1.clear_hand()
    dealer.set_turn_result('in-progress')
    dealer.clear_hand()


def final_score_check():
    if ((user1.get_hand_value() == 21 and dealer.get_hand_value() != 21  # User blackjack
         or dealer.get_hand_value() < user1.get_hand_value() <= 21)  # Neither bust, user has higher hand
            or dealer.get_hand_value() > 21 >= user1.get_hand_value()):  # Dealer bust, user does not
        user1.set_turn_result('win')
        dealer.set_turn_result('loss')
    elif (user1.get_hand_value() > 21  # User bust
          or user1.get_hand_value() < dealer.get_hand_value() <= 21):  # Neither bust, dealer has higher hand
        user1.set_turn_result('loss')
        dealer.set_turn_result('win')


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

stand_button = Button(
    screen,
    screen_width // 2 + 500,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    75,
    25,
    text='Stand',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=stand
)

clear_button = Button(  # TEMPORARY BUTTON
    screen,
    screen_width // 2 - 500,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    75,
    25,
    text='Clear',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=clear_table
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

    draw_text("Your cards are: ", text_font, white, screen_width // 2 - 25, 550)
    draw_text(str(user1.show_hand()), text_font, white, screen_width // 2 - 25, 600)

    draw_text("Your score: ", text_font, white, screen_width // 2 + 250, 550)
    draw_text(str(user1.get_hand_value()), text_font, white, screen_width // 2 + 350, 550)

    draw_text("Dealer's cards are: ", text_font, (255, 255, 255), screen_width // 2 - 25, 100)
    draw_text(str(dealer.show_hand()), text_font, (255, 255, 255), screen_width // 2 - 25, 150)

    # draw_text("Dealer's score: ", text_font, white, screen_width // 2 + 250, 100)
    # draw_text(str(dealer.get_hand_value()), text_font, white, screen_width // 2 + 350, 100)

    draw_text("Turn result: ", text_font, white, screen_width // 2 - 350, 100)
    draw_text(str(user1.get_turn_result()), text_font, white, screen_width // 2 - 250, 100)

    draw_text("Cards in deck: ", text_font, white, screen_width // 2 - 350, 300)
    draw_text(str(deck.get_deck_size()), text_font, white, screen_width // 2 - 250, 300)

    deal_cards_button.draw()
    hit_button.draw()
    stand_button.draw()
    clear_button.draw()

    pygame.display.flip()
    pygame.display.update()

    # check_dealer_score()

    pw.update(events)
    clock.tick(30)

pygame.quit()
