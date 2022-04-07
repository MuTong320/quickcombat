from ..attack import Attack

class Spell(Attack): 
    def __init__(self, hurt_dice, dice_times=1, range_max=5):
        super().__init__(hurt_dice, dice_times, range_max)