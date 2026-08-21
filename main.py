import random
import math

def tirar_dados():
    return math.floor(random.random() * 6) + 1

for i in range(10):
    print(tirar_dados())