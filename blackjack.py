import pygame
import math
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

import random
import pygame.freetype


# To try and embedd my game in browser: https://pygame-web.github.io/#demos-on-itchio

# TO-DO: add a counter over a split hand that shows how much money is riding on that hand. same for the counter of that
# hand to show its value

# TO-DO: at the end of each hand, tell user how many chips they won or lost.

# TO-DO: add animations - maybe not needed

# TO-DO: Add title screen, music, make look better

# TO-DO: mobile formatting (separate repo probably)


# UG: Dealers cards go face up during two split hands (three total hands). need to check what's causing, and if chips
# are properly being distributed.
# BUG: If you double down and get blackjack, test that you get the right amount of chips back
# BUG: If dealer gets two aces, only once ace is changed to 1, even if the third card busts them. - should be fixed now

# TO-DO: add insurance.


class Card:
    """Creates a card object"""

    def __init__(self, value, name, suit, face_up=True, has_value_changed=False):
        """Initializes a card object with a value and a suit/"""
        self._value = value
        self._suit = suit
        self._face_up = face_up
        self._name = str(name)
        self._name_and_suit = str(name) + "_" + str(self._suit)
        self._has_value_changed = has_value_changed
        self._image = self._name_and_suit + '_white.png'

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

    def add_to_name(self, addition):
        """Adds something to the end of a card's name"""
        self._name_and_suit += "_" + str(addition)

    def get_name_and_suit(self):
        """Returns the card's name with the suit attached"""
        if self._face_up is True:
            return str(self._name_and_suit)
        else:
            return "Face down"

    def get_name_and_suit_always(self):
        """Returns the card's name with the suit attached, even if card is face down"""
        return str(self._name_and_suit)

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

    def add_number_to_card_name(self, number):
        """Adds a number to the end of each card name, to keep track of duplicate cards from multiple decks"""
        for card in self._cards:
            card.add_to_name(str(number))

    def add_card_to_deck(self, card_to_add):
        """Adds cards to the deck"""
        self._cards.append(card_to_add)

    def get_deck_size(self):
        """Returns the current size of the deck"""
        return len(self._cards)

    def set_deck(self, new_deck):
        """Sets the deck to whatever is specified"""
        self._cards = new_deck

    def duplicate_deck(self, times_to_duplicate):
        """Duplicates the current deck a set number of times"""
        self._cards = self._cards * times_to_duplicate

    def merge_decks(self, deck_to_merge):
        """Merges decks together"""
        for card in deck_to_merge:
            self._cards.append(card)


