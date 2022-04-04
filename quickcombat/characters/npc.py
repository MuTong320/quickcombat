from ..card import CharacterCard
from ..dice import *

def commoner(random=True): 
    HP = 4
    if random: HP = d8()
    c = CharacterCard(HP=HP)
    return c