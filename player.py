import numpy as np
import card_utils as cu

class Player:

    def __init__(self, id, hand, num_players, trump_card, threshold=0.5):
        self.info = {
            'bet': None,
            'seen': set(np.append(hand,trump_card)),
            'trick': None,
            'trump': cu.num_to_suit(trump_card),
            'pos': id + 1,
            'round': set()
        }
        # self.bet_info = None
        # self.seen_cards = set()
        self.id = id
        self.hand = hand
        print("player",hand)
        self.hand_suits = list(map(cu.num_to_suit, hand))
        self.hand_ranks = list(map(cu.num_to_rank, hand))
        self.num_players = num_players
        self.threshold = threshold

    def find_num_higher_remaining(self, card, trump, seen):
        '''
        Finds the number of remaining cards of the same or trump suit that
        haven't been played yet.
        '''
        deck = set(np.arange(0,52))
        candidates = cu.get_cards_by_suits(set([trump, cu.num_to_suit(card)]))
        remaining = deck.difference(seen)
        remaining = remaining.difference(candidates)
        num_higher = 0

        for rc in remaining:
            if cu.num_to_suit(card) != cu.num_to_suit(rc):
                num_higher += 1
            elif cu.num_to_rank(rc) > cu.num_to_rank(card):
                num_higher += 1

        return num_higher

    def check_overall_win_prob(self):
        '''
        Find out the probability someone else has a card higher
        than each card in your hand. Returns the probability each
        card has to win.
        '''
        deck = set(np.arange(0,52))
        remaining = deck.difference(self.info['seen'])
        players_left = self.num_players - self.info['pos']
        win_probs = []
        for card in self.hand:
            num_higher = self.find_num_higher_remaining(card, self.info['trump'], self.info['seen'])
            complement = 1
            for i in range(players_left):
                complement *= (num_higher - i)/(len(remaining)-i)
            win_probs.append(1-complement)

        return win_probs

    def evaluate_hand(self, win_probs):
        '''
        If the win percentage of the highest, legal-play card is over threshold,
        return that index. Otherwise, return the index of the lowest probability
        legal-play card. Also includes logic for looking at cards played in that
        round. If a higher card of trick/trump is already played, do not play
        your high probability cards.
        '''
        candidates = []
        candidates_idx = []
        if self.info['trick'] in self.hand_suits:
            for i, s in enumerate(self.hand_suits):
                if s == self.info['trick']:
                    candidates_idx.append(i)
                    candidates.append(self.hand[s])
        else:
            candidates = list(range(len(self.hand)))

        candidates_prob = [win_probs[i] for i in candidates]
        is_greater_than_played = [True]*len(candidates)
        for i,candidate in enumerate(candidates):
            for card in self.info['round']:
                if not cu.is_greater_than(candidate, card, self.info['trump']):
                    is_greater_than_played[i] = False
                    break
        max_idx = np.argmax(np.multiply(candidates_prob,is_greater_than_played))
        min_idx = np.argmin(candidates_prob)

        if candidates_prob[max_idx] >= self.threshold:
            return candidates[max_idx]
        else:
            return candidates[min_idx]

    def play(self):
        '''
        Check the probabilities someone has a card higher than yours,
        evaluates the hand to find the index to play, then plays the
        card by returning it and removing it from your hand.
        '''
        overall_win_probs = self.check_overall_win_prob()
        pos_to_play = self.evaluate_hand(overall_win_probs)
        self.hand_suits.pop(pos_to_play)
        self.hand_ranks.pop(pos_to_play)

        return self.hand.pop(pos_to_play)
