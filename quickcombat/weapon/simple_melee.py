from .general import Melee, ThrowMelee

def club(name='短棍'): 
    m = Melee(hurt_dice=4, name=name)
    return m

def dagger(name='匕首'): 
    m = ThrowMelee(hurt_dice=4, name=name)
    return m

def scimitar(name='弯刀'): 
    m = Melee(hurt_dice=6, name=name)
    return m