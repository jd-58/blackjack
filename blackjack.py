import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

import random
import pygame.freetype


# To try and embedd my game in browser: https://pygame-web.github.io/#demos-on-itchio

# TO-DO: add chip betting
# TO-DO: add automatic table clearing after a turn is over

class Card:
    """Creates a card object"""

    def __init__(self, value, name, suit, face_up=True, has_value_changed=False):
        """Initializes a card object with a value and a suit/"""
        self._value = value
        self._suit = suit
        self._image = None
        self._face_up = face_up
        self._name = str(name)
        self._name_and_suit = str(name) + " " + str(self._suit)
        self._has_value_changed = has_value_changed

    def get_card(self):
        """Returns the string card value and then suit"""
        if self._face_up is True:
            return self._name
        else:
            return "Face Down"

    def get_face_up(self):
        """Returns a true value (default) if a card should be face up, and false if it should be face down"""
        return self._face_up

    def get_has_value_changed(self):
        """Returns if a card (an ace) has had its value changed this turn."""
        return self._has_value_changed

    def get_name(self):
        """Returns a card's name if it is face up"""
        if self._face_up is True:
            return str(self._name)
        else:
            return "Face down"

    def get_image(self):
        """Returns the image file name associated with the card"""
        return self._image

    def get_value(self):
        """Returns the value of the selected card"""
        return self._value

    def get_name_and_suit(self):
        """Returns the card's name with the suit attached"""
        if self._face_up is True:
            return str(self._name_and_suit)
        else:
            return "Face down"

    def set_face_up(self, face_up_value):
        """Sets a card's face up value. True if face up, False if face down."""
        self._face_up = face_up_value

    def set_has_value_changed(self, new_value):
        """Changes whether a card's value has changed this turn"""
        self._has_value_changed = new_value

    def set_name(self, new_name):
        """Sets a card's display name"""
        self._name = new_name

    def set_value(self, new_value):
        """Changes a card's value"""
        self._value = new_value

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
            for value in range(2, 11):
                self._cards.append(Card(value, value, suit))  # Makes the 2-10 cards
            self._cards.append(Card(10, "jack", suit))
            self._cards.append(Card(10, "queen", suit))
            self._cards.append(Card(10, "king", suit))
            self._cards.append(Card(11, "ace", suit))

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

    def __init__(self, username, bankroll=0, amount_bet=0):
        """Initializes a user object with a given username and empty hand"""
        self._username = username
        self._hand = []
        self._bankroll = 1000
        self._score = 0
        self._turn_result = 'in-progress'
        self._bankroll = bankroll
        self._amount_bet = amount_bet

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

    def get_amount_bet(self):
        """Returns the amount the player has bet during the current hand."""
        return self._amount_bet

    def get_score(self):
        """Returns the user's current score"""
        return self._score

    def get_hand_value(self):
        """Gets the value of the user's current hand"""
        current_value = 0
        for card in self._hand:
            current_value += card.get_value()
        return current_value

    def get_bankroll(self):
        """Returns the user's bankroll"""
        return self._bankroll

    def get_username(self):
        """Returns the user's current username"""
        return self._username

    def set_username(self, new_username):
        """Changes the user's username"""
        self._username = new_username

    def set_hand(self, specified_hand):
        """Changes the user's hand. For testing purposes"""
        self._hand = specified_hand

    def update_amount_bet(self, amount_bet):
        """Updates the amount the user has bet during the current hand."""
        self._amount_bet += amount_bet

    def set_turn_result(self, new_turn_result):
        """Changes the user's current turn result"""
        self._turn_result = new_turn_result

    def update_bankroll(self, amount_to_add):
        """Changes the user's bankroll by the desired amount. A negative number lowers the bankroll"""
        self._bankroll += amount_to_add

    def set_bankroll(self, new_amount):
        """Changes the user's bankroll to a specific amount."""
        self._bankroll = new_amount

    def set_score(self, new_score):
        """Changes the user's score"""
        self._score = new_score

    def set_amount_bet(self, new_amount):
        """Changes the amount a user has bet during the current hand to a specified amount."""
        self._amount_bet = new_amount

    def update_score(self):
        """Updates the user's score to reflect their current hand"""
        self._score = self.get_hand_value()

    def show_hand(self):
        """Returns the user's hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._hand:
            readable_card_list.append(card.get_name_and_suit())
        return readable_card_list

    def clear_hand(self):
        """Clears the user's hand, returns the cards to the deck, and shuffles the deck"""
        for card in self._hand:
            deck.add_card_to_deck(card)
        deck.shuffle_deck()
        self._hand = []

    @property
    def amount_bet(self):
        return self._amount_bet


user1 = User("jacob", 1000)
deck = Deck()
deck.shuffle_deck()
pot = User("pot", 0)


#  Need separate functions for each bet, since functions assigned to a button in pygame can't have parameters.
def user_bet_one():
    """Takes 1 chip out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-1)
    user1.update_amount_bet(1)
    pot.update_bankroll(1)


def user_bet_five():
    """Takes 5 chips out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-5)
    user1.update_amount_bet(5)
    pot.update_bankroll(5)


