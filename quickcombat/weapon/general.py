from ..dice import *

class Weapon: 
    def __init__(self, hurt_dice, dice_times=1, range_max=5): 
        self.hurt = hurt_dice
        self.times = dice_times
        self.range_max = range_max
    
    def __call__(self) -> int: 
        return sum([rd(self.hurt) for _ in range(self.times)])


class Hands(Weapon): 
    def __init__(self): 
        super().__init__(hurt_dice=1, dice_times=1, range_max=5)
        self.name = '赤手空拳'
    
    def __repr__(self): 
        return f"Unarmed strike (hurt=d{self.hurt}). "


class Melee(Weapon): 
    def __init__(self, hurt_dice, dice_times=1, range_max=5, name='unknown'): 
        super().__init__(hurt_dice, dice_times, range_max)
        self.name = name
    
    def __repr__(self):
        return f"Melee object '{self.name}'(hurt={self.times}d{self.hurt}, range={self.range_max}). "


class ThrowMelee(Melee): 
    def __init__(self, hurt_dice, dice_times=1, range_full=20, range_max=60, name='unknown'): 
        super().__init__(hurt_dice, dice_times, range_max)
        self.name = name
        self.range_full = range_full


class Ranged(Weapon): 
    def __init__(self, hurt_dice, dice_times=1, range_full=20, range_max=60, name='unknown'): 
        super().__init__(hurt_dice, dice_times, range_max)
        self.name = name
        self.range_full = range_full
    
    def __repr__(self): 
        return f"Melee object '{self.name}'(hurt={self.times}d{self.hurt}, range={self.range_max}). "