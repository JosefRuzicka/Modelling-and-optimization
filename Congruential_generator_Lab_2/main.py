"""
Created on Wed Oct 19 17:22:26 2022

@author: Josef Ruzicka & Gilbert Marquez
"""

from card import Card, get_deck
from game_rules import compare_hands
from congruential_generator import CongruentialGenerator, good_abm
#nimport random
import math
import itertools

def main():
    opponents = 1
    #rolls = 100000
    rolls = 100
    #a,b,m = good_abm(10000001)
    
    # Set congruential generator
    a,b,m = good_abm(1000)
    cg = CongruentialGenerator(a, b, m)
    print ("m: ", m, " period: " ,cg.period())
    
    # get deck for test 1.
    # set initial players hand
    p_hand = []
    p_hand.append(Card(14, "Hearts"))
    p_hand.append(Card(14, "Diamonds"))
    deck = get_deck()
    deck.pop(0)  # remove ace of hearts
    deck.pop(13) # remove ace of diamonds 
    simulate(p_hand, rolls, cg, opponents, deck)
    
    # get deck for test 2.
    p_hand = []
    p_hand.append(Card(2, "Hearts"))
    p_hand.append(Card(2, "Diamonds"))
    deck = get_deck()
    deck.pop(1)  # remove 2 of hearts
    deck.pop(14) # remove 2 of diamonds 
    simulate(p_hand, rolls, cg, opponents, deck)
    
    # get deck for test 2.
    p_hand = []
    p_hand.append(Card(2, "Hearts"))
    p_hand.append(Card(7, "Diamonds"))
    deck = get_deck()
    deck.pop(2)  # remove 2 of hearts
    deck.pop(20) # remove 7 of diamonds 
    simulate(p_hand, rolls, cg, opponents, deck)
    
def simulate(initial_cards, rolls, generator, opponents, sim_deck):
    wins  = 0
    ties  = 0
    loses = 0
    
    for roll in range(rolls):
        #print("roll: ", roll)
        # reset deck
        deck = sim_deck.copy()
        #random.shuffle(deck)
        # Set up opponent hands
        o_hands = []
        for opponent in range(opponents):
            o_hand = []
            o_hand.append(deck.pop(int(generator.random() * len(deck))))
            o_hand.append(deck.pop(int(generator.random() * len(deck))))
            o_hands.append(o_hand)
        
        # Set up game cards
        game_cards = []
        for i in range(5):
            game_cards.append(deck.pop(int(generator.random() * len(deck))))
        
        # get best player hand.
        # Get all possible player hands.
        player_total_cards = initial_cards + game_cards
        player_hands = list(itertools.combinations(player_total_cards, 5))
        #player_hands = printPowerSet(player_total_cards, 7)
        #player_hands = n_length_combo(player_total_cards, 7)
        # choose winning hand
        player_winning_hand = list(player_hands[0])
        for i in range(len(player_hands)):
            result = compare_hands(player_winning_hand, list(player_hands[i]))
            if (result == "opponent"):
                player_winning_hand = list(player_hands[i])
        
        
        
        # choose opponents winning hands.
        o_winning_hands = []
        for opponent in range(opponents):
            opponent_total_cards = o_hands[opponent] + game_cards
            opponent_hands = list(itertools.combinations(opponent_total_cards, 5))
            #opponent_hands = printPowerSet(opponent_total_cards, 7)
            #opponent_hands = n_length_combo(opponent_total_cards, 7)
            # choose winning hand
            opponent_winning_hand = list(opponent_hands[0])
            for i in range(len(opponent_hands)):
                # Get all possible opponent hands.
                result = compare_hands(opponent_winning_hand, list(opponent_hands[i]))
                if (result == "opponent"):
                    opponent_winning_hand = list(opponent_hands[i])
            o_winning_hands.append(opponent_winning_hand)
            
        # get game winner.
        for opponent in range(opponents):
            result = compare_hands(player_winning_hand, o_winning_hands[opponent])
            if (result == "opponent"):
                loses += 1
                break
        if (result == "tie"):
            ties += 1
        elif (result == "player"):
            wins += 1
    
    # Todo convert to %
    #print ("wins: ", wins, " ties: ", ties, " loses: ", loses)
    return wins, ties, loses
        
        
        
# Other attempts to get possible combinations.
# python3 program for power set
# Adapted from https://www.geeksforgeeks.org/power-set/
def get_all_combinations(set, set_size):
     
    # set_size of power set of a set
    # with set_size n is (2**n -1)
    pow_set_size = (int) (math.pow(2, set_size));
    counter = 0;
    j = 0;
    list_of_combinations = []
    # Run from counter 000..0 to 111..1
    for counter in range(0, pow_set_size):
        combination = []
        for j in range(0, set_size):
            # Check if jth bit in the
            # counter is set If set then
            # print jth element from set
            if((counter & (1 << j)) > 0):
                combination.append(set[j])
                #print(set[j].to_string(), end = "");
        #for c in combination:
        #    print(c.to_string())
        if (len(combination) == 5 ):
            list_of_combinations.append(combination)
        combination.clear()
    return list_of_combinations

# Function to create combinations
# without itertools
def get_all_combinations_without_itertools(lst, n):
     
    if n == 0:
        return [[]]
     
    l =[]
    for i in range(0, len(lst)):
         
        m = lst[i]
        remLst = lst[i + 1:]
         
        remainlst_combo = n_length_combo(remLst, n-1)
        for p in remainlst_combo:
             l.append([m, *p])
           
    return l

main() 

     