def user_bet_twenty_five():
    """Takes 25 chips out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-25)
    user1.update_amount_bet(25)
    pot.update_bankroll(25)


def user_bet_one_hundred():
    """Takes 100 chips out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-100)
    user1.update_amount_bet(100)
    pot.update_bankroll(100)


def user_bet_five_hundred():
    """Takes 500 chips out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-500)
    user1.update_amount_bet(500)
    pot.update_bankroll(500)


def user_bet_one_thousand():
    """Takes 1000 chips out of the user's bankroll and adds it to the pot"""
    user1.update_bankroll(-1000)
    user1.update_amount_bet(1000)
    pot.update_bankroll(1000)


dealer = User("Dealer")

blackjack = 21


def draw_cards_button_func():
    deck.shuffle_deck()
    user1.draw_user_card(deck, 2, True)
    dealer.draw_user_card(deck, 1, True)
    dealer.draw_user_card(deck, 1, False)
    initial_score_check()


def draw_specific_cards_button_func():  # This is for testing certain hand combinations and results
    card1 = Card(11, 'ace', 'hearts', True)
    card2 = Card(9, '9', 'diamonds', True)
    new_hand = [card1, card2]
    user1.set_hand(new_hand)
    dealer.set_hand(new_hand)
    initial_score_check()


def check_dealer_score():
    if dealer.get_hand_value() > 17:
        for card in dealer.get_hand():
            card.set_face_up(True)


def hit():
    user1.draw_user_card(deck, 1, True)
    user_hand = user1.get_hand()
    is_ace = False
    for card in user_hand:
        if card.get_name() == 'ace':
            is_ace = True
    if user1.get_hand_value() > 21 and is_ace is True:
        for card in user1.get_hand():
            if card.get_name() == 'ace':
                if card.get_value() != 1:
                    card.set_value(1)
    if user1.get_hand_value() > 21:
        user1.set_turn_result('loss')
        dealer.set_turn_result('win')


def stand():
    dealer_hand = dealer.get_hand()
    dealer_hand[1].set_face_up(True)
    while dealer.get_hand_value() <= 16:
        check_to_change_ace(dealer)
        dealer.draw_user_card(deck, 1, True)
    final_score_check()


def initial_score_check():
    if (user1.get_hand_value() > 21  # User busts
            or dealer.get_hand_value() == 21 and user1.get_hand_value != 21):  # Dealer gets natural blackjack
        dealer.set_turn_result('win')
        user1.set_turn_result('loss')
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:  # Player gets natural 21 and dealer does not
        dealer.set_turn_result('loss')
        user1.set_turn_result('blackjack!')
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() == 21:  # Both player and dealer get natural 21
        dealer.set_turn_result('push')
        user1.set_turn_result('push')


def clear_table():
    if check_for_ace(user1) is True:
        change_ace_value_to_11(user1)
    if check_for_ace(dealer) is True:
        change_ace_value_to_11(dealer)
    user1.set_turn_result('in-progress')
    user1.clear_hand()
    dealer.set_turn_result('in-progress')
    dealer.clear_hand()


def set_ace_to_1():
    for card in user1.get_hand():
        print(card.get_name())
        if card.get_name() == 'ace':
            card.set_value(1)
            print(card.get_name_and_suit())
            print(card.get_value())
            return
    return


def set_ace_to_11():
    for card in user1.get_hand():
        if card.get_name() == 'ace':
            card.set_value(11)
            return
    return


def turn_over_check():
    if user1.get_turn_result() != 'in-progress' and dealer.get_turn_result() != 'in-progress':
        dealer_hand = dealer.get_hand()
        for card in dealer_hand:
            card.set_face_up(True)
        distribute_chips_from_pot()
        # clear_table() - need to add a pop up window that displays the result, and only moves to the next hand after
        # the user acknowledges it. currently, it moves too quick for the user to know what happened.