class User:
    """Creates a user"""

    def __init__(self, username=None, bankroll=0, amount_bet=0):
        """Initializes a user object with a given username and empty hand"""
        self._username = username
        self._hand = []
        self._split_hand = []
        self._split_hand2 = []
        self._split_hand3 = []
        self._can_bet = False
        self._bankroll = 1000
        self._score = 0
        self._turn_result = 'in-progress'
        self._bankroll = bankroll
        self._amount_bet = amount_bet
        self._amount_bet_on_split = 0
        self._amount_bet_on_split_2 = 0
        self._amount_bet_on_split_3 = 0
        self._is_split_hand_active = False
        self._is_split_hand_2_active = False
        self._is_split_hand_3_active = False
        self._split_hand_result = None
        self._split_hand_2_result = None
        self._split_hand_3_result = None
        self._cards_ready_to_be_drawn = False
        self._split_count_during_turn = 0
        self._chips_gained_on_turn = 0

    def draw_user_card(self, game_deck, number_of_cards, is_face_up=True):
        """Adds a specified number of cards to the user's hand from the deck."""
        game_deck.shuffle_deck()
        i = 0
        while i < number_of_cards:
            self._hand.append(game_deck.draw_card(is_face_up))
            i += 1

    def draw_user_card_to_split_hand(self, game_deck, number_of_cards, is_face_up=True):
        """Adds a specified number of cards to the user's split hand from a specified deck."""
        game_deck.shuffle_deck()
        i = 0
        while i < number_of_cards:
            self._split_hand.append(game_deck.draw_card(is_face_up))
            i += 1

    def draw_user_card_to_split_hand_2(self, game_deck, number_of_cards, is_face_up=True):
        """Adds a specified number of cards to the user's 2nd split hand from a specified deck."""
        game_deck.shuffle_deck()
        i = 0
        while i < number_of_cards:
            self._split_hand2.append(game_deck.draw_card(is_face_up))
            i += 1

    def draw_user_card_to_split_hand_3(self, game_deck, number_of_cards, is_face_up=True):
        """Adds a specified number of cards to the user's 3rd split hand from a specified deck."""
        game_deck.shuffle_deck()
        i = 0
        while i < number_of_cards:
            self._split_hand3.append(game_deck.draw_card(is_face_up))
            i += 1

    def get_hand(self):
        """Returns the user's hand"""
        return self._hand

    def get_chips_gained_on_turn(self):
        """Returns the amount of chips gained or lost on a turn"""
        return self._chips_gained_on_turn

    def get_can_user_bet(self):
        """Returns True if the user is able to bet, False if not"""
        return self._can_bet

    def get_split_hand_result(self):
        """Returns the result of the current split hand. Is None if a split hand is not active"""
        return self._split_hand_result

    def get_split_hand_2_result(self):
        """Returns the result of the 2nd split hand. Is None if a split hand is not active"""
        return self._split_hand_2_result

    def get_split_count_this_turn(self):
        """Returns the number of times a split has occurred this turn"""
        return self._split_count_during_turn

    def get_split_hand_3_result(self):
        """Returns the result of the 3rd split hand. Is None if a split hand is not active"""
        return self._split_hand_3_result

    def get_is_split_hand_active(self):
        """Returns False if a split hand is not active, and True if it is"""
        return self._is_split_hand_active

    def get_are_cards_ready_to_be_drawn(self):
        """Returns True if cards are ready to be dealt, False if not"""
        return self._cards_ready_to_be_drawn

    def get_is_split_hand_2_active(self):
        """Returns False if 2nd split hand is not active, and True if it is"""
        return self._is_split_hand_2_active

    def get_is_split_hand_3_active(self):
        """Returns False if a 3rd split hand is not active, True if it is"""
        return self._is_split_hand_3_active

    def get_turn_result(self):
        """Returns win if the user has won the hand, or loss if they have not"""
        return self._turn_result

    def get_amount_bet(self):
        """Returns the amount the player has bet during the current hand."""
        return self._amount_bet

    def get_score(self):
        """Returns the user's current score"""
        return self._score

    def get_split_hand(self):
        """Returns the current contents of the user's split hand"""
        return self._split_hand

    def get_split_hand_2(self):
        """Returns the current contents of the user's 2nd split hand"""
        return self._split_hand2

    def get_split_hand_3(self):
        """Returns the current contents of the user's 3rd split hand"""
        return self._split_hand3

    def get_hand_value(self):
        """Gets the value of the user's current hand"""
        current_value = 0
        for card in self._hand:
            current_value += card.get_value()
        return current_value

    def get_amount_bet_on_split(self):
        """Gets the value of what the user has bet on a split hand"""
        return self._amount_bet_on_split

    def get_amount_bet_on_split_2(self):
        """Gets the value of what the user has bet on 2nd split hand"""
        return self._amount_bet_on_split_2

    def get_amount_bet_on_split_3(self):
        """Gets the value of what the user has bet on 3rd split hand"""
        return self._amount_bet_on_split_3

    def get_bankroll(self):
        """Returns the user's bankroll"""
        return self._bankroll

    def get_username(self):
        """Returns the user's current username"""
        return self._username

    def get_split_hand_value(self):
        """Returns the value of the user's current split hand"""
        current_value = 0
        for card in self._split_hand:
            current_value += card.get_value()
        return current_value

    def get_split_hand_2_value(self):
        """Returns the value of the user's current 2nd split hand"""
        current_value = 0
        for card in self._split_hand2:
            current_value += card.get_value()
        return current_value


    def get_split_hand_3_value(self):
        """Returns the value of the user's current 3rd split hand"""
        current_value = 0
        for card in self._split_hand3:
            current_value += card.get_value()
        return current_value

    def set_username(self, new_username):
        """Changes the user's username"""
        self._username = new_username

    def set_chips_gained_on_turn(self, new_amount):
        """Sets the amount of chips gained on the current turn to a specific amount"""
        user1._chips_gained_on_turn = new_amount

    def set_are_cards_ready_to_be_drawn(self, new_condition):
        """True if cards are ready to be drawn, False if not. Changes this value."""
        self._cards_ready_to_be_drawn = new_condition

    def set_split_count_during_turn(self, new_amount):
        """Sets the amount of splits that have occurred during the current turn to a new amount"""
        self._split_count_during_turn = new_amount

    def set_is_split_hand_active(self, new_condition):
        """Changes whether a split hand is active"""
        self._is_split_hand_active = new_condition

    def set_is_split_hand_2_active(self, new_condition):
        """Changes whether split hand 2 is active"""
        self._is_split_hand_2_active = new_condition

    def set_is_split_hand_3_active(self, new_condition):
        """Changes whether split hand 3 is active"""
        self._is_split_hand_3_active = new_condition

    def update_amount_of_chips_gained_on_turn(self, new_amount):
        """Updates the amount of chips gained or lost by the specified amount"""
        self._chips_gained_on_turn += new_amount

    def set_hand(self, specified_hand):
        """Changes the user's hand. For testing purposes"""
        self._hand = specified_hand

    def set_can_user_bet(self, new_value):
        """Changes whether the user can bet. True if they can, false if they cannot"""
        self._can_bet = new_value

    def set_split_hand_result(self, new_result):
        """Updates the result/status of the current split hand"""
        self._split_hand_result = new_result

    def set_split_hand_2_result(self, new_result):
        """Updates the result/status of the split hand 2"""
        self._split_hand_2_result = new_result

    def set_split_hand_3_result(self, new_result):
        """Updates the result/status of split hand 3"""
        self._split_hand_3_result = new_result

    def update_split_hand(self, card_to_add):
        """Adds a card to the user's split hand"""
        self._split_hand.append(card_to_add)

    def update_split_hand_2(self, card_to_add):
        """Adds a card to the user's 2nd split hand"""
        self._split_hand2.append(card_to_add)

    def update_split_hand_3(self, card_to_add):
        """Adds a card to the user's 2nd split hand"""
        self._split_hand3.append(card_to_add)

    def set_split_hand(self, specified_hand):
        """Updates the user's split hand to the specified hand"""
        self._split_hand = specified_hand

    def set_split_hand_2(self, specified_hand):
        """Updates the user's 2nd split hand to the specified hand"""
        self._split_hand2 = specified_hand

    def set_split_hand_3(self, specified_hand):
        """Updates the user's 3rd split hand to the specified hand"""
        self._split_hand3 = specified_hand

    def update_amount_bet_on_split(self, amount_bet):
        """Updates the amount a user has bet on a split hand"""
        self._amount_bet_on_split += amount_bet

    def update_amount_bet_on_split_2(self, amount_bet):
        """Updates the amount a user has bet on 2nd split hand"""
        self._amount_bet_on_split_2 += amount_bet

    def update_amount_bet_on_split_3(self, amount_bet):
        """Updates the amount a user has bet on 3rd split hand"""
        self._amount_bet_on_split_3 += amount_bet

    def set_amount_bet_on_split(self, new_amount):
        """Sets the amount a user has bet on a split hand"""
        self._amount_bet_on_split = new_amount

    def set_amount_bet_on_split_2(self, new_amount):
        """Sets the amount a user has bet on 2nd split hand"""
        self._amount_bet_on_split_2 = new_amount

    def set_amount_bet_on_split_3(self, new_amount):
        """Sets the amount a user has bet on 3rd split hand"""
        self._amount_bet_on_split_3 = new_amount

    def update_amount_bet(self, amount_bet):
        """Updates the amount the user has bet during the current hand."""
        self._amount_bet += amount_bet

    def set_turn_result(self, new_turn_result):
        """Changes the user's current turn result"""
        self._turn_result = new_turn_result

    def update_bankroll(self, amount_to_add):
        """Changes the user's bankroll by the desired amount. A negative number lowers the bankroll"""
        self._bankroll += amount_to_add

    def update_split_count_during_turn(self, amount):
        """Updates the amount of splits that have occurred during the turn. A positive amount adds a positive number
        to the total"""
        self._split_count_during_turn += amount

    def set_bankroll(self, new_amount):
        """Changes the user's bankroll to a specific amount."""
        self._bankroll = new_amount

    def set_score(self, new_score):
        """Changes the user's score"""
        self._score = new_score

    def set_amount_bet(self, new_amount):
        """Changes the amount a user has bet during the current hand (not including splits) to a specified amount."""
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

    def show_split_hand(self):
        """Returns the user's split hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._split_hand:
            readable_card_list.append(card.get_name_and_suit())
        return readable_card_list

    def show_split_hand_2(self):
        """Returns the user's split hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._split_hand2:
            readable_card_list.append(card.get_name_and_suit())
        return readable_card_list

    def show_split_hand_3(self):
        """Returns the user's split hand with the value and suit in string form"""
        readable_card_list = []
        for card in self._split_hand3:
            readable_card_list.append(card.get_name_and_suit())
        return readable_card_list

    def clear_hand(self):
        """Clears the user's hand, returns the cards to the deck, and shuffles the deck"""
        for card in self._hand:
            deck.add_card_to_deck(card)
        for card in self._split_hand:
            deck.add_card_to_deck(card)
        for card in self._split_hand2:
            deck.add_card_to_deck(card)
        for card in self._split_hand3:
            deck.add_card_to_deck(card)
        deck.shuffle_deck()
        self._hand = []
        self._split_hand = []
        self._split_hand2 = []
        self._split_hand3 = []

    @property
    def amount_bet(self):
        return self._amount_bet


deck = Deck()  # The deck we will use for the game.
deck2 = Deck()
deck2.add_number_to_card_name(2)
deck3 = Deck()
deck3.add_number_to_card_name(3)
deck4 = Deck()
deck4.add_number_to_card_name(4)
deck5 = Deck()
deck5.add_number_to_card_name(5)
deck6 = Deck()
deck6.add_number_to_card_name(6)
deck.merge_decks(deck2.get_deck())
deck.merge_decks(deck3.get_deck())
deck.merge_decks(deck4.get_deck())
deck.merge_decks(deck5.get_deck())
deck.merge_decks(deck6.get_deck())


user1 = User(bankroll=1000)
pot = User("pot", 0)

def has_game_started():
    if user1.get_username() is None:
        user1.set_can_user_bet(False)


#  Need separate functions for each bet, since functions assigned to a button in pygame can't have parameters.
def user_bet_zero():
    """Takes 0 chips out of the user's bankroll and adds it to the pot"""
    user1.set_are_cards_ready_to_be_drawn(True)


def user_bet_one():
    """Takes 1 chip out of the user's bankroll and adds it to the pot"""
    if user1.get_can_user_bet() is True and user1.get_bankroll() >= 1:
        user1.update_bankroll(-1)
        user1.update_amount_bet(1)
        pot.update_bankroll(1)


def user_bet_five():
    """Takes 5 chips out of the user's bankroll and adds it to the pot"""
    if user1.get_bankroll() >= 5 and user1.get_can_user_bet() is True:
        user1.update_bankroll(-5)
        user1.update_amount_bet(5)
        pot.update_bankroll(5)


def user_bet_twenty_five():
    """Takes 25 chips out of the user's bankroll and adds it to the pot"""
    if user1.get_bankroll() >= 25 and user1.get_can_user_bet() is True:
        user1.update_bankroll(-25)
        user1.update_amount_bet(25)
        pot.update_bankroll(25)


