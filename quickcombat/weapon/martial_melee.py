from .general import Melee

def battleaxe(name='战斧'): 
    m = Melee(hurt_dice=8, dice_times=1, range_max=5, name=name)
    return m