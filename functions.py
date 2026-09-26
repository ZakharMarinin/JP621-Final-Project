from constant import COLORS, DIFICULTS
from classes import card, card_pul
def mi_bombo(x):
    if x == "mi bombo":
        print("Say my name")
        if input() == "Heisenberg":
            print("You god damn right")
        else:
            print("You god damn fat")
        return True
    else:
        return False

def card_check(user_input: int | str, pul: list[card]):
    good_attempt = False
    while not good_attempt:
        try:
            if user_input not in ["+", "stop"]:
                if len(user_input.split()) >= 2:
                    if user_input not in ["+4 wild card", "color choose", "+2 wild card", "wild draw color"]:
                        attempted_card = card(user_input.split()[0], user_input.split()[1])
                        user_input = pul.index(attempted_card)+1
                    else:
                        user_input = pul.index(card(user_input, None))+1
                else:
                    pul[int(user_input)-1]
        except IndexError:
            print("Введённое число больше номера последней карты")
            user_input = str.lower(input("Пожалуйста повторите ввод: "))
        except ValueError:
            if mi_bombo(input):
                user_input=str.lower(input("Выберите карту: "))
            else:
                print("Некорректный ввод")
                user_input=str.lower(input("Пожалуйста повторите ввод: "))
        else:
            if user_input == "+" and (len(card_pul(pul).types()) == card_pul(pul).types().count("+2") or len(pul) == pul.count(card("+4 wild card"))):
                print("Вы должны отбить карту противника")
                user_input=str.lower(input("Выберите карту: "))
            elif user_input != "mi bombo":
                good_attempt=True
                return(user_input)
            elif user_input == "mi bombo":
                user_input = str.lower(input("Выберите карту: "))

def other_check(x: str) -> int:
    good_attempt=False
    if x == "difficult":        # Сложность
        while good_attempt != True:
            try:
                x=input("Введите цифру: ")
                x=int(x)
                DIFICULTS[x-1]
            except IndexError:
                print(f"Пожалуйста выберите цифру от 1 до 2")
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)
    elif x == "SizeOfStartPul":     # Стартовое кол-во карт
        while good_attempt != True:
            try:
                x=input("Выберите стартовое количество карт: ")
                x=int(x)
                while x<5 or x>50:
                    print("Стартовое количество карт должно быть в промежутке от 5 до 15")
                    x=input("Выберите стартовое количество карт: ")
                    x=int(x)
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)
    elif x == "gamemode":       # Режим
        while not good_attempt :
            try:
                x=input("Выберите режим игры: ")
                x=int(x)
                while x<1 or x>2:
                    print("Пожалуйста введите число от 1 до 2")
                    x=int(input())
            except ValueError:
                if mi_bombo(x):
                    pass
                else:
                    print("Некорректный ввод")
            else:
                good_attempt=True
                return(x)

def check_correct(your_choose, last_card, pul):
    if your_choose not in ["+", "stop"]:
        your_card = pul[int(your_choose)-1]
        while not (your_card.eq(last_card) or your_choose in ["+", "stop"]):
            print("Карта не подходит. пожалуйста выберите другую или возьмите новую")
            your_choose = input()
            your_choose = card_check(your_choose, pul)
            if your_choose not in ["+", "stop"]:
                your_card = pul[int(your_choose)-1]
    return(your_choose)

def make_card_pul(raw_pul: list[tuple[str] | str]) -> list[card]:
    result = []
    for el in raw_pul:
        if type(el) == tuple:
            result.append(card(el[0], el[1]))
        else:
            result.append(card(el))
    return card_pul(result)

def active_pul(light_pul, dark_pul, side):
    if side == "light":
        return light_pul
    return dark_pul

def choose_color(side):
    if side == "light":
        colors = COLORS[:4]
    else:
        colors = COLORS[4:]
    print("Доступные цвета:", ", ".join(colors))

    color = input("Выберите цвет: ").lower()

    while color not in colors:
        print("Нет такого цвета")
        color = input("Выберите цвет: ").lower()
    return color