def user_bet_one_hundred():
    """Takes 100 chips out of the user's bankroll and adds it to the pot"""
    if user1.get_bankroll() >= 100 and user1.get_can_user_bet() is True:
        user1.update_bankroll(-100)
        user1.update_amount_bet(100)
        pot.update_bankroll(100)


def user_bet_five_hundred():
    """Takes 500 chips out of the user's bankroll and adds it to the pot"""
    if user1.get_bankroll() >= 500 and user1.get_can_user_bet() is True:
        user1.update_bankroll(-500)
        user1.update_amount_bet(500)
        pot.update_bankroll(500)


def user_bet_one_thousand():
    """Takes 1000 chips out of the user's bankroll and adds it to the pot"""
    if user1.get_bankroll() >= 1000 and user1.get_can_user_bet() is True:
        user1.update_bankroll(-1000)
        user1.update_amount_bet(1000)
        pot.update_bankroll(1000)


def user_bet_all_in():
    """Takes all chips out of the user's bankroll and adds it to the pot"""
    if user1.get_can_user_bet() is True:
        user_bankroll = user1.get_bankroll()
        user1.update_amount_bet(user_bankroll)
        pot.update_bankroll(user_bankroll)
        user1.update_bankroll(-user_bankroll)


dealer = User("Dealer")

blackjack = 21


def draw_cards_button_func():
    deck.shuffle_deck()
    deck.shuffle_deck()
    user1.set_can_user_bet(False)
    user1.draw_user_card(deck, 2, True)
    # card1 = Card(11, 'ace', 'hearts')
    # card2 = Card(10, '10', 'spades')
    # hand2 = [card1, card2]
    # user1.set_hand(hand2)
    dealer.draw_user_card(deck, 1, True)
    dealer.draw_user_card(deck, 1, False)
    if user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:
        dealer.set_turn_result('Loss')
        user1.set_turn_result('Blackjack')
        distribute_chips_from_pot()
        turn_over_check()
        is_turn_over()
    initial_score_check()
    is_double_down_possible()
    split_check()
    user1.set_are_cards_ready_to_be_drawn(False)


