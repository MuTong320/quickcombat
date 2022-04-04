class CharacterCard:
    def __init__(self, name='Someone', HP=4, AC=10, init_add=0, hit_add=2, hurt_rand=4, hurt_add=0, HPmax=None):
        self.name      = name
        self.hp        = HP
        self.ac        = AC
        self.init_add  = init_add
        self.hit_add   = hit_add
        self.hurt_rand = hurt_rand
        self.hurt_add  = hurt_add
        self.hpmax     = HP
        self.active    = True
        if HPmax: self.hpmax = HPmax
    
    def __repr__(self): 
        repr  = f"CharacterCard object '{self.name}' ({self.hp}/{self.hpmax})"
        return repr
    
    def activate(self): 
        self.active = True

    def deactivate(self): 
        self.active = False


