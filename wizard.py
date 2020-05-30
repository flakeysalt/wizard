import copy
import numpy as np
import card_utils as cu
from player import Player

NUM_PLAYERS = 7
NUM_GAMES = 1
NUM_DEALT = 6
'''
The hand you wish to find out what to bet
'''
READABLE_HAND = [(6,1), (5,1), (12,0), (9,1), (7,2), (2,0)]
HAND = cu.readable_to_array(READABLE_HAND)
print(HAND)
'''
The position you are playing
'''
POS = 3
'''
The trump card in the game
'''
TRUMP = 8
def evaluate(cards_played_round, trump_suit):
    print(cards_played_round[0])
    trick_suit = cu.num_to_suit(cards_played_round[0])

    idx_possible_wins = [i for i,card in enumerate(cards_played_round) if cu.num_to_suit(card) == trump_suit]
    if len(idx_possible_wins) == 0:
        idx_possible_wins = [i for i,card in enumerate(cards_played_round) if cu.num_to_suit(card) == trick_suit]
    max = 0
    max_idx = 0
    for i in idx_possible_wins:
        if cards_played_round[i] > max:
            max = cards_played_round[i]
            max_idx = i

    return max_idx, max

def play_wizard(players, trump_suit):
    wins = [0]*NUM_PLAYERS
    game_info = []
    order = list(range(NUM_PLAYERS))

    for i in range(len(players[0].hand)):
        cards_played_round = []
        for i in order:
            #update player knowledge
            players[i].info['seen'].update(game_info)
            players[i].info['pos'] = i + 1

            #play
            card = players[i].play()
            print("card",card)

            #record
            cards_played_round.append(card)
            game_info.append(card)

        #evaluate who won
        print("cards_played_round:",cards_played_round)
        card_won_idx, card_won = evaluate(cards_played_round, trump_suit)
        print("card_won:",card_won,"card_won_idx:",card_won_idx,"order:",order)
        wins[order[card_won_idx]] += 1

        #update the order
        b = order[0:i]
        order = order[i:]
        order.extend(b)
    return wins
if __name__ == "__main__":
    hand_wins = []
    for i in range(NUM_GAMES):
        print("HAND:",HAND)
        deck = set(np.arange(0,52))
        deck = list(deck.difference(set(HAND+[TRUMP])))
        np.random.shuffle(deck)
        deck = deck[1:]
        players = []
        # initialize the players
        for id in range(NUM_PLAYERS):
            if id + 1 == POS:
                players.append(Player(id, copy.deepcopy(HAND), NUM_PLAYERS, TRUMP, threshold=0.5))
            else:
                players.append(Player(id, deck[0:NUM_DEALT], NUM_PLAYERS, TRUMP))
                deck = deck[NUM_DEALT:]

        # play the game
        wins = play_wizard(players, cu.num_to_suit(TRUMP))
        print(wins)
        hand_wins.append(wins[POS-1])
    print("Average Wins:",np.mean(hand_wins),"STDEV:", np.std(hand_wins))
    unique, counts = np.unique(hand_wins, return_counts=True)
    win_count = dict(zip(unique, counts))
    print("Win Count:", win_count)
