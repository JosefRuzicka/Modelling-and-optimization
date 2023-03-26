from queue import Queue
from queue_system_utils import *

def main():
    queue = Queue(15, 3, 'markovian', lambd,'markovian', mu)
    queue.simulation(1000, 1, 15)

if __name__ == "__main__":
    main()