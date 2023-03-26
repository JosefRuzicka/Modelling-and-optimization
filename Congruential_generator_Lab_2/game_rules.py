from card import Card

def compare_hands(player, opponent):
  # Player cardsn
  player = sort_cards(player)
  # Opponent cards
  opponent = sort_cards(opponent)
  result = get_winner(player.copy(), opponent.copy())

  return result

#--------------------- RULES -------------------#
# Call with cards of same suit
def royal_flush(cards_numbers):
  is_rf = False
  if (1 in cards_numbers and 10 in cards_numbers and 11 in cards_numbers and 12 in cards_numbers and 13 in cards_numbers):
    is_rf = True
  #print("IS RF: ", is_rf)
  return is_rf

# Call with cards of same suit
def straight_flush(cards_numbers):
  is_sf = True
  card_num = cards_numbers.pop(0)
  for num in cards_numbers:
    # card's number(num) should be higher by one than card_num
    if (card_num + 1 != num):
      if not(card_num == 13 and num == 1):
        is_sf = False
    card_num = num
  #print("IS SF: ", is_sf)
  return is_sf

def four_of_a_kind(cards_numbers):
  is_foak = False
  cards_count = count_card_numbers_frequency(cards_numbers)
  if (cards_count[max(cards_count, key=cards_count.get)] == 4):
    is_foak = True
  #print(is_foak)
  return is_foak

def full_house(cards_numbers):
  is_fh = False
  cards_count = count_card_numbers_frequency(cards_numbers)
  three = False
  pair = False
  for number in cards_count.keys():
    if (cards_count[number] == 2):
      pair = True
    if (cards_count[number] == 3):
      three = True
  is_fh = pair and three
  #print("IS FH: ", is_fh)
  return is_fh

def are_all_same_suit(cards):
  same_suit = True
  first_suit = cards.pop().suit
  for card in cards:
    if card.suit != first_suit:
      same_suit = False
  return same_suit

def straight(cards):
    straight = True
    cards = sort_cards(cards)
    card_numbers = get_hand_numbers(cards)
    for i in range(len(card_numbers)-1):
        if (not (card_numbers[i] + 1 == card_numbers[i+1])):
            straight = False
    return straight

def three_of_a_kind(cards_numbers):
  is_toak = False
  cards_count = count_card_numbers_frequency(cards_numbers)
  if (cards_count[max(cards_count, key=cards_count.get)] == 3):
    is_toak = True

  return is_toak

def two_pair(cards_numbers):
    two_pair = False
    pair_count = 0
    cards_count = count_card_numbers_frequency(cards_numbers)
    for i in cards_count.values():
        if (i == 2):
            pair_count += 1
    if (pair_count == 2):
        two_pair = True
    return two_pair

def one_pair(cards_numbers):
  one_pair = False
  cards_count = count_card_numbers_frequency(cards_numbers)
  if (cards_count[max(cards_count, key=cards_count.get)] == 2):
    one_pair = True
  return one_pair


def high_card(player_cards_numbers, opponent_cards_numbers):
    winner_defined = False
    counter = 0
    result = "tie"
    n_cards = len(player_cards_numbers)
    while ((not winner_defined) and counter < n_cards):
        # give Ace a higher value.
        if (player_cards_numbers[-1] == 1):
            player_cards_numbers[-1] += 13
        if (opponent_cards_numbers[-1] == 1):
            opponent_cards_numbers[-1] += 13
            
        if (player_cards_numbers[-1] > opponent_cards_numbers[-1]):
            winner_defined = True
            result = "player"
        elif (player_cards_numbers[-1] < opponent_cards_numbers[-1]):
            winner_defined = True
            result = "opponent"
        else:
            player_cards_numbers.pop()
            opponent_cards_numbers.pop()
        counter += 1
    return result

#----------------- TIE BREAKS ---------------------#
# n = 3 OR n = 4
def n_of_a_kind_tiebreak(player_cards_numbers, opponent_cards_numbers, n):
  result = "tie"
  p_cards_count = count_card_numbers_frequency(player_cards_numbers)
  o_cards_count = count_card_numbers_frequency(opponent_cards_numbers)
  
  # Get value of card that appears 4 times
  p_repeated_number = max(p_cards_count, key=p_cards_count.get)
  o_repeated_number = max(o_cards_count, key=o_cards_count.get)

  if (p_repeated_number > o_repeated_number):
    result = "player"
  elif (p_repeated_number < o_repeated_number):
    result = "opponent"
  else:
    # Remove repeated number cards 
    result = high_card(player_cards_numbers, opponent_cards_numbers)
  return result

def four_of_a_kind_tiebreak(player_cards_numbers, opponent_cards_numbers):
  result = "tie"
  
  p_cards_count = count_card_numbers_frequency(player_cards_numbers)
  o_cards_count = count_card_numbers_frequency(opponent_cards_numbers)
  
  # Get value of card that appears 4 times
  p_four = max(p_cards_count, key=p_cards_count.get)
  o_four = max(o_cards_count, key=o_cards_count.get)

  if (p_four > o_four):
    result = "player"
  elif (p_four < o_four):
    result = "opponent"
  else:
    result = high_card(player_cards_numbers, opponent_cards_numbers)
  return result

def full_house_tiebreak(player_cards_numbers, opponent_cards_numbers):
  result = "tie"
  # Get trio
  p_trio = player_cards_numbers[-1]
  o_trio = opponent_cards_numbers[-1]

  # First check highest trio
  if (p_trio > o_trio):
    result = "player"
  elif (p_trio < o_trio):
    result = "opponent"
  else:
    # Check highest pair
    p_pair = player_cards_numbers[0]
    o_pair = player_cards_numbers[0]
    if (p_pair > o_pair):
      result = "player"
    elif (p_pair < o_pair):
      result = "opponent"
  return result

