import numpy as np


def numToSuit(num):
    return num//13

def numToRank(num):
    return num % 13

if __name__ == "__main__":
    num_players = 7
    num_dealt = 1
    player_wins = np.zeros(num_players)
    card_wins = np.zeros(52)
    player_rank_wins = np.zeros((num_players,13))
    player_rank_losses = np.zeros((num_players,13))
    player_rank_percentages = np.zeros((num_players,13))

    player_rank_trump_wins = np.zeros((num_players,13))
    player_rank_trump_losses = np.zeros((num_players,13))
    player_rank_trump_percentages = np.zeros((num_players,13))

    player_rank_trick_wins = np.zeros((num_players,13))
    player_rank_trick_losses = np.zeros((num_players,13))
    player_rank_trick_percentages = np.zeros((num_players,13))

    trick_suit_wins = 0
    trump_suit_wins = 0
    count = 0
    iter = 100000

    for i in range(iter):
        #1) Deal and reveal trump suit
        deck = np.arange(0, 52)
        # print(deck)
        np.random.shuffle(deck)
        # print(deck)
        trump = deck[0]
        trump_suit = numToSuit(trump)
        deck = deck[1:]
        # print(trump,deck)
        hands = []
        for p in range(num_players):
            hands.append(deck[0:num_dealt])
            deck = deck[num_dealt:]
        # print(hands)

        #2) Bet where the sum of bets cannot be equal to number of cards dealt to each player
        #no betting for now, part of agent probably


        #3) Reveal a card, highest card takes trick
        trick_suit = 0
        for hand in hands:
            if numToRank(hand[0]) != 0:
                trick_suit = numToSuit(hand[0])
                break
        # curr_max_rank = numToRank(hand[0][0])

        # for p, hand in enumerate(hands):
        #     hand_suit = numToSuit(hand[0])
        #     if hand_suit == trump_suit:
        idx_possible_wins = [i for i,hand in enumerate(hands) if numToSuit(hand[0]) == trump_suit and numToRank(hand[0]) != 0]
        if len(idx_possible_wins) == 0:
            idx_possible_wins = [i for i,hand in enumerate(hands) if numToSuit(hand[0]) == trick_suit and numToRank(hand[0]) != 0]

        # print(idx_possible_wins)
        if len(idx_possible_wins) != 0:
            possible_wins = [hands[i] for i in idx_possible_wins]
            winning_card_idx = np.argmax([numToRank(hand) for hand in possible_wins])
            winning_card = possible_wins[winning_card_idx]
            winning_player = hands.index(winning_card)
            winning_suit = numToSuit(winning_card)
            winning_rank = numToRank(winning_card)
            losing_players = [i for i in range(num_players) if i != winning_player]
            losing_players_ranks = [numToRank(hands[i]) for i in losing_players]
            losing_players_suits = [numToSuit(hands[i]) for i in losing_players]

            if winning_suit == trump_suit:
                trump_suit_wins += 1
                player_rank_trump_wins[winning_player, winning_rank] += 1
            else:
                trick_suit_wins += 1

            card_wins[winning_card] += 1
            player_wins[winning_player] += 1
            player_rank_wins[winning_player, winning_rank] += 1
            player_rank_losses[losing_players, losing_players_ranks] += 1

            for i,suit in enumerate(losing_players_suits):
                if suit == trump_suit:
                    player_rank_trump_losses[losing_players[i], losing_players_ranks[i]] += 1
        else:
            count += 1

    print("card_wins:",card_wins)
    print("card win percentages:", [val/iter for val in card_wins])
    print("player_wins:",player_wins,"win percentage:",[val/iter for val in player_wins])
    print("trump_suit_wins:",trump_suit_wins, "trick_suit_wins:", trick_suit_wins)
    print("player_rank_wins:",player_rank_wins)
    print("player_rank_losses:",player_rank_losses)

    for i in range(num_players):
        for j in range(13):
            player_rank_percentages[i,j] = player_rank_wins[i,j]/(player_rank_wins[i][j]+player_rank_losses[i,j])
            player_rank_trump_percentages[i,j] = player_rank_trump_wins[i,j]/(player_rank_trump_wins[i][j]+player_rank_trump_losses[i,j])

            player_rank_trick_wins[i,j] = player_rank_wins[i,j] - player_rank_trump_wins[i,j]
            player_rank_trick_losses[i,j] = player_rank_losses[i,j] - player_rank_trump_losses[i,j]
            player_rank_trick_percentages[i,j] = player_rank_trick_wins[i,j]/(player_rank_trick_wins[i][j]+player_rank_trick_losses[i,j])
    print("player_rank_percentages:",player_rank_percentages)

    print("player_rank_trump_wins:",player_rank_trump_wins)
    print("player_rank_trump_losses:",player_rank_trump_losses)
    print("player_rank_trump_percentages:",player_rank_trump_percentages)
    print("player_rank_trick_percentages:",player_rank_trick_percentages)

    print("count of games where no one won:",count)

    #4) Reward players based on bet and tricks won
