def load_words(filename):
  print("load_words")


def add_decorators(words, decorator, n):
  print("add_decorators")
# Test
add_decorators(["hello","world"], "$", 1)
add_decorators(["hello","world"], "$", 2)

def get_sequences(words, n):
  print("get_sequences")

#Test
get_sequences(["$hello$", "$world$"], 1)
get_sequences(["$$hello$$", "$$world$$"], 2)

def calculate_transitions(words, sequences):
  print("calculate_transitions")

#Test
calculate_transitions(["$hello$", "$world$"], ["$","d","e","h","l","o", "r", "w"])