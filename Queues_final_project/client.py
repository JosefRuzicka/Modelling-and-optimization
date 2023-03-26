class Client:
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.attention_time = 0
        self.exit_time = 0
    
    def calc_waiting_time(self):
        return self.exit_time - self.arrival_time - self.calc_attention_time()

    def calc_attention_time(self):
        return self.exit_time - self.attention_time
    
