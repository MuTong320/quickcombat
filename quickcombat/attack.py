from .dice import *

class Attack: 
    def __init__(self, hurt_dice, dice_times=1, range_max=5): 
        self.hurt = hurt_dice
        self.times = dice_times
        self.range_max = range_max
    
    def __call__(self) -> int: 
        return sum([rd(self.hurt) for _ in range(self.times)])