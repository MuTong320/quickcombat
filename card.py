class CharacterCard:
    def __init__(
        self, name='Someone',
        HP=4, AC=10, 
        STR=10, DEX=10, CON=10, 
        INT=10, WIS=10, CHA=10, 
        speed=30
    ):
        self.name  = name
        self.hp    = HP
        self.hpmax = HP
        self.ac    = AC
        self.str   = STR
        self.dex   = DEX
        self.con   = CON
        self.int   = INT
        self.wis   = WIS
        self.cha   = CHA
        self.speed = speed
    
    def prop_lists(self): 
        self.prop  = [self.str, self.dex, self.con, self.int, self.wis, self.cha]
        self.modfy = [n//2-5 for n in self.prop]
        self.remit = []
    
    def __repr__(self): 
        repr  = f"CharacterCard object '{self.name}' ({self.hp}/{self.hpmax})"
        return repr

class Enemy(CharacterCard): 
    def __init__(self, name='Someone', HP=4, AC=10, 
        STR=10, DEX=10, CON=10, INT=10, WIS=10, CHA=10, 
        speed=30, 
        hit_add=2, hurt_rand=4, hurt_add=0,
        HPmax=None, init_add=None, remark=None):
        super().__init__(name, HP, AC, STR, DEX, CON, INT, WIS, CHA, speed)
        self.hit_add   = hit_add
        self.hurt_rand = hurt_rand
        self.hurt_add  = hurt_add
        self.init_add  = 0
        self.remark    = ''
        if HPmax:    self.hpmax    = HPmax
        if init_add: self.init_add = init_add
        if remark:   self.remark   = remark
    
    def __repr__(self): 
        repr  = f"CharacterCard object '{self.name}' ({self.hp}/{self.hpmax})"
        repr += self.remark
        return repr