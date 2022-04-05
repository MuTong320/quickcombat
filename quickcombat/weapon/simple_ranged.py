from .general import Ranged

def sling(name='投石索'): 
    m = Ranged(4, dice_times=1, range_full=30, range_max=120, name=name)
    return m

def shortbow(name='短弓'): 
    m = Ranged(6, dice_times=1, range_full=80, range_max=320, name=name)
    return m