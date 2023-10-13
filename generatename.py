import random

filef = open("misc\\firstnames.txt", "r")
first = filef.readlines()

filel = open("misc\\lastnames.txt", "r")
last = filel.readlines()

filef.close()
filel.close()

def make():
    temp = (first[random.randint(0, len(first)-1)] + "_" + last[random.randint(0, len(last)-1)]).replace("\n", "").upper()
    if len(temp) < 14: return temp
    return make()
