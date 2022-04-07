import copy

from .card import CharacterCard


class RoomBase:
    def __init__(self, *cards): 
        self.cards   = []
        self.add_card(*cards)

    def add_card(self, *cards, wake=True): 
        if cards: 
            self.cards += cards
            if wake: self.wakeup(*cards)

    def remove_card(self, *characters): 
        for c in characters:
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: self.cards.remove(c)

    def get_card(self, name=None): 
        if not name: 
            return tuple(self.cards)
        else: 
            for c in self.cards: 
                if c.name == name: return c

    def wakeup(self, *characters): 
        if not characters: characters = self.cards
        for c in characters:
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: c.activate()

    def sleep(self, *characters): 
        if not characters: characters = self.cards
        for c in characters:
            if type(c) == str: c = self.get_card(c)
            if type(c) == CharacterCard: c.deactivate()


class Team(RoomBase): 
    def __init__(self, *cards):
        super().__init__(*cards)


class Room(RoomBase): 
    def __init__(self, *enemies, name='unnamed room'):
        super().__init__(*enemies)
        self.name  = name

    def __repr__(self): 
        repr = "Room object, "
        repr += self.room_info()
        return repr

    def room_info(self): 
        repr = f"房间{self.name}\n共{len(self.cards)}个敌人：\n"
        if self.cards: 
            for c in self.cards: 
                repr += "    %-10s" % c.name
                if c.active: repr += '（已敌对）'
                repr += f"(HP = {c.hp}/{c.hpmax})"
                repr += '\n'
        return repr

    def add_card(self, *cards, active=True): 
        if cards: 
            for c in cards: 
                if c in self.cards: c = copy.deepcopy(c)
                self.__check_name(c)
                self.cards.append(c)
            if active: self.wakeup(*cards)

    def __check_name(self, c): 
        all_names = [c.name for c in self.cards]
        if c.name not in all_names: 
            return c
        else: 
            num = len(all_names)
            old_name = c.name
            for i in range(num):
                new_name = f'{old_name}({i+2})'
                if new_name not in all_names: 
                    break
            c.name = new_name


