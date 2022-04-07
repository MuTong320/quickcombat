from os import kill
from .weapon.general import Attack, Hands
from .dice import *

class CharacterCard:
    def __init__(self, name='Someone', HP=4, AC=10, init_add=0, hit_add=0, hurt_add=0, HPmax=None):
        self.name  = name
        self.ac    = AC
        self.hp    = HP
        self.hpmax = HP
        if HPmax: self.hpmax = HPmax 
        self.__init_add = init_add
        self.__hit_add  = hit_add
        self.__hurt_add = hurt_add
        self.active = True
        self.state = '正常'
        self.attitude = '中立'
        self.__init_arsenal()
        self.combat_number = 0
        self.history = []

    def __repr__(self): 
        repr  = f"CharacterCard object '{self.name}' ({self.hp}/{self.hpmax})"
        return repr

    def story(self): 
        for event in self.history: 
            if event['type'] == 'combat': 
                print(f"发生在{event['room']}战斗的详情：")
                for act_dict in event['round'].values(): 
                    s = '    ' + self.natural_format(act_dict)
                    print(s)
        """
        act_dict = {
            'active': bool, 
            'state': str, 
            'weapon': str, 
            'aim': str, 
            'r1': bool, 
            'r20': bool, 
            'hit': bool, 
            'hurt': int, 
            'kill': bool, 
            'hp': int, 
            'hpmax': int, 
            'aim_hp': int, 
            'aim_hpmax': int
        }
        """

    def natural_format(self, act_dict, hp=False): 
        s = str(self.name)
        if act_dict['active']: 
            s += f"用{act_dict['weapon']}攻击{act_dict['aim']}"
            if hp: s += f"(HP {act_dict['hp']}/{act_dict['hpmax']})"
            if act_dict['r1']: 
                s += f"大失败，对自身造成{act_dict['hurt']}伤害"
                if kill: 
                    s += '，因此死亡。'
                else: 
                    s += '。'
            elif act_dict['r20']: 
                s += f"大成功，伤害翻倍为{act_dict['hurt']}，"
                if act_dict['kill']: 
                    s += f"并杀死了{act_dict['aim']}"
                else: 
                    s += f"但{act_dict['aim']}仍然存活。"
            else: 
                if act_dict['hit']: 
                    s += f"成功，伤害为{act_dict['hurt']}，"
                    if act_dict['kill']: 
                        s += f"并杀死了{act_dict['aim']}"
                    else: 
                        s += f"但{act_dict['aim']}仍然存活。"
                    if hp: s += f"(HP {act_dict['aim_hp']}/{act_dict['aim_hpmax']})"
                else: 
                    s += "，但失败了。"
        else: 
            s += f"因{act_dict['state']}跳过回合。"
        return s

    def activate(self): 
        self.active = True

    def deactivate(self, death=False, coma=False, fetter=False): 
        self.active = False
        if death : self.state = '死亡'
        if coma  : self.state = '昏迷'
        if fetter: self.state = '束缚'

    def __init_arsenal(self): 
        hands = Hands()
        self.arsenal = [hands, ]
        self.__weapon = hands

    def set_weapon(self, weapon): 
        if type(weapon) == str: 
            weapon = self.__get_weapon(weapon)
        if isinstance(weapon, Attack): 
            if weapon not in self.arsenal: self.add_weapon(weapon, use=True)
        else: 
            print("Setting failed.")

    def get_weapon(self): 
        return self.__weapon

    def __get_weapon(self, name): 
        for w in self.arsenal: 
            if w.name == name: return w

    def add_weapon(self, *weapon, use=False): 
        self.arsenal += list(weapon)
        if use: 
            if len(weapon) == 1: 
                self.__weapon = weapon[0]
            else: 
                print("Set only one weapon if use.")

    def remove_weapon(self, *weapon): 
        for w in weapon: 
            if type(w) == str: w = self.__get_weapon(weapon)
            if isinstance(w, Attack): 
                if w in self.arsenal: self.arsenal.remove(w)

    def get_init(self, dice_value=None): 
        if not dice_value: dice_value = d20()
        return dice_value + self.__init_add

    def get_hit(self, dice_value=None): 
        if not dice_value: dice_value = d20()
        return dice_value + self.__hit_add

    def get_hurt(self, weapon=None): 
        if not weapon: 
            w = self.__weapon
        else: 
            if type(weapon) == str: 
                w = self.__get_weapon(weapon)
            if isinstance(weapon, Attack): 
                w = weapon
        return w() + self.__hurt_add



