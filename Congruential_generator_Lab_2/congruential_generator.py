import time
import math

# n least significant bits to take
N_LSB = 14

class CongruentialGenerator:
  def __init__(self, a, b, m):
    self.a = a
    self.b = b
    self.m = m
    self.x = int(time.time() * 1000)
  
  def seed(self, s):
    self.x = s

  def random(self):
    random_value = (self.a * self.x + self.b) % self.m
    # Take N_LSB least significant bits
    if (random_value < 2**N_LSB):
        random_value = float(random_value / self.m)
    else:
        random_value = float(random_value / 2**N_LSB)

    return random_value
  
  def extractNBits(self,num,n): 
    # convert number into binary first
    binary = bin(num) 
    # remove first two characters
    binary = binary[2:]
    end = len(binary)
    start = end - n
    # extract k  bit sub-string
    nBitSubStr = binary[start : end+1]
    # convert extracted sub-string into decimal again
    return(int(nBitSubStr,2))

  def period(self):
    period = 0
    x = self.x
    x_ns = []
    x_n = (self.a*x + self.b) % self.m
    while not x_n in x_ns:
      x_ns.append(x_n)
      x = x_n
      x_n = (self.a*x + self.b) % self.m
      period += 1
    return period

def good_abm(n):
    # We will use 3 as the only prime component of m.
    # to easily find a-1 using q in rule #2 "if q is a prime that divides m
    # then q divides a-1 as well."
    m = 3
    while (m < n):
        m *= 3
        
    # First requisite. m and b primes between each other.
    b = int(m/2 + 1)
    # Dont check even numbers
    if (b%2 == 0):
        b += 1
    while (not is_prime(b)):
        b += 2
    
    # Second requisite. if q is a prime that divides m, it will also divide a-1.
    q = 3
    a = int(m/2)
    while (not (a % q == 0)):
        a += 1
    
    # set a from a-1
    a += 1
    
    return a,b,m  

def is_prime(b):
    is_prime = True
    
    if (not (b == 2)):
        if (b%2 == 0):
            is_prime = False
        else:
            for i in range(3, int(math.sqrt(b)+1)):
                if (b%i) == 0:
                    is_prime = False
                # Dont check even numbers.
                i += 1
    return is_prime

# Test
cg = CongruentialGenerator(3,2,34)
print(cg.random())
print(cg.period())
cg = CongruentialGenerator(52,19,17)
print(cg.period())

a,b,m = good_abm(10)
cg = CongruentialGenerator(a, b, m)
print(cg.period())