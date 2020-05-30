import numpy as np

def readable_to_array(hand):
    converted_hand = []
    for card in hand:
        converted_hand.append(card[0] + card[1]*13)
    return converted_hand

def get_cards_by_suits(suit_set):
    deck = np.arange(0,52)
    cards = set()
    for card in deck:
        if num_to_suit(card) in suit_set:
            cards.add(card)
    return cards

def is_greater_than(a, b, trump_suit):
    a_suit = num_to_suit(a)
    b_suit = num_to_suit(b)

    if a_suit == trump_suit and b_suit == trump_suit:
        return num_to_rank(a) > num_to_rank(b)
    elif a_suit == trump_suit:
        return True
    else:
        return False

def num_to_suit(num):
    return num//13

def num_to_rank(num):
    return num % 13