def show_user_card_image():
    user_hand = user1.get_hand()
    i = 0
    for card in user_hand:
        image_file_name = card.get_image()
        img_size = (120, 168)  # Original size: 60x84
        load_string = "img/cards/all_cards/"
        final_image = load_string + image_file_name
        img = pygame.image.load(final_image)
        img = pygame.transform.scale(img, img_size)
        screen.blit(img, (screen_width // 2 - 100 + (40 * i), 500 + (3 * i)))
        i += 1


def show_dealer_card_image():
    dealer_hand = dealer.get_hand()
    i = 0
    for card in dealer_hand:
        img_size = (120, 168)  # Original size: 60x84
        if card.get_face_up() is True:
            image_file_name = card.get_image()
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (screen_width // 2 - 100 + (40 * i), 100 + (3 * i)))
            i += 1
        if card.get_face_up() is False:
            img = pygame.image.load('img/cards/all_cards/back_blue_basic_white.png')
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (screen_width // 2 - 100 + (40 * i), 100 + (3 * i)))
            i += 1


def hit_specific_cards():
    new_card = Card(7, '7', 'spades')
    user_hand = user1.get_hand()
    user_hand.append(new_card)
    ace_needs_to_change = False
    for card in user_hand:
        if card.get_name() == 'ace' and card.get_has_value_changed() is False:
            ace_needs_to_change = True
    if user1.get_hand_value() > 21 and ace_needs_to_change is True:
        for card in user1.get_hand():
            if card.get_name() == 'ace':
                if card.get_value() != 1:
                    card.set_value(1)
                    return
    if user1.get_hand_value() > 21:
        user1.set_turn_result('Loss')
        dealer.set_turn_result('Win')
    is_double_down_possible()


def split_check():
    """Checks if the user has two cards of the same value after the first two cards are dealt.
    If so, the function returns True."""
    user_hand = user1.get_hand()
    if len(user_hand) == 2:
        card1 = user_hand[0].get_name()
        card2 = user_hand[1].get_name()
        if card1 == card2 and user1.get_bankroll() >= user1.get_amount_bet():
            return True
        else:
            return False


def split_check_2():
    if user1.get_is_split_hand_active() is True:
        user_split_hand = user1.get_split_hand()
        if len(user_split_hand) == 2:
            card1_split = user_split_hand[0].get_name()
            card2_split = user_split_hand[1].get_name()
            if card1_split == card2_split and user1.get_bankroll() >= user1.get_amount_bet_on_split():
                return True
        return False


def split_check_3():
    if user1.get_is_split_hand_2_active() is True:
        user_split_hand2 = user1.get_split_hand_2()
        if len(user_split_hand2) == 2:
            card1_split = user_split_hand2[0].get_name()
            card2_split = user_split_hand2[1].get_name()
            if card1_split == card2_split and user1.get_bankroll() >= user1.get_amount_bet_on_split_2():
                return True
        return False


def is_double_down_possible():
    if user1.get_is_split_hand_active() is True:
        user_split_hand = user1.get_split_hand()
        if (len(user_split_hand) == 2 and 8 < user1.get_split_hand_value() < 12
                and user1.get_bankroll() >= user1.get_amount_bet_on_split()):
            return True
        else:
            return False

    if user1.get_is_split_hand_2_active() is True:
        user_split_hand = user1.get_split_hand_2()
        if (len(user_split_hand) == 2 and 8 < user1.get_split_hand_2_value() < 12
                and user1.get_bankroll() >= user1.get_amount_bet_on_split_2()):
            return True
        else:
            return False

    if user1.get_is_split_hand_3_active() is True:
        user_split_hand = user1.get_split_hand_3()
        if (len(user_split_hand) == 2 and 8 < user1.get_split_hand_3_value() < 12
                and user1.get_bankroll() >= user1.get_amount_bet_on_split_3()):
            return True
        else:
            return False
    user_hand = user1.get_hand()
    if len(user_hand) == 2 and 8 < user1.get_hand_value() < 12 and user1.get_bankroll() >= user1.get_amount_bet():
        if user1.get_turn_result() == 'in-progress':
            return True
    else:
        return False


def double_down():
    if is_double_down_possible() is True:
        if user1.get_is_split_hand_active() is True:
            pot.update_bankroll(user1.get_amount_bet_on_split())
            user1.update_bankroll(-user1.get_amount_bet_on_split())
            user1.update_amount_bet_on_split(user1.get_amount_bet_on_split())
            user1.draw_user_card_to_split_hand(deck, 1, True)
            # Should be face down, update later
            stand()
            return
        if user1.get_is_split_hand_2_active() is True:
            pot.update_bankroll(user1.get_amount_bet_on_split_2())
            user1.update_bankroll(-user1.get_amount_bet_on_split_2())
            user1.update_amount_bet_on_split(user1.get_amount_bet_on_split_2())
            user1.draw_user_card_to_split_hand_2(deck, 1, True)
            # Should be face down, update later
            stand()
            return
        if user1.get_is_split_hand_3_active() is True:
            pot.update_bankroll(user1.get_amount_bet_on_split_3())
            user1.update_bankroll(-user1.get_amount_bet_on_split_3())
            user1.update_amount_bet_on_split(user1.get_amount_bet_on_split_3())
            user1.draw_user_card_to_split_hand_3(deck, 1, True)
            # Should be face down, update later
            stand()
            return
        pot.update_bankroll(user1.get_amount_bet())
        user1.update_bankroll(-user1.get_amount_bet())
        user1.update_amount_bet(user1.get_amount_bet())
        user1.draw_user_card(deck, 1, True)
        stand()
        return
    return


def split_cards():
    """Splits the user's cards if split_check returns true."""
    if split_check_3() is True:
        user1.set_split_hand_3_result('in-progress')
        user_hand_to_split = user1.get_split_hand_2()
        for card in user_hand_to_split:
            if card.get_name() == 'ace':
                card.set_value(11)
                card.set_has_value_changed(False)
        user1.update_split_hand_3(user_hand_to_split[0])
        user1.update_amount_bet_on_split_2(user1.get_amount_bet_on_split())
        user1.update_bankroll(-user1.get_amount_bet_on_split())
        pot.update_bankroll(user1.get_amount_bet_on_split_2())
        i = 0
        for card in user1.get_split_hand_3():
            image_file_name = card.get_image()
            img_size = (120, 168)  # Original size: 60x84
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (screen_width // 2 - 400 + (40 * i), 500 + (3 * i)))
        user1.set_is_split_hand_3_active(True)
        del user_hand_to_split[0]
        user1.update_split_count_during_turn(1)
        for card in user1.get_split_hand_3():
            if card.get_name() == 'ace':
                hit()
                stand()
        return
    if split_check_2() is True:
        user1.set_split_hand_2_result('in-progress')
        user_hand_to_split = user1.get_split_hand()
        for card in user_hand_to_split:
            if card.get_name() == 'ace':
                card.set_value(11)
                card.set_has_value_changed(False)
        user1.update_split_hand_2(user_hand_to_split[0])
        user1.update_amount_bet_on_split_2(user1.get_amount_bet_on_split())
        user1.update_bankroll(-user1.get_amount_bet_on_split())
        pot.update_bankroll(user1.get_amount_bet_on_split_2())
        i = 0
        for card in user1.get_split_hand_2():
            image_file_name = card.get_image()
            img_size = (120, 168)  # Original size: 60x84
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (screen_width // 2 - 400 + (40 * i), 500 + (3 * i)))
        user1.set_is_split_hand_2_active(True)
        del user_hand_to_split[0]
        user1.update_split_count_during_turn(1)
        for card in user1.get_split_hand_2():
            if card.get_name() == 'ace':
                hit()
                stand()
        return
    if split_check() is True:
        if user1.get_split_hand():
            user1.set_split_hand_2_result('in-progress')
            user_hand_to_split = user1.get_split_hand()
            for card in user_hand_to_split:
                if card.get_name() == 'ace':
                    card.set_value(11)
                    card.set_has_value_changed(False)
            user1.update_split_hand_2(user_hand_to_split[0])
            user1.update_amount_bet_on_split_2(user1.get_amount_bet_on_split())
            user1.update_bankroll(-user1.get_amount_bet_on_split())
            pot.update_bankroll(user1.get_amount_bet_on_split_2())
            i = 0
            for card in user1.get_split_hand_2():
                image_file_name = card.get_image()
                img_size = (120, 168)  # Original size: 60x84
                load_string = "img/cards/all_cards/"
                final_image = load_string + image_file_name
                img = pygame.image.load(final_image)
                img = pygame.transform.scale(img, img_size)
                screen.blit(img, (screen_width // 2 - 400 + (40 * i), 500 + (3 * i)))
            user1.set_is_split_hand_2_active(True)
            del user_hand_to_split[0]
            user1.update_split_count_during_turn(1)
            for card in user1.get_split_hand_2():
                if card.get_name() == 'ace':
                    hit()
                    stand()
            return
        user1.set_split_hand_result('in-progress')
        user_hand = user1.get_hand()
        for card in user_hand:
            if card.get_name() == 'ace':
                card.set_value(11)
                card.set_has_value_changed(False)
        user1.update_split_hand(user_hand[0])
        user1.update_amount_bet_on_split(user1.get_amount_bet())
        user1.update_bankroll(-user1.get_amount_bet_on_split())
        pot.update_bankroll(user1.get_amount_bet_on_split())
        user1.set_is_split_hand_active(True)
        del user_hand[0]
        user1.update_split_count_during_turn(1)
        for card2 in user1.get_split_hand():
            if card2.get_name() == 'ace':
                hit()
                stand()
        return


def clear_bets():
    user1.update_bankroll(pot.get_bankroll())
    pot.set_bankroll(0)
    user1.set_amount_bet(0)
    user1.set_are_cards_ready_to_be_drawn(False)


"""def draw_specific_cards_button_func():  # This is for testing certain hand combinations and results
    card1 = Card(11, 'ace', 'hearts', True)
    card2 = Card(11, 'ace', 'diamonds', False)
    new_hand1 = [card1, card2]
    user1.set_can_user_bet(False)
    user1.draw_user_card(deck, 2, True)
    card3 = Card(11, 'ace', 'hearts', True)
    card4 = Card(1, 'ace', 'clubs', True)
    dealer.set_hand(new_hand1)
    new_hand2 = [card3, card4]
    # user1.set_hand(new_hand2)
    # dealer.draw_user_card(deck, 1, True)
    # dealer.draw_user_card(deck, 1, False)
    initial_score_check()
    is_double_down_possible()
    split_check()"""



def hit():
    if pot.get_bankroll() == 0:
        return "No bets placed"
    split_check_3()
    split_check_2()
    split_check()
    if user1.get_is_split_hand_3_active() is True:
        user1.draw_user_card_to_split_hand_3(deck, 1, True)
        # specific_card = Card(7, '7', 'clubs', True) # For testing only
        user_split_hand3 = user1.get_split_hand_3()
        # user_split_hand3.append(specific_card) # For testing only
        ace_needs_to_change = False
        for card in user_split_hand3:
            if card.get_name() == 'ace' and card.get_has_value_changed() is False:
                ace_needs_to_change = True
        if user1.get_split_hand_3_value() > 21 and ace_needs_to_change is True:
            for card in user1.get_split_hand_3():
                if card.get_name() == 'ace':
                    if card.get_value() != 1:
                        card.set_value(1)
                        return
        if user1.get_split_hand_3_value() > 21:
            user1.set_split_hand_3_result('Loss')
            dealer.set_split_hand_3_result('Win')
            user1.set_is_split_hand_3_active(False)
        return

    if user1.get_is_split_hand_2_active() is True:
        user1.draw_user_card_to_split_hand_2(deck, 1, True)
        # specific_card = Card(11, 'ace', 'clubs', True) # For testing only
        user_split_hand2 = user1.get_split_hand_2()
        # user_split_hand2.append(specific_card)  # For testing only
        ace_needs_to_change = False
        for card in user_split_hand2:
            if card.get_name() == 'ace' and card.get_has_value_changed() is False:
                ace_needs_to_change = True
        if user1.get_split_hand_2_value() > 21 and ace_needs_to_change is True:
            for card in user1.get_split_hand_2():
                if card.get_name() == 'ace':
                    if card.get_value() != 1:
                        card.set_value(1)
                        return
        if user1.get_split_hand_2_value() > 21:
            user1.set_split_hand_2_result('Loss')
            dealer.set_split_hand_2_result('Win')
            user1.set_is_split_hand_2_active(False)
        return

    if user1.get_is_split_hand_active() is True:
        user1.draw_user_card_to_split_hand(deck, 1, True)
        # specific_card = Card(11, 'ace', 'clubs', True) # For testing only
        user_split_hand = user1.get_split_hand()
        # user_split_hand.append(specific_card)  # For testing only
        ace_needs_to_change = False
        for card in user_split_hand:
            if card.get_name() == 'ace' and card.get_has_value_changed() is False:
                ace_needs_to_change = True
        if user1.get_split_hand_value() > 21 and ace_needs_to_change is True:
            for card in user1.get_split_hand():
                if card.get_name() == 'ace':
                    if card.get_value() != 1:
                        card.set_value(1)
                        return
        if user1.get_split_hand_value() > 21:
            user1.set_split_hand_result('Loss')
            dealer.set_split_hand_result('Win')
            user1.set_is_split_hand_active(False)
        return

    user1.draw_user_card(deck, 1, True)
    # specific_card = Card(7, '7', 'clubs', True) # For testing only
    user_hand = user1.get_hand()
    # user_hand.append(specific_card) # For testing only
    ace_needs_to_change = False
    for card in user_hand:
        if card.get_name() == 'ace' and card.get_has_value_changed() is False:
            ace_needs_to_change = True
    if user1.get_hand_value() > 21 and ace_needs_to_change is True:
        for card in user1.get_hand():
            if card.get_name() == 'ace':
                if card.get_value() != 1:
                    card.set_value(1)
                    return
    if user1.get_hand_value() > 21:
        if user1.get_split_hand():
            while dealer.get_hand_value() <= 16:
                dealer.draw_user_card(deck, 1, True)
                check_to_change_ace(dealer)
                check_to_change_ace(dealer)
            split_hand_score_check()
            stand()
        user1.set_turn_result('Loss')
        dealer.set_turn_result('Win')


def stand():
    if len(user1.get_hand()) == 2 and user1.get_hand_value() == 21:
        dealer_hand = dealer.get_hand()
        dealer_hand[1].set_face_up(True)
        check_to_change_ace(dealer)
        final_score_check()
        return
    if user1.get_is_split_hand_3_active() is True:
        user1.set_is_split_hand_3_active(False)
        return
    if user1.get_is_split_hand_2_active() is True:
        user1.set_is_split_hand_2_active(False)
        return
    if user1.get_is_split_hand_active() is True:
        user1.set_is_split_hand_active(False)
        return
    dealer_hand = dealer.get_hand()
    dealer_hand[1].set_face_up(True)
    check_to_change_ace(dealer)
    check_to_change_ace(dealer)
    while dealer.get_hand_value() <= 16:
        dealer.draw_user_card(deck, 1, True)
        check_to_change_ace(dealer)
        check_to_change_ace(dealer)
    final_score_check()


def initial_score_check():
    check_to_change_ace(user1)
    check_to_change_ace(dealer)
    if user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:  # Player gets natural 21 and dealer does not
        dealer.set_turn_result('Loss')
        user1.set_turn_result('Blackjack')
        is_turn_over()
        return
    elif (user1.get_hand_value() > 21 and user1.get_split_hand == []  # User busts
            or dealer.get_hand_value() == 21 and user1.get_hand_value != 21):  # Dealer gets natural blackjack
        dealer.set_turn_result('Win')
        user1.set_turn_result('Loss')
        return
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() == 21:  # Both player and dealer get natural 21
        dealer.set_turn_result('Push')
        user1.set_turn_result('Push')
        turn_over_check()
        return


def refill_bankroll():
    user1.set_bankroll(1000)


def game_over_check():
    if user1.get_turn_result() == 'Loss':
        if user1.get_bankroll() == 0:
            return True
        else:
            return False


def clear_table():
    user1.set_chips_gained_on_turn(0)
    change_ace_value_to_11_for_all_user_hands(user1.get_hand())
    change_ace_value_to_11_for_all_user_hands(user1.get_split_hand())
    change_ace_value_to_11_for_all_user_hands(user1.get_split_hand_2())
    change_ace_value_to_11_for_all_user_hands(user1.get_split_hand_3())
    change_ace_value_to_11_for_all_user_hands(dealer.get_hand())
    user1.set_turn_result('in-progress')
    user1.clear_hand()
    pot.set_bankroll(0)
    user1.set_is_split_hand_active(False)
    user1.set_split_hand_result(None)
    user1.set_is_split_hand_2_active(False)
    user1.set_split_hand_2_result(None)
    user1.set_is_split_hand_3_active(False)
    user1.set_split_hand_3_result(None)
    dealer.set_turn_result('in-progress')
    dealer.clear_hand()
    user1.set_can_user_bet(True)


def set_ace_to_1():
    for card in user1.get_hand():
        if card.get_name() == 'ace':
            card.set_value(1)
            return
    return


def set_ace_to_11():
    for card in user1.get_hand():
        if card.get_name() == 'ace':
            card.set_value(11)
            return
    return


def turn_over_check():
    if user1.get_split_hand_3():
        if (user1.get_turn_result() != 'in-progress' and user1.get_split_hand_result() != 'in-progress'
                and user1.get_split_hand_2_result() != 'in-progress'
                and user1.get_split_hand_3_result() != 'in-progress' and dealer.get_turn_result() != 'in-progress'):
            dealer_hand = dealer.get_hand()
            for card in dealer_hand:
                card.set_face_up(True)
            distribute_chips_from_pot()
            return
    if user1.get_split_hand_2():
        if (user1.get_turn_result() != 'in-progress' and user1.get_split_hand_result() != 'in-progress'
                and user1.get_split_hand_2_result() != 'in-progress' and dealer.get_turn_result() != 'in-progress'):
            dealer_hand = dealer.get_hand()
            for card in dealer_hand:
                card.set_face_up(True)
            distribute_chips_from_pot()
            return
    if user1.get_split_hand():
        if (user1.get_turn_result() != 'in-progress' and user1.get_split_hand_result() != 'in-progress'
                and dealer.get_turn_result() != 'in-progress'):
            dealer_hand = dealer.get_hand()
            for card in dealer_hand:
                card.set_face_up(True)
            distribute_chips_from_pot()
            return
    if user1.get_turn_result() != 'in-progress' and dealer.get_turn_result() != 'in-progress':
        dealer_hand = dealer.get_hand()
        for card in dealer_hand:
            card.set_face_up(True)
        distribute_chips_from_pot()
        return
        # clear_table() - need to add a pop up window that displays the result, and only moves to the next hand after
        # the user acknowledges it. currently, it moves too quick for the user to know what happened.


def change_ace_value_to_11(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace':
            card.set_has_value_changed(False)
            card.set_value(11)


def change_ace_value_to_11_for_all_user_hands(hand):
    for item in hand:
        if item.get_name() == 'ace':
            item.set_has_value_changed(False)
            item. set_value(11)


def change_ace_value_to_1(user):
    user_hand = user.get_hand()
    for card in user_hand:
        if card.get_name() == 'ace' and card.get_has_value_changed() is False and user.get_hand_value() > 21:

            card.set_value(1)
            card.set_has_value_changed(True)


def new_game():
    clear_table()
    user1.set_bankroll(1000)


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


def split_hand_score_check():
    if user1.get_split_hand_result() is not None:
        if 21 >= user1.get_split_hand_value() == dealer.get_hand_value():
            #  If the user and dealer tie
            user1.set_split_hand_result('Push')
            dealer.set_split_hand_result('Push')
            return True
        elif user1.get_split_hand_value() == 21 and dealer.get_hand_value() != 21:  # User blackjack
            user1.set_split_hand_result('Blackjack')
            dealer.set_split_hand_result('Loss')
            return True
        elif (dealer.get_hand_value() < user1.get_split_hand_value() <= 21  # Neither bust, user has higher hand
              or dealer.get_hand_value() > 21 >= user1.get_split_hand_value()):  # Dealer bust, user does not
            user1.set_split_hand_result('Win')
            dealer.set_split_hand_result('Loss')
            return True
        elif (user1.get_split_hand_value() > 21  # User bust
              or user1.get_split_hand_value() < dealer.get_hand_value() <= 21  # Neither bust, dealer has higher hand
              or dealer.get_hand_value() == 21):  # Dealer blackjack
            user1.set_split_hand_result('Loss')
            dealer.set_split_hand_result('Win')
            return True
    return False


def split_hand_2_score_check():
    if user1.get_split_hand_2_result() is not None:
        if 21 >= user1.get_split_hand_2_value() == dealer.get_hand_value():
            #  If the user and dealer tie
            user1.set_split_hand_2_result('Push')
            dealer.set_split_hand_2_result('Push')
            return True
        elif user1.get_split_hand_2_value() == 21 and dealer.get_hand_value() != 21:  # User blackjack
            user1.set_split_hand_2_result('Blackjack')
            dealer.set_split_hand_2_result('Loss')
            return True
        elif (dealer.get_hand_value() < user1.get_split_hand_2_value() <= 21  # Neither bust, user has higher hand
              or dealer.get_hand_value() > 21 >= user1.get_split_hand_2_value()):  # Dealer bust, user does not
            user1.set_split_hand_2_result('Win')
            dealer.set_split_hand_2_result('Loss')
            return True
        elif (user1.get_split_hand_2_value() > 21  # User bust
              or user1.get_split_hand_2_value() < dealer.get_hand_value() <= 21  # Neither bust, dealer has higher hand
              or dealer.get_hand_value() == 21):  # Dealer blackjack
            user1.set_split_hand_2_result('Loss')
            dealer.set_split_hand_2_result('Win')
            return True
    return False


def split_hand_3_score_check():
    if user1.get_split_hand_3_result() is not None:
        if 21 >= user1.get_split_hand_3_value() == dealer.get_hand_value():
            #  If the user and dealer tie
            user1.set_split_hand_3_result('Push')
            dealer.set_split_hand_3_result('Push')
            return True
        elif user1.get_split_hand_3_value() == 21 and dealer.get_hand_value() != 21:  # User blackjack
            user1.set_split_hand_3_result('Blackjack')
            dealer.set_split_hand_3_result('Loss')
            return True
        elif (dealer.get_hand_value() < user1.get_split_hand_2_value() <= 21  # Neither bust, user has higher hand
              or dealer.get_hand_value() > 21 >= user1.get_split_hand_2_value()):  # Dealer bust, user does not
            user1.set_split_hand_3_result('Win')
            dealer.set_split_hand_3_result('Loss')
            return True
        elif (user1.get_split_hand_3_value() > 21  # User bust
              or user1.get_split_hand_3_value() < dealer.get_hand_value() <= 21  # Neither bust, dealer has higher hand
              or dealer.get_hand_value() == 21):  # Dealer blackjack
            user1.set_split_hand_3_result('Loss')
            dealer.set_split_hand_3_result('Win')
            return True
    return False


def check_to_change_ace(user):
    if user.get_hand_value() > 21 and check_for_ace(user) is True:
        change_ace_value_to_1(user)
        return


def final_score_check():
    split_hand_3_score_check()
    split_hand_2_score_check()
    split_hand_score_check()
    if 21 >= user1.get_hand_value() == dealer.get_hand_value():
        #  If the user and dealer tie
        user1.set_turn_result('Push')
        dealer.set_turn_result('Push')
        return
    elif user1.get_hand_value() == 21 and dealer.get_hand_value() != 21:  # User blackjack
        user1.set_turn_result('Blackjack')
        dealer.set_turn_result('Loss')
        return
    elif (dealer.get_hand_value() < user1.get_hand_value() <= 21  # Neither bust, user has higher hand
          or dealer.get_hand_value() > 21 >= user1.get_hand_value()):  # Dealer bust, user does not
        user1.set_turn_result('Win')
        dealer.set_turn_result('Loss')
        return
    elif (user1.get_hand_value() > 21  # User bust
          or user1.get_hand_value() < dealer.get_hand_value() <= 21  # Neither bust, dealer has higher hand
          or dealer.get_hand_value() == 21):  # Dealer blackjack
        user1.set_turn_result('Loss')
        dealer.set_turn_result('Win')
        return
    return


def blackjack_check():
    if user1.get_split_hand_3():
        if user1.get_split_hand_3_value() == 21 and user1.get_split_hand_3_result() == 'in-progress':
            stand()
    if user1.get_split_hand_2():
        if user1.get_split_hand_2_value() == 21 and user1.get_split_hand_2_result() == 'in-progress':
            stand()
    if user1.get_split_hand():
        if user1.get_split_hand_value() == 21 and user1.get_split_hand_result == 'in-progress':
            stand()
    if user1.get_hand_value() == 21 and user1.get_turn_result() == 'in-progress':
        stand()

def is_turn_over():
    if user1.get_turn_result() != 'in-progress' and dealer.get_turn_result() != 'in-progress':
        return True


# and user1.get_split_hand_result() != 'in-progress' and user1.get_split_hand_2_result() != 'in-progress'
# and user1.get_split_hand_3_result() != 'in-progress':


def ready_to_draw_cards_check():
    if pot.get_bankroll() > 0 and user1.get_hand() == []:
        user1.set_are_cards_ready_to_be_drawn(True)


def distribute_chips_from_pot():
    if user1.get_split_hand_result() is not None:
        if user1.get_split_hand_result() == 'Win' or user1.get_split_hand_result() == 'Blackjack':
            user1.update_bankroll(2 * user1.get_amount_bet_on_split())
            user1.update_amount_of_chips_gained_on_turn(2 * user1.get_amount_bet_on_split())
            pot.update_bankroll(user1.get_amount_bet_on_split())
            user1.set_amount_bet_on_split(0)
        elif user1.get_split_hand_result() == 'Push':
            user1.update_bankroll(user1.get_amount_bet_on_split())
            user1.update_amount_of_chips_gained_on_turn(user1.get_amount_bet_on_split())
            pot.update_bankroll(-user1.get_amount_bet_on_split())
            user1.set_amount_bet_on_split(0)
        elif user1.get_split_hand_result() == 'Loss':
            user1.update_amount_of_chips_gained_on_turn(-user1.get_amount_bet_on_split())
            pot.update_bankroll(user1.get_amount_bet_on_split())
            user1.set_amount_bet_on_split(0)
    if user1.get_split_hand_2_result() is not None:
        if user1.get_split_hand_2_result() == 'Win' or user1.get_split_hand_2_result() == 'Blackjack':
            user1.update_bankroll(2 * user1.get_amount_bet_on_split_2())
            user1.update_amount_of_chips_gained_on_turn(2 * user1.get_amount_bet_on_split_2())
            pot.set_bankroll(0)
            user1.set_amount_bet_on_split_2(0)
        elif user1.get_split_hand_2_result() == 'Push':
            user1.update_bankroll(user1.get_amount_bet_on_split_2())
            user1.update_amount_of_chips_gained_on_turn(user1.get_amount_bet_on_split_2())
            pot.set_bankroll(0)
            user1.set_amount_bet_on_split_2(0)
        elif user1.get_split_hand_2_result() == 'Loss':
            user1.update_amount_of_chips_gained_on_turn(-user1.get_amount_bet_on_split_2())
            user1.set_amount_bet_on_split_2(0)
            pot.set_bankroll(0)
    if user1.get_split_hand_3_result() is not None:
        if user1.get_split_hand_3_result() == 'Win' or user1.get_split_hand_3_result() == 'Blackjack':
            user1.update_bankroll(2 * user1.get_amount_bet_on_split_3())
            user1.update_amount_of_chips_gained_on_turn(2 * user1.get_amount_bet_on_split_3())
            pot.set_bankroll(0)
            user1.set_amount_bet_on_split_3(0)
        elif user1.get_split_hand_3_result() == 'Push':
            user1.update_bankroll(user1.get_amount_bet_on_split_3())
            user1.update_amount_of_chips_gained_on_turn(user1.get_amount_bet_on_split_3())
            pot.set_bankroll(0)
            user1.set_amount_bet_on_split_3(0)
        elif user1.get_split_hand_3_result() == 'Loss':
            user1.update_amount_of_chips_gained_on_turn(-user1.get_amount_bet_on_split_3())
            user1.set_amount_bet_on_split_3(0)
            pot.set_bankroll(0)
    if user1.get_turn_result() == 'Win':
        user1.update_bankroll(2 * user1.get_amount_bet())
        user1.update_amount_of_chips_gained_on_turn(2 * user1.get_amount_bet())
        pot.set_bankroll(0)
        user1.set_amount_bet(0)
    elif user1.get_turn_result() == 'Blackjack':
        user1.update_bankroll(math.floor(2.5 * user1.get_amount_bet()))
        user1.update_amount_of_chips_gained_on_turn(math.floor(2.5 * user1.get_amount_bet()))
        pot.set_bankroll(0)
        user1.set_amount_bet(0)
    elif user1.get_turn_result() == 'Push':
        user1.update_bankroll(user1.get_amount_bet())
        user1.update_amount_of_chips_gained_on_turn(user1.get_amount_bet())
        pot.set_bankroll(0)
        user1.set_amount_bet(0)
    elif user1.get_turn_result() == 'Loss':
        user1.update_amount_of_chips_gained_on_turn(-user1.get_amount_bet())
        pot.set_bankroll(0)
        user1.set_amount_bet(0)


def update_username():
    text_entered = str(username_textbox.getText())
    user1.set_username(text_entered)
    user1.set_can_user_bet(True)


pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

username_textbox = TextBox(screen, screen_width // 2 - 175, 500, 300, 50, fontSize=20,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=update_username, radius=10, borderThickness=5)

double_down_button = Button(
    screen,
    screen_width // 2 + 100,  # X coordinate of the top-left corner
    450,  # Y coordinate of the top-left corner
    125,
    25,
    text='Double Down',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=double_down
)

deal_cards_button = Button(
            screen,
            screen_width // 2 - 55550,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            125,
            25,
            text='Draw cards',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

"""deal_specific_cards_button = Button(  # For testing
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
)"""

refill_bankroll_button = Button(
    screen,
    screen_width // 2 + 450,  # X coordinate of the top-left corner
    575,  # Y coordinate of the top-left corner
    125,
    25,
    text='Refill Bank2',
    fontSize=20, margin=20,
    inactiveColour=(0, 0, 255),
    pressedColour=(255, 0, 0), radius=20,
    onClick=refill_bankroll
)

no_bet_button = Button(
    screen,
    screen_width // 2 + 420,  # X coordinate of the top-left corner
    575,  # Y coordinate of the top-left corner
    125,
    25,
    text='Pass',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_zero
)

hit_specific_card_button = Button(
    screen,
    screen_width // 2 + 250,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    75,
    25,
    text='Hit2',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=hit_specific_cards
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

one_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 250,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='1',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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

five_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 300,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='5',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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

twenty_five_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 350,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='25',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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

one_hundred_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 400,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='100',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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

five_hundred_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 450,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='500',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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

one_thousand_dollar_chip_no_func = Button(
    screen,
    screen_width // 2 + 500,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    25,
    25,
    text='1000',
    fontSize=10, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
)

all_in_button = Button(
    screen,
    screen_width // 2 + 550,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    75,
    25,
    text='All In',
    fontSize=16, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=user_bet_all_in
)

all_in_button_no_func = Button(
    screen,
    screen_width // 2 + 550,  # X coordinate of the top-left corner
    650,  # Y coordinate of the top-left corner
    75,
    25,
    text='All In',
    fontSize=16, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
)

split_button = Button(
    screen,
    screen_width // 2 - 50,  # X coordinate of the top-left corner
    425,  # Y coordinate of the top-left corner
    75,
    25,
    text='Split',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
    onClick=split_cards
)

new_game_button = Button(
    screen,
    screen_width // 2 - 4587,  # X coordinate of the top-left corner
    400,  # Y coordinate of the top-left corner
    174,
    25,
    text='New Game',
    fontSize=24, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
)

new_turn_button = Button(
    screen,
    screen_width // 2 + 4275,  # X coordinate of the top-left corner
    450,  # Y coordinate of the top-left corner
    125,
    25,
    text='New Turn',
    fontSize=20, margin=20,
    inactiveColour=(255, 0, 0),
    pressedColour=(0, 255, 0), radius=20,
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
big_text_font = pygame.font.SysFont("Arial", 35)


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
    new_turn_button.draw()

    if user1.get_hand():
        draw_text("Your cards", text_font, black, screen_width // 2 - 80, 470)
    # draw_text(str(user1.show_hand()), text_font, black, screen_width // 2 - 25, 600)
    if user1.get_turn_result() == 'in-progress':
        new_turn_button = Button(
            screen,
            screen_width // 2 + 44350,  # X coordinate of the top-left corner
            4550,  # Y coordinate of the top-left corner
            125,
            25,
            text='New Turn',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=clear_table
        )

    if user1.get_username() is not None:
        draw_text(str(user1.get_username()), big_text_font, black, screen_width // 2 + 450, 450)

    draw_text("Hand value: ", text_font, black, screen_width // 2 + 450, 510)
    draw_text(str(user1.get_hand_value()), text_font, black, screen_width // 2 + 535, 510)

    draw_text("Chips: ", text_font, black, screen_width // 2 + 450, 550)
    draw_text(str(user1.get_bankroll()), text_font, black, screen_width // 2 + 500, 550)

    one_dollar_chip.draw()
    five_dollar_chip.draw()
    twenty_five_dollar_chip.draw()
    one_hundred_dollar_chip.draw()
    five_hundred_dollar_chip.draw()
    one_thousand_dollar_chip.draw()
    all_in_button.draw()

    one_dollar_chip_no_func.draw()
    five_dollar_chip_no_func.draw()
    twenty_five_dollar_chip_no_func.draw()
    one_hundred_dollar_chip_no_func.draw()
    five_hundred_dollar_chip_no_func.draw()
    one_thousand_dollar_chip_no_func.draw()
    all_in_button_no_func.draw()

    if dealer.get_hand():
        draw_text("Dealer's cards", text_font, black, screen_width // 2 - 80, 70)
    # draw_text(str(dealer.show_hand()), text_font, black, screen_width // 2 - 25, 150)

    draw_text("Pot: ", text_font, black, screen_width // 2 - 50, 300)
    draw_text(str(pot.get_bankroll()), text_font, black, screen_width // 2 - 15, 300)

    # draw_text("Dealer's score: ", text_font, black, screen_width // 2 + 250, 100)
    # draw_text(str(dealer.get_hand_value()), text_font, black, screen_width // 2 + 350, 100)


    # draw_text("Cards in deck: ", text_font, black, screen_width // 2 - 350, 300)
    # draw_text(str(deck.get_deck_size()), text_font, black, screen_width // 2 - 250, 300)

    if user1.get_split_hand_result() is not None:
        draw_text("Your split cards are: ", text_font, black, 30, 475)
        i = 0
        for card in user1.get_split_hand():
            image_file_name = card.get_image()
            img_size = (120, 168)  # Original size: 60x84
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (25 + (40 * i), 525 + (3 * i)))
            i += 1

        draw_text("Split hand value: ", text_font, black, screen_width // 2 + 250, 510)
        draw_text(str(user1.get_split_hand_value()), text_font, black, screen_width // 2 + 375, 510)

        draw_text("Split hand result: ", text_font, black, screen_width // 2 + 250, 190)
        draw_text(str(user1.get_split_hand_result()), text_font, black, screen_width // 2 + 375, 190)

    if user1.get_split_hand_2_result() is not None:
        draw_text("Your 2nd split cards are: ", text_font, black, 30, 250)
        i = 0
        for card in user1.get_split_hand_2():
            image_file_name = card.get_image()
            img_size = (120, 168)  # Original size: 60x84
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (25 + (40 * i), 275 + (3 * i)))
            i += 1

        draw_text("Split hand 2 value: ", text_font, black, screen_width // 2 + 250, 540)
        draw_text(str(user1.get_split_hand_2_value()), text_font, black, screen_width // 2 + 375, 540)

        draw_text("Split hand 2 result: ", text_font, black, screen_width // 2 + 250, 230)
        draw_text(str(user1.get_split_hand_2_result()), text_font, black, screen_width // 2 + 375, 230)



    if user1.get_split_hand_3_result() is not None:
        draw_text("Your 3rd split cards are: ", text_font, black, 25, 25)
        i = 0
        for card in user1.get_split_hand_3():
            image_file_name = card.get_image()
            img_size = (120, 168)  # Original size: 60x84
            load_string = "img/cards/all_cards/"
            final_image = load_string + image_file_name
            img = pygame.image.load(final_image)
            img = pygame.transform.scale(img, img_size)
            screen.blit(img, (25 + (40 * i), 75 + (3 * i)))
            i += 1

        draw_text("Split hand 3 value: ", text_font, black, screen_width // 2 + 250, 570)
        draw_text(str(user1.get_split_hand_3_value()), text_font, black, screen_width // 2 + 375, 570)

        draw_text("Split hand 3 result: ", text_font, black, screen_width // 2 + 250, 270)
        draw_text(str(user1.get_split_hand_3_result()), text_font, black, screen_width // 2 + 375, 270)

    if user1.get_can_user_bet() is True:
        draw_text("Place your bets!", big_text_font, black, screen_width // 2 - 125, 350)
        # Moving the non-functioning chips off-screen
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

        one_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55250,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
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

        five_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55300,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='5',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
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

        twenty_five_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55350,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='25',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
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

        one_hundred_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55400,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='100',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
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

        five_hundred_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55450,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='500',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
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

        one_thousand_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 55500,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1000',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        all_in_button = Button(
            screen,
            screen_width // 2 + 550,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            75,
            25,
            text='All In',
            fontSize=16, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_all_in
        )

        all_in_button_no_func = Button(
            screen,
            screen_width // 2 + 55550,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            75,
            25,
            text='All In',
            fontSize=16, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        if pot.get_bankroll() != 0:
            clear_bet_button = Button(
                screen,
                screen_width // 2 + 345,  # X coordinate of the top-left corner
                600,  # Y coordinate of the top-left corner
                125,
                25,
                text='Clear Bets',
                fontSize=20, margin=20,
                inactiveColour=(255, 0, 0),
                pressedColour=(0, 255, 0), radius=20,
                onClick=clear_bets
            )
            clear_bet_button.draw()
    else:
        clear_bet_button = Button(
            screen,
            screen_width // 2 + 54370,  # X coordinate of the top-left corner
            575,  # Y coordinate of the top-left corner
            125,
            25,
            text='Clear Bets',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=clear_bets
        )
        # Moving functioning chips off-screen
        one_dollar_chip = Button(
            screen,
            screen_width // 2 + 55250,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_one
        )

        one_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 250,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        five_dollar_chip = Button(
            screen,
            screen_width // 2 + 55300,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='5',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_five
        )

        five_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 300,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='5',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        twenty_five_dollar_chip = Button(
            screen,
            screen_width // 2 + 55350,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='25',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_twenty_five
        )

        twenty_five_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 350,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='25',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        one_hundred_dollar_chip = Button(
            screen,
            screen_width // 2 + 55400,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='100',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_one_hundred
        )

        one_hundred_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 400,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='100',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        five_hundred_dollar_chip = Button(
            screen,
            screen_width // 2 + 55450,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='500',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_five_hundred
        )

        five_hundred_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 450,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='500',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        one_thousand_dollar_chip = Button(
            screen,
            screen_width // 2 + 55500,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1000',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_one_thousand
        )

        one_thousand_dollar_chip_no_func = Button(
            screen,
            screen_width // 2 + 500,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            25,
            25,
            text='1000',
            fontSize=10, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

        all_in_button = Button(
            screen,
            screen_width // 2 + 55550,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            75,
            25,
            text='All In',
            fontSize=16, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=user_bet_all_in
        )

        all_in_button_no_func = Button(
            screen,
            screen_width // 2 + 550,  # X coordinate of the top-left corner
            650,  # Y coordinate of the top-left corner
            75,
            25,
            text='All In',
            fontSize=16, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )

    has_game_started()
    ready_to_draw_cards_check()
    show_user_card_image()
    show_dealer_card_image()
    if user1.get_are_cards_ready_to_be_drawn() is True:
        deal_cards_button = Button(
            screen,
            screen_width // 2 - 87,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            124,
            25,
            text='Draw cards',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=draw_cards_button_func
        )
        deal_cards_button.draw()
    else:
        deal_cards_button = Button(
            screen,
            screen_width // 2 - 55550,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            125,
            25,
            text='Draw cards',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
        )
        deal_cards_button.draw()

    if user1.get_hand() and user1.get_turn_result() == 'in-progress':
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
        hit_button.draw()
        stand_button.draw()
    else:
        hit_button = Button(
            screen,
            screen_width // 2 + 55350,  # X coordinate of the top-left corner
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
            screen_width // 2 + 55500,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            75,
            25,
            text='Stand',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=stand
        )
    if is_turn_over() is True and game_over_check() is not True:
        new_turn_button = Button(
            screen,
            screen_width // 2 - 87,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            124,
            25,
            text='New Turn',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=clear_table
        )
        draw_text("Dealer's hand value: ", text_font, black, screen_width // 2 - 80, 35)
        draw_text(str(dealer.get_hand_value()), text_font, black, screen_width // 2 + 80, 35)

        draw_text("Hand result: ", text_font, black, screen_width // 2 + 250, 150)
        draw_text(str(user1.get_turn_result()), text_font, black, screen_width // 2 + 350, 150)

        # Telling the user how many chips they gained or lost
        if user1.get_chips_gained_on_turn() > 0:
            chips_gained_text = "+" + str(user1.get_chips_gained_on_turn()) + " chips"
        else:
            chips_gained_text = str(user1.get_chips_gained_on_turn()) + " chips"
        draw_text(chips_gained_text, text_font, black, screen_width // 2 + 250, 110)
    elif game_over_check() is True and is_turn_over() is True:
        draw_text("Dealer's hand value: ", text_font, black, screen_width // 2 - 80, 35)
        draw_text(str(dealer.get_hand_value()), text_font, black, screen_width // 2 + 80, 35)

    elif is_turn_over() is False:
        new_turn_button = Button(
            screen,
            screen_width // 2 + 44350,  # X coordinate of the top-left corner
            4550,  # Y coordinate of the top-left corner
            125,
            25,
            text='New Turn',
            fontSize=20, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=clear_table
        )


        draw_text("Hand result: ", text_font, black, screen_width // 2 + 250, 150)
        draw_text(str(user1.get_turn_result()), text_font, black, screen_width // 2 + 350, 150)

        # Telling the user how many chips they gained or lost
        if user1.get_chips_gained_on_turn() > 0:
            chips_gained_text = "+" + str(user1.get_chips_gained_on_turn()) + " chips"
        else:
            chips_gained_text = str(user1.get_chips_gained_on_turn()) + " chips"
        draw_text(chips_gained_text, text_font, black, screen_width // 2 + 250, 110)

    if game_over_check() is not True:
        if user1.get_username() is None:
            draw_text("Enter username", big_text_font, black, screen_width // 2 - 120, 450)
            username_textbox.draw()

    if user1.get_is_split_hand_active() is True:
        pygame.draw.line(screen, (255, 0, 0), (30, 705), (130, 705), 3)

    if user1.get_is_split_hand_2_active() is True:
        pygame.draw.line(screen, (255, 0, 0), (30, 465), (130, 465), 3)

    if user1.get_is_split_hand_3_active() is True:
        pygame.draw.line(screen, (255, 0, 0), (30, 250), (130, 250), 3)

    if user1.get_split_hand() != [] and user1.get_is_split_hand_active() is False:
        pygame.draw.line(screen, (255, 0, 0), (screen_width // 2 - 90, 690), (screen_width // 2 + 50, 690), 3)

    if is_double_down_possible() is True:
        double_down_button.draw()

    if split_check() is True or split_check_2() is True or split_check_3() is True:
        if user1.get_split_count_this_turn() < 3 and user1.get_turn_result() == 'in-progress':
            split_button.draw()

    if game_over_check() is True:
        new_game_button = Button(
            screen,
            screen_width // 2 - 87,  # X coordinate of the top-left corner
            400,  # Y coordinate of the top-left corner
            174,
            25,
            text='New Game',
            fontSize=24, margin=20,
            inactiveColour=(255, 0, 0),
            pressedColour=(0, 255, 0), radius=20,
            onClick=new_game
        )
        draw_text("Game Over", big_text_font, black, screen_width // 2 - 75, 350)

    blackjack_check()
    pygame.display.flip()
    pygame.display.update()

    turn_over_check()


    pw.update(events)
    clock.tick(30)



pygame.quit()
