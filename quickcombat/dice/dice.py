from random import randint

def d4(): 
    return randint(1,4)

def d6(): 
    return randint(1,6)

def d8(): 
    return randint(1,8)

def d12(): 
    return randint(1,12)

def d20(): 
    return randint(1,20)

def d50(): 
    return randint(1,50)

def d100(): 
    return randint(1,100)

def rd(n):
    return randint(1,n)