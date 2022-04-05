from ..card import CharacterCard
from ..dice import *
from ..weapon import *


def kobold(name='狗头人', random=True, weapon=True): 
    if random: 
        HP = d6() + d6() - 2
    else: 
        HP = 5
    c = CharacterCard(name=name, HP=HP, AC=12, init_add=2, hit_add=4, hurt_add=2)
    if weapon: 
        c.set_weapon(simple_melee.dagger()) #默认武器：匕首
        c.add_weapon(simple_ranged.sling()) #远程武器：投石索
    return c

def goblin(name='地精', random=True, weapon=True): 
    if random: 
        HP = d6() + d6()
    else: 
        HP = 5
    c = CharacterCard(name=name, HP=HP, AC=15, init_add=2, hit_add=4, hurt_add=2)
    if weapon: 
        c.set_weapon(simple_melee.scimitar()) #默认武器：弯刀
        c.add_weapon(simple_ranged.shortbow()) #远程武器：短弓
    return c