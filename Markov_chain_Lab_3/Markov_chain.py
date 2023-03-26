
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 09:59:23 2022

@author: Josef Ruzicka, Gilberth Marquez.
Optimization Modeling,  Lab 3.
"""

import random
import numpy as np
import math
def load_words(fileName):
    with open(fileName) as f:
        data = [line.rstrip('\n') for line in f]
    return data
    
def add_decorators(words, decorator, n):
    decorated_words = []
    for word in words:
        word = word.lower()
        for i in range(n):
            word = decorator + word + decorator
        decorated_words.append(word)
    return decorated_words

def get_sequences(words, n):
    sequences = []
    for word in words:
        for char in range(len(word)-n):
            sequence = ''
            for i in range(n):
                sequence = sequence + word[char+i]
            sequences.append(sequence)
    # remove duplicates and sort.
    sequences = sorted(list(dict.fromkeys(sequences)))
    return sequences

def calculate_transitions(words, sequences):
    sequence_matrix = []
    # Iterate over all sequences as a matrix
    # rows
    for current_sequence in sequences:
        sequence_row = []
        total_ocurrences_count = 0
        # columns
        for comparison_sequence in sequences:
            ocurrences_count_per_sequence = 0
            for word in words:
                # Count ocurrences of current sequence followed by comparison sequence
                combined_sequence = current_sequence + comparison_sequence
                ocurrences = [i for i in range(len(word)) if word.startswith(combined_sequence, i)]
                ocurrences_count_per_sequence += len(ocurrences)
                total_ocurrences_count += len(ocurrences)
            sequence_row.append(ocurrences_count_per_sequence)
        # Calculate probability
        if (total_ocurrences_count > 0):
            for i in range(len(sequence_row)):
                sequence_row[i] = format(float(sequence_row[i]/total_ocurrences_count))
        sequence_matrix.append(sequence_row)                
    return sequence_matrix
    
def create_model(words, ngrams):
    decorated_words = add_decorators(words, '$', ngrams)
    sequences       = get_sequences(decorated_words, ngrams)
    transitions     = calculate_transitions(decorated_words, sequences)
    return transitions, sequences

def generate_word(model, seed):
    word = ""
    transitions = model[0]
    sequence = model[1]
    
    init_final_state = sequence[0]

    state = init_final_state
    state_index = 0
    r = random.Random()
    r.seed(seed)

    # First, loop for decorator (init_state)
    r_val = r.random()
    # init state, state_index = 0
    for i in range(len(transitions[state_index])):
        if (r_val < float(transitions[state_index][i])):
            state = sequence[i]
            state_index = i
            word += state
            break;
        else:
            r_val = r_val - float(transitions[state_index][i])
    
    num_decorators = "$" * len(sequence[0])
    # Loop until decorator (final_state)
    while state != init_final_state:
        r_val = r.random()
        for i in range(len(transitions[state_index])):
            if (r_val < float(transitions[state_index][i])):
                state = sequence[i]
                state_index = i
                
                if (state != num_decorators):
                    word += state
                break;
            else:
                r_val = r_val - float(transitions[state_index][i])
    return word

def get_probability(model, word):
    transitions = model[0]
    sequences = model[1]
    word = word.lower()
    
    len_sequence = len(sequences[0])
    word = add_decorators([word], "$", len_sequence)[0]

    probability = 0

    # Iterate rows of matrix of transitions
    for i in range(len(sequences)):
        # Find index of letter in word
        index = word.find(sequences[i])

        if index != -1:
            #Find the letter/letters in the matrix of transitions, then add to probability
            for j in range(len(sequences)):
                # Compare letter/letters of word with sequence
                if (word[index+1: index + 1 + len_sequence] == sequences[j]):
                    if probability == 0:
                        probability += float(transitions[i][j])
                    else:
                        probability = probability * float(transitions[i][j])
                    break;
    return probability

# main
data = load_words('pokemon.csv')
#transitions, sequences = create_model(data, 1)



# tests.
#sequences = get_sequences(['$hello$','$world$'], 1)
#sequences = get_sequences(['$$hello$$','$$world$$'], 2)
#transitions = calculate_transitions(['$hello$','$world$'], ['$','d','e','h','l','o','r','w'])
#transitions = calculate_transitions(['$$hello$$','$$world$$'], sequences)
#transitions, sequences = create_model(['hello', 'world'], 1)
model = create_model(data, 3)
#print(model[1])
#print(model[0])
word = generate_word(model, 21)
print("WORD: ", word)

prob = get_probability(model, "mew")
print(prob)

#print(data)
#print(decorated_data)
#print(model[0])
#print(model[1])