def change_ace_value_to_11(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace':
            card.set_has_value_changed(False)
            card.set_value(11)


def change_ace_value_to_1(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace':
            card.set_value(1)


def check_for_ace_to_change(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace' and card.get_value() == 11:
            return True


def check_for_ace(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace':
            return True


def check_to_change_ace(user):
    if user.get_hand_value() > 21 and check_for_ace(user) is True:
        change_ace_value_to_1(user)
        return


def final_score_check():
    """if user1.get_hand_value() > 21:
        if check_for_ace_to_change(user1) is True:
            change_ace_value_to_1(user1)
        else:
            user1.set_turn_result('loss')
            dealer.set_turn_result('win')
            return
    if dealer.get_hand_value() > 21:
        if check_for_ace_to_change(dealer) is True:
            change_ace_value_to_1(dealer)"""
    if 21 >= user1.get_hand_value() == dealer.get_hand_value():
        #  If the user and dealer tie
        user1.set_turn_result('push')
        dealer.set_turn_result('push')
        return
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:  # User blackjack
        user1.set_turn_result('blackjack')
        dealer.set_turn_result('loss')
    elif (dealer.get_hand_value() < user1.get_hand_value() <= 21  # Neither bust, user has higher hand
          or dealer.get_hand_value() > 21 >= user1.get_hand_value()):  # Dealer bust, user does not
        user1.set_turn_result('win')
        dealer.set_turn_result('loss')
        return
    elif (user1.get_hand_value() > 21  # User bust
          or user1.get_hand_value() < dealer.get_hand_value() <= 21  # Neither bust, dealer has higher hand
          or dealer.get_hand_value() == 21):  # Dealer blackjack
        user1.set_turn_result('loss')
        dealer.set_turn_result('win')
        return
    return


def distribute_chips_from_pot():
    if user1.get_turn_result() == 'win':
        user1.update_bankroll(2 * user1.get_amount_bet())
        pot.set_bankroll(0)
        user1.set_amount_bet(0)
    elif user1.get_turn_result() == 'blackjack':
        user1.update_bankroll(2.5 * user1.get_amount_bet())
        pot.set_bankroll(0)
        user1.set_amount_bet(0)
    elif user1.get_turn_result() == 'loss':
        pot.set_bankroll(0)
        user1.set_amount_bet(0)


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

deal_specific_cards_button = Button(  # For testing
    screen,
    screen_width // 2 - 250,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    200,
    25,
    text='Draw Specific cards',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=draw_specific_cards_button_func
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

one_dollar_chip = Button(
    screen,
    screen_width // 2 + 250,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='1',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_one
)

five_dollar_chip = Button(
    screen,
    screen_width // 2 + 300,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='5',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_five
)

twenty_five_dollar_chip = Button(
    screen,
    screen_width // 2 + 350,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='25',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_twenty_five
)

one_hundred_dollar_chip = Button(
    screen,
    screen_width // 2 + 400,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='100',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_one_hundred
)

five_hundred_dollar_chip = Button(
    screen,
    screen_width // 2 + 450,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='500',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_five_hundred
)

one_thousand_dollar_chip = Button(
    screen,
    screen_width // 2 + 500,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='1000',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_one_thousand
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

"""ace_choice_button_1 = Button(
    screen,
    screen_width // 2 - 600,  # X coordinate of the top-left corner
    600,  # Y coordinate of the top-left corner
    75,
    25,
    text='1',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=set_ace_to_1
)

ace_choice_button_11 = Button(
    screen,
    screen_width // 2 - 500,  # X coordinate of the top-left corner
    600,  # Y coordinate of the top-left corner
    75,
    25,
    text='11',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=set_ace_to_11
)"""

white = (255, 255, 255)
blue = (0, 0, 128)
black = (0, 0, 0)

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
    screen.fill("green")

    draw_text("Your cards are: ", text_font, black, screen_width // 2 - 25, 550)
    draw_text(str(user1.show_hand()), text_font, black, screen_width // 2 - 25, 600)

    draw_text("Your score: ", text_font, black, screen_width // 2 + 250, 550)
    draw_text(str(user1.get_hand_value()), text_font, black, screen_width // 2 + 350, 550)

    draw_text("Chips: ", text_font, black, screen_width // 2 + 450, 550)
    draw_text(str(user1.get_bankroll()), text_font, black, screen_width // 2 + 500, 550)

    draw_text("Dealer's cards are: ", text_font, black, screen_width // 2 - 25, 100)
    draw_text(str(dealer.show_hand()), text_font, black, screen_width // 2 - 25, 150)

    draw_text("Pot: ", text_font, black, screen_width // 2 - 25, 300)
    draw_text(str(pot.get_bankroll()), text_font, black, screen_width // 2 + 25, 300)

    draw_text("Dealer's score: ", text_font, black, screen_width // 2 + 250, 100)
    draw_text(str(dealer.get_hand_value()), text_font, black, screen_width // 2 + 350, 100)

    draw_text("Turn result: ", text_font, black, screen_width // 2 - 350, 100)
    draw_text(str(user1.get_turn_result()), text_font, black, screen_width // 2 - 250, 100)

    draw_text("Cards in deck: ", text_font, black, screen_width // 2 - 350, 300)
    draw_text(str(deck.get_deck_size()), text_font, black, screen_width // 2 - 250, 300)

    deal_cards_button.draw()
    hit_button.draw()
    stand_button.draw()
    clear_button.draw()
    # deal_specific_cards_button.draw()
    one_dollar_chip.draw()
    five_dollar_chip.draw()
    twenty_five_dollar_chip.draw()
    one_hundred_dollar_chip.draw()
    five_hundred_dollar_chip.draw()
    one_thousand_dollar_chip.draw()

    pygame.display.flip()
    pygame.display.update()

    # check_dealer_score()
    turn_over_check()

    pw.update(events)
    clock.tick(30)

pygame.quit()