def two_pair_tiebreak(player_cards_numbers, opponent_cards_numbers):
  result = "tie"
  # Revert to find the highest pair first
  player_cards_numbers.reverse()
  opponent_cards_numbers.reverse()
  p_cards_count = count_card_numbers_frequency(player_cards_numbers)
  o_cards_count = count_card_numbers_frequency(opponent_cards_numbers)
  
  # Get highest pair
  p_pair = max(p_cards_count, key=p_cards_count.get)
  o_pair = max(o_cards_count, key=o_cards_count.get)

  if (p_pair > o_pair):
    result = "player"
  elif (p_pair < o_pair):
    result = "opponent"
  else:
    # Remove highest pair 
    for i in range(2):
      player_cards_numbers.remove(p_pair)
      opponent_cards_numbers.remove(o_pair)
    # Compare other three cards
    result = one_pair_tiebreak(player_cards_numbers, opponent_cards_numbers)
  return result

def one_pair_tiebreak(player_cards_numbers, opponent_cards_numbers):
  result = "tie"

  p_cards_count = count_card_numbers_frequency(player_cards_numbers)
  o_cards_count = count_card_numbers_frequency(opponent_cards_numbers)
  # Get pair
  p_pair = max(p_cards_count, key=p_cards_count.get)
  o_pair = max(o_cards_count, key=o_cards_count.get)
  
  if (p_pair > o_pair):
    result = "player"
  elif (p_pair < o_pair):
    result = "opponent"
  else:
    result = high_card(player_cards_numbers, opponent_cards_numbers)
  return result



''' This tiebreak works for: straight flush, flush and straight'''
def straight_flush_tiebreak(player_cards_numbers, opponent_cards_numbers):
    result = "tie"
    if (player_cards_numbers[-1] > opponent_cards_numbers[-1]):
        result = "player"
    elif (player_cards_numbers[-1] < opponent_cards_numbers[-1]):
        result = "opponent"
    return result

def get_hand_numbers(cards):
  numbers = []
  for card in cards:
    numbers.append(card.number)
  return numbers

def get_hand_suits(cards):
  suits = []
  for card in cards:
    suits.append(card.suit)
  return suits

def sort_cards(cards):
  count = len(cards)-1
  while count > 0:
    for i in range(count):
      if cards[i].number > cards[i+1].number:
        temp_card = cards[i]
        cards[i] = cards[i+1]
        cards[i+1] = temp_card
    count -= 1
  return cards

def count_card_numbers_frequency(cards_numbers):
  cards_count = {}
  for num in cards_numbers:
    if not num in cards_count:
      cards_count[num] = 1
    else:
      cards_count[num] += 1
  return cards_count

def get_winner(player, opponent):
  p_numbers = get_hand_numbers(player)
  p_score = 10
  
  o_numbers = get_hand_numbers(opponent)
  o_score = 10
  
  stop_condition = False
  
  # Check royal flush.
  if (royal_flush(p_numbers)):
    p_score = 1
  if (royal_flush(o_numbers)):
    o_score = 1
  if (not (p_score == o_score)):
      stop_condition == True
  elif(p_score == 1):
      result = "tie"
      stop_condition == True
      
  # check straight flush.    
  if (not (stop_condition)):
    if (straight_flush(p_numbers)):
      p_score = 2
    if (straight_flush(o_numbers)):
      o_score = 2
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 2):
      result = straight_flush_tiebreak(p_numbers, o_numbers);
      stop_condition == True
          
  # check foak.    
  if (not (stop_condition)):
    if (four_of_a_kind(p_numbers)):
      p_score = 3
    if (four_of_a_kind(o_numbers)):
      o_score = 3
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 3):
      #result = foak_tiebreak(p_numbers, o_numbers);
      stop_condition == True
            
  # check full house.    
  if (not (stop_condition)):
    if (full_house(p_numbers)):
      p_score = 4
    if (full_house(o_numbers)):
      o_score = 4
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 4):
    #result = full_house_tiebreak(p_numbers, o_numbers);
      stop_condition == True

  # check flush.    
  if (not (stop_condition)):
    if (are_all_same_suit(player)):
      p_score = 5
    if (are_all_same_suit(opponent)):
      o_score = 5
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 5):
      result = straight_flush_tiebreak(p_numbers, o_numbers);
      stop_condition == True
    
  # check straight.    
  if (not (stop_condition)):
    if (straight(player)):
      p_score = 6
    if (straight(opponent)):
      o_score = 6
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 6):
      result = straight_flush_tiebreak(p_numbers, o_numbers);
      stop_condition == True
          
  # check toak.    
  if (not (stop_condition)):
    if (three_of_a_kind(p_numbers)):
      p_score = 7
    if (three_of_a_kind(o_numbers)):
      o_score = 7
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 7):
      #result = toak_tiebreak(p_numbers, o_numbers);
      stop_condition == True
          
  # check two_pair.    
  if (not (stop_condition)):
    if (two_pair(p_numbers)):
      p_score = 8
    if (two_pair(o_numbers)):
      o_score = 8
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 8):
      #result = two_pair_tiebreak(p_numbers, o_numbers);
      stop_condition == True
          
  # check pair.    
  if (not (stop_condition)):
    if (one_pair(p_numbers)):
      p_score = 9
    if (one_pair(o_numbers)):
      o_score = 9
    if (not (p_score == o_score)):
      stop_condition == True
    # tiebreak
    elif (p_score == 9):
      #result = one_pair_tiebreak(p_numbers, o_numbers);
      stop_condition == True
        
  # compare scores.
  if (p_score < o_score):
    result = "player"
  elif(p_score > o_score):
    result = "opponent"
  else:
    result = high_card(p_numbers, o_numbers)
      
  return result