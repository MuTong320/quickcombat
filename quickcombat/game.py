import random
import time

from .card import CharacterCard
from .dice import *
from .room import Room, Team


class Game(Team): 
    def __init__(self, *player_cards, file=None): 
        super().__init__(*player_cards)
        self.__first_room()
        self.combating = False
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
        repr = '团队成员：\n'
        for c in self.cards: 
            repr += f"    {c.name} (HP = {c.hp}/{c.hpmax})"
            if not c.active: repr += '（失能）'
            repr += '\n'
        all_room = [r.name for r in self.rooms]
        repr += f"已探明房间：{all_room}\n"
        if self.combating: repr += '（战斗中）'
        repr += f"小队现在位于{self.__current.room_info()}\n"
        return repr

    def __first_room(self): 
        origin       = Room(name='origin')
        self.rooms   = [origin, ]
        self.__current =  origin
    
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
        self.auto_init(*all_card)
        self.combating = True
        with open(self.file,'a') as f: 
            f.write("----------   New Combat   ----------\n")
            f.write(time.asctime())
            f.write('\n')
            f.write(f"Happened in {self.__current.name}: \n")
            f.write("Initiative list: \n")
            f.write(self.get_init_repr())
            f.close()
        self.__round = 0
        while self.combating: 
            self.auto_round()
            if self.__round == round: break

    def auto_init(self, *characters, report=True): 
        for c in characters: 
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: 
                init = d20() + c.hit_add
                self.__init_dict[c] = init
                if report: print(f"{c.name}的先攻是{init}.")
        self.__sort_init()
        if report: 
            print('先攻列表：')
            print(self.get_init_repr())

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

    def get_init_repr(self): 
        repr = ''
        for i,c in enumerate(self.__init_list): 
            repr += f"    {i+1}. "
            repr += "%-10s" % c.name
            repr += f" (d20+{c.init_add}={self.__init_dict[c]}) \n"
        return repr
    
    def manual_init(self, **character_value): 
        for c, init in character_value.items(): 
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: 
                self.__init_dict[c] = init
        self.__sort_init()
    
    def auto_round(self): 
        self.__round += 1
        s = f"第{self.__round}轮战斗："
        f = open(self.file,'a')
        f.write(s)
        f.write('\n')
        f.close()
        print(s)
        for c in self.__init_list: 
            if c.active: 
                aim = self.__rand_aim(c)
                self.__round_action(c, aim)
            else: 
                self.__round_skip(c)
            if all([not c.active for c in self.__current.cards]): 
                print('所有敌人已被消灭。')
                f = open(self.file,'a')
                f.write('Combat is over. \n')
                f.close()
                self.cease_fire()
                break
            if all([not c.active for c in self.cards]): 
                print('全员失去战斗力，失败。')
                f = open(self.file,'a')
                f.write('Combat FAIL. \n')
                f.close()
                self.cease_fire()
                break

    def __rand_aim(self, c):
        if c in self.cards: 
            alives = list(filter(lambda c: c.active, self.__current.cards))
            return random.sample(alives, 1)[0]
        elif c in self.__current.cards: 
            alives = list(filter(lambda c: c.active, self.cards))
            return random.sample(alives, 1)[0]

    def __round_action(self, c, aim): 
        f = open(self.file,'a')
        repr = f"    {c.name}攻击{aim.name}"
        f.write(f"    {c.name}(HP={c.hp}/{c.hpmax}): ")
        hit = d20() 
        if hit == 1: 
            hurt = random.randint(1, c.hurt_rand) + c.hurt_add
            c.hp -= hurt
            repr += f"（大失败，对自身造成{hurt}伤害）"
            f.write(f"Great Failure, {hurt} hurt to self. \n")
        else: 
            if hit == 20: 
                multiplier = 2
                repr += "（大成功）"
                f.write(f"Great Success, ")
                great_success = True
            else: 
                multiplier = 1
                great_success = False
            hit += c.hit_add
            f.write(f"hit={hit}, ")
            if hit > aim.ac or great_success: 
                hurt = random.randint(1, c.hurt_rand) + c.hurt_add
                hurt *= multiplier
                repr += f"成功，伤害为{hurt}，"
                aim.hp -= hurt
                if aim.hp > 0: 
                    repr += f"但{aim.name}仍然存活。"
                elif aim.hp <= 0: 
                    repr += f"并击杀{aim.name}。"
                    aim.deactivate()
                f.write(f"hurt={hurt}, aim={aim.name}(HP={aim.hp}/{aim.hpmax}) \n")
            else: 
                repr += '，但失败了。'
                f.write(f"failed, aim={aim.name}(HP={aim.hp}/{aim.hpmax}) \n")
        print(repr)
        f.close()

    def __round_skip(self, c):
        print(f"    跳过{c.name}")
        f = open(self.file,'a')
        f.write(f"    {c.name}(HP={c.hp}/{c.hpmax}): skiped \n")
        f.close()

    def cease_fire(self): 
        self.combating = False
        self.team_info()

    def team_info(self):
        print("团队成员情况：")
        f = open(self.file,'a')
        for c in self.cards: 
            s = "    %-10s" % c.name + f"HP={c.hp}/{c.hpmax}"
            print(s)
            f.write(f"    {c.name}(HP={c.hp}/{c.hpmax})\n")
        f.close()



