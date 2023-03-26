class Card:
  def __init__(self, number, suit):
    self.number = number
    self.suit = suit
  
  def seed(self, s):
    self.x = s

  def to_string(self):
    return "num: " + str(self.number) + ", suit: " + self.suit

def get_deck():
    deck = []
    suit = ""
    for i in range(4):
        if (i == 0):
            suit = "Hearts"
        elif(i == 1):
            suit = "Diamonds"
        elif(i == 2):
            suit = "Clubs"
        elif(i == 3):
            suit = "Spades"
        for j in range(13):
            deck.append(Card(j+1, suit))
    return deck