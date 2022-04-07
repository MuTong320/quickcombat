import random
import time

from .card import CharacterCard
from .dice import *
from .room import Room, Team


class Game(Team): 
    def __init__(self, *player_cards, file=None): 
        super().__init__(*player_cards)
        self.__init_file(file)
        self.__set_world()

    def __init_file(self, file):
        if file: 
            self.file = file
            f = open(self.file,'w')
        else: 
            self.file = 'history.txt'
            f = open(self.file,'a')
        f.write("****************************************\n")
        f.write("*               New Game               *\n")
        f.write("****************************************\n")
        f.write(time.asctime())
        f.write('\n')
        f.close()

    def __repr__(self): 
        s = '团队成员：\n'
        for c in self.cards: 
            s += f"    {c.name} (HP = {c.hp}/{c.hpmax})"
            if not c.active: s += '（失能）'
            s += '\n'
        all_room = [r.name for r in self.rooms]
        s += f"已探明房间：{all_room}\n"
        if self.combating: s += '（战斗中）'
        s += f"小队现在位于{self.__current.room_info()}\n"
        return s

    def __set_world(self): 
        self.world     = Room(name='World')
        self.rooms     = [self.world, ]
        self.__current = self.world
        self.combating = False

    def goto_room(self, room):
        if type(room) == str: room = self.get_room(room)
        if type(room) == Room: self.__current = room

    def get_room(self, name=None): 
        if not name: 
            return self.__current
        else: 
            for c in self.rooms: 
                if c.name == name: return c

    def add_room_obj(self, *r): 
        self.rooms += list(r)

    def add_room(self, *enemies, copy_times=1, name=None, arrive=False): 
        if not name: name = self.__new_room_name()
        if copy_times > 1: enemies = list(enemies)*copy_times
        self.world.add_card(*enemies)
        enemies = self.world.cards[-len(enemies):]
        r = Room(*enemies, name=name)
        self.rooms.append(r)
        if arrive: self.goto_room(r)

    def __new_room_name(self): 
        all_names = [r.name for r in self.rooms]
        for i in range(len(self.rooms)):
            name = f'room({i+1})'
            if name not in all_names: break
        return name

    def remove_room(self, *to_remove_names): 
        for r in self.rooms: 
            if r.name in to_remove_names: self.rooms.remove(r)

    def combat(self, room=None, round=0): 
        if room: self.goto_room(room)
        self.__init_dict = {}
        all_card = self.cards + self.__current.cards
        self.__auto_init(*all_card)
        self.combating = True
        pl_time = time.asctime()
        with open(self.file,'a') as f: 
            f.write("----------   New Combat   ----------\n")
            f.write(pl_time)
            f.write('\n')
            f.write(f"Happened in {self.__current.name}: \n")
            f.write("Initiative list: \n")
            f.write(self.__get_init_repr())
            f.close()
        self.__round = 0
        for c in all_card: 
            c.combat_number += 1
            c.history.append({
                'type': 'combat', 
                'time': pl_time, 
                'room': self.__current.name, 
                'round': {}
            })
        while self.combating: 
            self.auto_round()
            if self.__round == round: break

    def __auto_init(self, *characters, report=True): 
        for c in characters: 
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: 
                init = c.get_init()
                self.__init_dict[c] = init
                if report: print(f"{c.name}的先攻是{init}.")
        self.__sort_init()
        if report: 
            print('先攻列表：')
            print(self.__get_init_repr())

    def __sort_init(self): 
        lst = list(self.__init_dict.keys())
        num = list(set(self.__init_dict.values()))
        num.sort()
        sorted = []
        for i in num: 
            for c in lst: 
                if self.__init_dict[c] == i: sorted.append(c)
        sorted.reverse()
        self.__init_list = sorted

    def __get_init_repr(self): 
        s = ''
        for i,c in enumerate(self.__init_list): 
            s += f"    {i+1}. "
            s += "%-10s" % c.name
            s += f" (initiative={self.__init_dict[c]}) \n"
        return s

    def manual_init(self, **character_value): 
        for c, init in character_value.items(): 
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: 
                self.__init_dict[c] = init
        self.__sort_init()

    def auto_round(self): 
        self.__round += 1
        print(f"第{self.__round}轮战斗：")
        with open(self.file,'a') as f: 
            f.write(f"{self.__round}th round: \n")
            f.close()
        for c in self.__init_list: 
            if c.active: 
                act_dict = self.__round_action(c)
            else: 
                act_dict = self.__skip_round(c)
            c.history[-1]['round'][self.__round] = act_dict
            screen = '    ' + c.natural_format(act_dict)
            print(screen)
            with open(self.file,'a') as f: 
                line = '    ' + c.natural_format(act_dict, hp=True) + '\n'
                f.write(line)
                f.close()
            if self.__check_break_combat(): break

    def __check_break_combat(self):
        if all([not c.active for c in self.__current.cards]): 
            self.cease_fire(reason='success')
            return True
        elif all([not c.active for c in self.cards]): 
            self.cease_fire(reason='failure')
            return True
        else: 
            return False

    def __round_action(self, c, strategy='random'): 
        if strategy == 'random': aim = self.__rand_aim(c)
        act_dict = {
            'active': True, 
            'weapon': str(c.get_weapon().name), 
            'state': c.state, 
            'hp': c.hp, 
            'hpmax': c.hpmax, 
            'aim': str(aim.name), 
            'aim_hp': aim.hp, 
            'aim_hpmax': aim.hpmax
        }
        hit_dice = d20()
        if hit_dice == 1: 
            act_dict['r1']  = True
            act_dict['r20'] = False
            hit, hurt, kill = self.__great_failure(c)
        elif hit_dice == 20: 
            act_dict['r1']  = False
            act_dict['r20'] = True
            hit, hurt, kill = self.__great_success(c, aim)
        else: 
            act_dict['r1']  = False
            act_dict['r20'] = False
            hit, hurt, kill = self.__normal_attack(c, aim, hit_dice)
        act_dict['hit']  = hit
        act_dict['hurt'] = hurt
        act_dict['kill'] = kill
        return act_dict

    def __rand_aim(self, c):
        if c in self.cards: 
            alives = list(filter(lambda c: c.active, self.__current.cards))
            return random.sample(alives, 1)[0]
        elif c in self.__current.cards: 
            alives = list(filter(lambda c: c.active, self.cards))
            return random.sample(alives, 1)[0]

    def __great_failure(self, c):
        hit = False
        hurt = d4()
        c.hp -= hurt
        kill = self.__check_kill(c)
        return hit, hurt, kill

    def __great_success(self, c, aim): 
        hit = True
        hurt = 2*c.get_hurt()
        aim.hp -= hurt
        kill = self.__check_kill(aim)
        return hit, hurt, kill

    def __normal_attack(self, c, aim, dice_value):
        hit_value = c.get_hit(dice_value)
        if hit_value > aim.ac: 
            hit = True
            hurt = c.get_hurt()
            aim.hp -= hurt
            kill = self.__check_kill(aim)
        else: 
            hit = False
            hurt = 0
            kill = False
        return hit, hurt, kill

    def __check_kill(self, aim): 
        if aim.hp > 0: 
            kill = False
        elif aim.hp <= 0: 
            kill = True
            self.__set_deactive_state(aim)
        return kill

    def __set_deactive_state(self, aim):
        if aim in self.cards: 
            if aim.hp < -aim.hpmax: 
                aim.deactivate(death=True)
            else: 
                aim.deactivate(coma=True)
        elif aim in self.__current.cards: 
            aim.deactivate(death=True)

    def __skip_round(self, c):
        return {
            'active': False, 
            'state': c.state, 
            'hp': c.hp, 
            'hpmax': c.hpmax
        }

    def cease_fire(self, reason=None): 
        self.combating = False
        if reason == 'success': 
            print('所有敌人已被消灭。')
        elif reason == 'failure': 
            print('全员失去战斗力，失败。')
        else: 
            print('战斗结束。')
        print("团队成员情况：")
        s = self.team_info()
        print(s)
        with open(self.file, 'a') as f: 
            f.write(f"Combat is over. \n")
            f.write(s)
            f.close()

    def team_info(self):
        s = ''
        for c in self.cards: 
            s += "    %-10s" % c.name + f"HP={c.hp}/{c.hpmax}\n"
        return s



