from ..card import CharacterCard
from ..dice import *
from ..weapon import *

def commoner(name='平民', random=True, weapon=True): 
    if random: 
        HP = d8()
    else: 
        HP = 4
    c = CharacterCard(name=name, HP=HP)
    if weapon: 
        c.set_weapon(simple_melee.club()) #默认武器：短棍
    return c