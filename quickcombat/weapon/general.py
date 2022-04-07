from ..dice import *
from ..attack import Attack

class Hands(Attack): 
    def __init__(self): 
        super().__init__(hurt_dice=1, dice_times=1, range_max=5)
        self.name = '赤手空拳'

    def __repr__(self): 
        return f"Unarmed strike (hurt=d{self.hurt}). "


class Melee(Attack): 
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


class Ranged(Attack): 
    def __init__(self, hurt_dice, dice_times=1, range_full=20, range_max=60, name='unknown'): 
        super().__init__(hurt_dice, dice_times, range_max)
        self.name = name
        self.range_full = range_full

    def __repr__(self): 
        return f"Melee object '{self.name}'(hurt={self.times}d{self.hurt}, range={self.range_max}). "