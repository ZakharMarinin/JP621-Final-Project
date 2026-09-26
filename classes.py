from constant import COLORS, COLORS_PY, SPEC_COLOR, COLOR_RESET
import random
class card:
    def __init__(self, value, color=None):
        self.value = value
        self.color = color

    def __new__(cls, value, color=None):
        if cls is card and value in ("+2 wild card", "+4 wild card", "color choose", "wild draw color"):
            return super().__new__(wild_card)
        return super().__new__(cls)

    def __eq__(self, other) -> bool:
        if (self.value == other.value) and (self.color == other.color):
            return True
        else:
            return False

    def __str__(self) -> str:
        if self.color in COLORS:
            result = f"{COLORS_PY[COLORS.index(self.color)]}({self.value} {self.color}){COLOR_RESET}"
        else:
            result = f"{SPEC_COLOR}{self.value}{COLOR_RESET}"
        return result

    def eq(self, other) -> bool:
        if (self.value == other.value) or (self.color == other.color) or self.value in ("color choose", "+4 wild card", "+2 wild card", "wild draw color"):
            return True
        else:
            return False

class wild_card(card):
    def __init__(self, value, color=None):
        self.value = value
        self.color = color

    def select_color(self, who, side="light", color=None):
        if who == "player":
            if side == "light":
                colors = COLORS[:4]
            else:
                colors = COLORS[4:]
            print("Доступные цвета:", ", ".join(colors))

            color = input("Выберите цвет: ").lower()

            while color not in colors:
                print("Нет такого цвета")
                color = input("Выберите цвет: ").lower()
            self.color = color
        elif who == "opponent":
            self.color = color

class card_pul:
    def __init__(self, pul: list[card]):
        self.__pul = pul

    def __str__(self) -> str:
        x = []
        for el in self.get_pul():
            x.append(str(el))
        result = ", ".join(x)
        if 2 <= len(self.get_pul())%10 <=4 and len(self.get_pul())//10 != 1:
            result += (f" - {len(self.get_pul())} штуки")
        elif 4 < len(self.get_pul())%10 <= 9 or len(self.get_pul())//10 == 1:
            result += (f" - {len(self.get_pul())} штук")
        elif len(self.get_pul())%10 == 1 and len(self.get_pul()) != 1:
            result += (f" - {len(self.get_pul())} штука")
        return result

    def __isub__(self, minus_pul: list[card]):
        for el in minus_pul:
            self.pop(self.get_pul().index(el))
        return self

    def get_pul(self):
        return self.__pul

    def add(self, col: int, global_pul, show=False):
        plus_pul = []
        for i in range(col):
            if len(global_pul.get_pul()) > 0:
                x = random.randint(0, len(global_pul.get_pul())-1)
                plus_pul.append(global_pul.get_pul()[x])
                global_pul.pop(x)
        self.__pul.extend(plus_pul)
        plus_pul = card_pul(plus_pul)
        if show:
            if len(plus_pul.get_pul()) == 1:
                print("Добавленная карта:", plus_pul)
            else:
                print("Добавленные карты:", plus_pul)
        return plus_pul

    def extra_add(self, color, global_pul, show=False):
        plus_pul = []
        x = random.randint(0, len(global_pul.get_pul())-1)
        card = global_pul.get_pul()[x]
        while card.color not in (color, None) and len(global_pul.get_pul()) != 0:
            plus_pul.append(card)
            global_pul.pop(x)
            x = random.randint(0, len(global_pul.get_pul())-1)
            card = global_pul.get_pul()[x]
        plus_pul.append(card)
        global_pul.pop(x)
        self.get_pul().extend(plus_pul)
        plus_pul = card_pul(plus_pul)
        if show:
            if len(plus_pul.get_pul()) == 1:
                print("Добавленная карта:", plus_pul)
            elif len(plus_pul.get_pul()) != 0:
                print("Добавленные карты:", plus_pul)
            if plus_pul.get_pul()[-1].color not in (color, None) and len(global_pul.get_pul()) == 0:
                print("Невозможно добавить больше карт, т.к. колода закончилась.")
        return len(plus_pul.get_pul())        

    def pop(self, x):
        self.__pul.pop(x)

    def types(self) -> list[str]:
        pul = []
        for el in self.get_pul():
            pul.append(el.value)
        return pul