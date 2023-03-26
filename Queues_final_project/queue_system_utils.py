import math
import random

def degenerate(lambd):
    return lambd

def markovian(lambd):
    return (-1 * math.log(1 - random.random()))/lambd

"""
    Returns the lambda value.
    n: ammount of clients.
"""
def lambd(n):
    lambd = 64 - n ** -1.5
    return lambd

"""
    Returns the mu value.
    n: ammount of clients.
"""
def mu(n):
    mu = 5 + 3*n
    return mu
