from ..card import CharacterCard
from ..dice import *

def commoner(random=True): 
    if random: 
        HP = d8()
    else: 
        HP = 4
    c = CharacterCard(HP=HP)
    return c