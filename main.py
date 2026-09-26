import random
from datetime import datetime
from random import randint
from constant import RAW_CLASSIC_CARDS, GAMEMODES, DIFICULTS, COLORS, session_stats, RAW_LIGHT_FLIP_CARDS, RAW_DARK_FLIP_CARDS
from classes import card, card_pul, wild_card
from functions import *
import json

with open("stats.json", "r+") as file:
    data = json.load(file)

    if data["name"] is None:
        name = input("Привет, пожалуйста введи своё имя: ")
        data["name"] = name

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    player_name = data["name"]
    last_parameter = data["last_parameter"]
    if last_parameter is not None:
        gamemode = last_parameter["gamemode"]
        difficult = last_parameter["difficult"]
        SizeOfStartPul = last_parameter["SOSP"]

running = True
MENU_CHOOSE = ["play", "fast_restart", "rules", "n_stats", "global_stats", "quit"]
print(f"{player_name}, приветствуем тебя в терминальной игре UNO!")

while running:
    print("")
    print("Навигация:")
    print("1. Начать игру \n2. Быстрый перезапуск партии с последними используемыми параметрами \n3. Правила \n4. Статистика последних n партий \n5. Общая статистика \n6. Выход")
    menu_choose = input("Выберите действие: ")
    while menu_choose not in "123456" or menu_choose == "":
        print("Некорректный ввод")
        menu_choose = input("Выберите действие: ")
    menu_choose = MENU_CHOOSE[int(menu_choose) - 1]

    if menu_choose == "fast_restart" and last_parameter is None:
        print("")
        print("Быстрый перезапуск невозможен, т.к. вы ещё не сыграли ни одной игры")

    elif menu_choose in ("play", "fast_restart"):      # Игра
        if menu_choose != "fast_restart":
            print("")
            print("Режимы:")
            print("1. UNO Classic - классическое уно")
            print("2. UNO Flip - двухсторонняя колода с особыми картами действия")
            gamemode = GAMEMODES[other_check("gamemode")-1]
        if gamemode=="classic":    # UNO Classic
            if menu_choose != "fast_restart":
                print("")
                print("Выберите уровень сложности:")
                print("1. Лёгкий - отбивать карты +2 и +4 невозможно")
                print("2. Нормальный - все стандартные правила игры")
                difficult = DIFICULTS[other_check("difficult")-1]
            cards = make_card_pul(RAW_CLASSIC_CARDS)
            player_pul = card_pul([])
            opponent_pul = card_pul([])
            if menu_choose != "fast_restart":
                SizeOfStartPul = other_check("SizeOfStartPul")
            player_pul.add(SizeOfStartPul, cards)
            opponent_pul.add(SizeOfStartPul, cards)
            stopgame = False
            choose = 0
            player_try = False
            opponent_try = False
            buff_sum = 0
            player_block = False
            opponent_block = False
            card_is_over = False
            pul_is_changed = False
            start_card = cards.get_pul()[randint(0,len(cards.get_pul()[:-28])-1)]
            cards -= [start_card]
            last_card = start_card
            opponent_card = start_card
            player_card = card(None)
            print("")
            print("Начальная карта:", start_card)
            start_time = datetime.now()
            while not stopgame and len(player_pul.get_pul()) != 0 and len(opponent_pul.get_pul()) !=0 and not card_is_over:
                opponent_block=False
                your_choose = ""
                if opponent_card.value in ("+2", "+4 wild card") and not (opponent_card.value in player_pul.types()) and buff_sum != 0 and difficult=="normal":
                    print("Вы не можете отбить карту противника")
                    player_pul.add(buff_sum, cards, True)
                    buff_sum=0
                elif opponent_card.value in ("+2", "+4 wild card") and buff_sum !=0:
                    print("Будете ли вы отбивать карту противника?")
                    deef=input("y (yes) / n (no): ")
                    while deef != "y" and deef != "n":
                        print("Некорректный ввод")
                        deef=input("Пожалуйста повторите ввод: ")
                    if deef == "y":
                        changed_pul = []
                        for el in player_pul.get_pul():
                            if (opponent_card.value == "+2" and el.value == "+2") or (opponent_card.value == "+4 wild card" and el == "+4 wild card"):
                                changed_pul.append(el)
                        changed_pul = card_pul(changed_pul)
                        changed_pul, player_pul = player_pul, changed_pul
                        pul_is_changed=True
                    else:
                        print("Вы отказались отбивать карту противника.")
                        player_pul.add(buff_sum, cards, True)
                        buff_sum=0
                if player_try and opponent_try and len(cards.get_pul()) == 0:     # Если колода закончилась
                    card_is_over=True
                if opponent_card.value in ("block", "reverse") and not opponent_try:        # Если блок
                    opponent_block = True
                if not (opponent_block or card_is_over):
                    print(f"Ваш набор карт:\n{player_pul}")
                    print('Выберите карту для хода. Если подходящей карты нет введите "+"')
                    player_choose=str.lower(input())
                    player_choose = check_correct(card_check(player_choose, player_pul.get_pul()), last_card, player_pul.get_pul())
                if not (player_choose in ("+", "stop") or opponent_block or card_is_over):  # Если сходил
                    player_card = player_pul.get_pul()[int(player_choose)-1]
                    if type(player_card) is wild_card:
                        player_card.select_color("player", "light")
                    if player_card.value in ("+2", "+4 wild card"):
                        if difficult == "easy":
                            opponent_pul.add(int(player_card.value[1]), cards)
                        else:
                            buff_sum += int(int(player_card.value[1]))

                    player_pul.pop(int(player_choose)-1)
                    last_card = player_card
                    player_try = False
                    if player_card.value not in ("+2", "color choose", "+4 wild card") and player_card in player_pul.get_pul():
                        card_sum = 1
                        while player_card in player_pul.get_pul():
                            player_pul -= [player_card]
                            card_sum += 1
                        print(f"Ваш ход: {player_card} x{card_sum}")
                    else:
                        print("Ваш ход:", player_card)
                elif player_choose == "+":        # Если взял карту
                    player_try = True
                    player_pul.add(1, cards, True)
                elif player_choose == "stop":     # Если завершил игру
                    stopgame = True
                if not (((opponent_card.value in ("block", "reverse")) and not opponent_try) or ((player_card.value in ("block", "reverse")) and not player_try)):
                    print("")
                if pul_is_changed:
                    changed_pul -= [player_card]
                    player_pul = changed_pul
                    pul_is_changed = False

                # Ход противника

                choose=0
                card_is_change = False
                player_block = False
                card_color_pul=[]
                opponent_try = False
                if player_try and opponent_try and len(cards.get_pul()) == 0:
                    card_is_over=True
                if player_card.value in ("block", "reverse") and not player_try:
                    player_block = True
                while not (choose or opponent_try or player_block or stopgame or card_is_over) and len(player_pul.get_pul()) != 0:
                    for el in opponent_pul.get_pul():
                        card_color_pul.append(el.color)
                    card_count_pul = {
                        "yellow" : card_color_pul.count("yellow"),
                        "red" : card_color_pul.count("red"),
                        "green" : card_color_pul.count("green"),
                        "blue" : card_color_pul.count("blue")
                    }

                    if difficult == "normal":
                        if player_card.value in ("+2", "+4 wild card") and player_card.value in opponent_pul.types() and buff_sum != 0:
                            opponent_card = opponent_pul.get_pul()[opponent_pul.types().index(player_card.value)]
                            choose = True
                        elif player_card.value in ("+2", "+4 wild card") and buff_sum != 0:
                            print("Противник не смог отбить вашу карту")
                            opponent_pul.add(buff_sum, cards)
                            buff_sum = 0
                    if not choose:
                        if len(player_pul.get_pul()) <= 3:
                            if "+4 wild card" in opponent_pul.types():
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("+4 wild card")]
                                choose = True
                            if "+2" in opponent_pul.types():
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("+2")]
                                choose = True
                        if not choose:
                            if "block" in opponent_pul.types() and (opponent_pul.get_pul()[opponent_pul.types().index("block")].color == last_card.color or last_card.value == "block") and card_color_pul.count(opponent_pul.get_pul()[opponent_pul.types().index("block")].color) >= 2:
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("block")]
                                choose = True
                            elif "reverse" in opponent_pul.types() and (opponent_pul.get_pul()[opponent_pul.types().index("reverse")].color == last_card.color or last_card.value == "reverse") and card_color_pul.count(opponent_pul.get_pul()[opponent_pul.types().index("reverse")].color) >= 2:
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("reverse")]
                                choose = True
                            elif last_card.color in card_color_pul and opponent_pul.types()[card_color_pul.index(last_card.color)] not in ("+2", "+4 wild card", "color choose"):
                                opponent_card = opponent_pul.get_pul()[card_color_pul.index(last_card.color)]
                                choose = True
                            elif last_card.value in opponent_pul.types() and opponent_pul.types()[opponent_pul.types().index(last_card.value)] not in ("+2", "+4 wild card" , "color choose"):
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index(last_card.value)]
                                choose = True
                            elif "block" in opponent_pul.types() and (opponent_pul.get_pul()[opponent_pul.types().index("block")].color == last_card.color or last_card.value == "block"):
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("block")]
                                choose = True
                            elif "reverse" in opponent_pul.types() and (opponent_pul.get_pul()[opponent_pul.types().index("reverse")].color == last_card.color or last_card.value == "reverse"):
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("reverse")]
                                choose = True
                            elif "+2" in opponent_pul.types() and opponent_pul.get_pul()[opponent_pul.types().index("+2")].color == last_card.color:
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("+2")]
                                choose = True
                            elif "color choose" in opponent_pul.types():
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("color choose")]
                                choose = True
                            elif "+4 wild card" in opponent_pul.types():
                                opponent_card = opponent_pul.get_pul()[opponent_pul.types().index("+4 wild card")]
                                choose = True
                    if type(opponent_card) is wild_card and choose:
                        opponent_card.select_color("opponent", color=max(card_count_pul, key = card_count_pul.get))
                    if choose:
                        opponent_pul -= [opponent_card]
                        last_card = opponent_card
                        opponent_try = False
                        if opponent_card.value not in ("+2", "color choose", "+4 wild card") and opponent_card in opponent_pul.get_pul():
                            opponent_card_sum=1
                            while opponent_card in opponent_pul.get_pul():
                                opponent_pul -= [opponent_card]
                                opponent_card_sum+=1
                            print(f"Ход противника: {opponent_card} x{opponent_card_sum}")
                        else:
                            print("Ход противника:", opponent_card)
                        if opponent_card.value not in ("block", "reverse"):
                            print("Количество карт противника:", len(opponent_pul.get_pul()))
                        if  opponent_card.value in ("+2", "+4 wild card"):
                            if difficult == "easy":
                                player_pul.add(int(opponent_card.value[1]), cards, True)
                            else:
                                buff_sum += int(opponent_card.value[1])
                    elif not choose:
                        opponent_try = True
                        print("Ход противника: +")
                        opponent_pul.add(1, cards)
                        print("Количество карт противника:", len(opponent_pul.get_pul()))
                        print("Последняя карта:", last_card)
                if not (((opponent_card.value in ("block", "reverse")) and not opponent_try) or ((player_card.value in ("block", "reverse")) and not player_try)):
                    print("")
            end_time = datetime.now()

        elif gamemode=="flip":      # UNO Flip
            if menu_choose != "fast_restart":
                print("")
                print("Выберите уровень сложности:")
                print("1. Лёгкий - нельзя отбивать карты +1, +2 wild card и +5")
                print("2. Нормальный - все стандартные правила игры")
                difficult = DIFICULTS[other_check("difficult")-1]

            light_cards = make_card_pul(RAW_LIGHT_FLIP_CARDS)
            dark_cards = make_card_pul(RAW_DARK_FLIP_CARDS)
            player_light_pul = card_pul([])
            player_dark_pul = card_pul([])
            opponent_light_pul = card_pul([])
            opponent_dark_pul = card_pul([])
            side = "light"

            x = randint(0,len(light_cards.get_pul())-40)
            start_card = light_cards.get_pul()[x]
            light_cards.pop(x)
            dark_cards.pop(x)

            if menu_choose != "fast_restart":
                SizeOfStartPul = other_check("SizeOfStartPul")
            player_light_pul.add(SizeOfStartPul, light_cards)
            player_dark_pul.add(SizeOfStartPul, dark_cards)
            opponent_light_pul.add(SizeOfStartPul, light_cards)
            opponent_dark_pul.add(SizeOfStartPul,dark_cards)

            last_card = start_card
            player_card = start_card
            opponent_card = start_card
            stopgame = False
            player_try = False
            opponent_try = False
            buff_sum = 0
            player_block = False
            card_is_over = False
            pul_is_changed = False

            print("")
            start_time = datetime.now()
            print("Начальная карта:", start_card)

            while not (stopgame or card_is_over) and len(player_light_pul.get_pul()) != 0 and len(opponent_light_pul.get_pul()) != 0:
                opponent_block = False
                card_is_flip = False
                current_player_pul = active_pul(player_light_pul,player_dark_pul,side)

                if not (player_block or opponent_try):
                    if opponent_card.value in ("+1", "+2 wild card", "+5") and not (opponent_card.value in current_player_pul.types()) and buff_sum != 0 and difficult=="normal":
                        print("Вы не можете отбить карту противника")
                        player_light_pul.add(buff_sum, light_cards, True if side == "light" else False)
                        player_dark_pul.add(buff_sum, dark_cards, True if side == "dark" else False)
                        buff_sum = 0
                    elif opponent_card.value in ("+1", "+2 wild card", "+5") and buff_sum != 0:
                        print("Будете ли вы отбивать карту противника?")
                        deef = input("y (yes) / n (no): ")
                        while deef != "y" and deef != "n":
                            print("Некорректный ввод")
                            deef=input("Пожалуйста повторите ввод: ")
                        if deef == "y":
                            changed_pul = []
                            for el in current_player_pul.get_pul():
                                if (opponent_card.value == "+1" and el.value == "+1") or (opponent_card.value == "+2 wild card" and el.value == "+2 wild card") or (opponent_card.value == "+5" and el.value == "+5"):
                                    changed_pul.append(el)
                            changed_pul = card_pul(changed_pul)
                            changed_pul, current_player_pul = current_player_pul, changed_pul
                            pul_is_changed=True
                        else:
                            print("Вы отказались отбивать карту противника.")
                            player_light_pul.add(buff_sum, light_cards, True if side == "light" else False)
                            player_dark_pul.add(buff_sum, dark_cards, True if side == "dark" else False)
                            buff_sum=0
                if player_try and opponent_try and len(light_cards.get_pul()) == 0:
                    card_is_over = True
                if opponent_card.value in ("block", "reverse", "again") and not opponent_try:
                    opponent_block = True

                if not opponent_block and not card_is_over:
                    print(f"Ваш набор карт:\n{current_player_pul}")
                    print('Выберите карту для хода. Если подходящей карты нет введите "+"')
                    player_choose = str.lower(input())
                    player_choose = check_correct(card_check(player_choose, current_player_pul.get_pul()), last_card, current_player_pul.get_pul())

                    if player_choose == "+":
                        player_try = True
                        player_light_pul.add(1, light_cards, True if side == "light" else False)
                        player_dark_pul.add(1, dark_cards, True if side == "dark" else False)

                    elif player_choose == "stop":
                        stopgame = True

                    else:
                        player_index = int(player_choose)-1
                        player_card = current_player_pul.get_pul()[player_index]

                        if type(player_card) is wild_card:
                            player_card.select_color("player", side)

                        if player_card.value in ("+1", "+2 wild card", "+5"):
                            if difficult == "easy":
                                opponent_light_pul.add(int(player_card.value[1]), light_cards)
                                opponent_dark_pul.add(int(player_card.value[1]), dark_cards)
                            elif difficult == "normal":
                                buff_sum += int(player_card.value[1])
                        elif player_card.value == "wild draw color":
                            opponent_light_pul.add(opponent_dark_pul.extra_add(player_card.color, dark_cards), light_cards)
                        if player_card.value == "flip":
                            print(f"Ваш ход: {player_card}, ", end="")
                            if side == "light":
                                side = "dark"
                                player_card = player_dark_pul.get_pul()[player_index]
                            else:
                                side = "light"
                                player_card = player_light_pul.get_pul()[player_index]
                            if player_card.value in ("+1", "+2 wild card", "+5"):
                                if difficult == "easy":
                                    opponent_light_pul.add(int(player_card.value[1]), light_cards)
                                    opponent_dark_pul.add(int(player_card.value[1]), dark_cards)
                                elif difficult == "normal":
                                    buff_sum += int(player_card.value[1])
                            card_is_flip = True
                        else:
                            print("Ваш ход: ", end="")

                        player_light_pul.pop(player_index)
                        player_dark_pul.pop(player_index)
                        last_card = player_card
                        player_try = False

                        if pul_is_changed:
                            if side == "light":
                                player_dark_pul -= [player_light_pul[player_light_pul.types().index(player_card.value)]]
                                player_light_pul -= [player_card]
                            elif side == "dark":
                                player_light_pul -= [player_dark_pul[player_dark_pul.types().index(player_card.value)]]
                                player_dark_pul -= [player_card]
                        if player_card in current_player_pul.get_pul() and player_card.value not in ("+1", "+5"):
                            card_sum = 1
                            while player_card in current_player_pul.get_pul():
                                card_sum += 1
                                player_index = current_player_pul.get_pul().index(player_card)
                                player_light_pul.pop(player_index)
                                player_dark_pul.pop(player_index)          
                            print(f"{player_card} x{card_sum}")
                        else:
                            print(player_card)
                        if card_is_flip:
                            if type(player_card) is wild_card:
                                player_card.select_color("player", side)
                                print("Ваш ход:", player_card)
                            if player_card.value == "wild draw color":
                                opponent_light_pul.add(opponent_dark_pul.extra_add(player_card.color, dark_cards), light_cards)                        
                if not (((opponent_card.value in ("block", "reverse", "again")) and not opponent_try) or ((player_card.value in ("block", "reverse", "again")) and not player_try)):
                    print("")

                # Ход противника

                player_block = False
                choose = False
                card_color_pul = []

                if player_card.value in ("block", "reverse", "again") and not player_try:
                    player_block = True
                if player_try and opponent_try and len(light_cards.get_pul()) == 0:
                    card_is_over = True
                current_opponent_pul = active_pul(opponent_light_pul, opponent_dark_pul, side)

                for el in current_opponent_pul.get_pul():
                    card_color_pul.append(el.color)
                    color_count_pul = {
                        "yellow" : card_color_pul.count("yellow"),
                        "red" : card_color_pul.count("red"),
                        "green" : card_color_pul.count("green"),
                        "blue" : card_color_pul.count("blue"),
                        "purple" : card_color_pul.count("purple"),
                        "orange" : card_color_pul.count("orange"),
                        "teal" : card_color_pul.count("teal"),
                        "pink" : card_color_pul.count("pink")
                    }

                if not (player_block or card_is_over):
                    if buff_sum != 0 and difficult == "normal":
                        if player_card.value in current_opponent_pul.types():
                            opponent_card = current_opponent_pul.get_pul()[current_opponent_pul.types().index(player_card.value)]
                            choose = True
                        else:
                            print("Противник не смог отбить вашу карту")
                            opponent_light_pul.add(buff_sum, light_cards)
                            opponent_dark_pul.add(buff_sum, dark_cards)
                            buff_sum = 0
                            current_opponent_pul = active_pul(opponent_light_pul, opponent_dark_pul, side)
                    if not choose:
                        if len(player_light_pul.get_pul()) <= 3:
                            for el in current_opponent_pul.get_pul():
                                if el.value in ("+1","+2 wild card","+5","wild draw color"):
                                    opponent_card = el
                                    choose = True
                                    break
                        if not choose:
                            for el in current_opponent_pul.get_pul():
                                if (el.color == last_card.color or el.value == last_card.value) and el.value in ("block, reverse, again") and color_count_pul[el.color] >= 3:
                                    opponent_card = el
                                    choose = True
                                    break
                        if not choose:
                            for el in current_opponent_pul.get_pul():
                                if el.color == last_card.color and el.value not in ("+2", "+5"):
                                    opponent_card = el
                                    choose = True
                                    break
                        if not choose:
                            for el in current_opponent_pul.get_pul():
                                if el.color == last_card.color:
                                    opponent_card = el
                                    choose = True
                                    break
                        if not choose:
                            for el in current_opponent_pul.get_pul():
                                if el.value == last_card.value:
                                    opponent_card = el
                                    choose = True
                                    break
                        if not choose:
                            for el in current_opponent_pul.get_pul():
                                if type(el) is wild_card:
                                    opponent_card = el
                                    choose = True
                                    break

                    if choose:
                        opponent_index = current_opponent_pul.get_pul().index(opponent_card)

                        if type(opponent_card) is wild_card:
                            opponent_card.select_color("opponent", side, max(color_count_pul, key = color_count_pul.get))
                        if opponent_card.value in ("+1", "+2 wild card", "+5"):
                            if difficult == "easy":
                                player_light_pul.add(int(opponent_card.value[1]), light_cards, True)
                            elif difficult == "normal":
                                buff_sum += int(opponent_card.value[1])
                        if opponent_card.value == "flip":
                            print(f"Ход противника: {opponent_card}, ", end="")
                            if side == "light":
                                side = "dark"
                                opponent_card = opponent_dark_pul.get_pul()[opponent_index]
                            elif side == "dark":
                                side = "light"
                                opponent_card = opponent_light_pul.get_pul()[opponent_index]
                            if type(opponent_card) is wild_card:
                                opponent_card.select_color("opponent", side, max(color_count_pul, key = color_count_pul.get))
                            if opponent_card.value in ("+1", "+2 wild card", "+5"):
                                if difficult == "easy":
                                    player_light_pul.add(int(opponent_card.value[1]))
                                elif difficult == "normal":
                                    buff_sum += int(opponent_card.value[1])
                            elif opponent_card.value == "wild draw color":
                                player_light_pul.add(player_dark_pul.extra_add(opponent_card.color, dark_cards, True), light_cards)
                        else:
                            print("Ход противника: ", end="")

                        opponent_light_pul.pop(opponent_index)
                        opponent_dark_pul.pop(opponent_index)
                        last_card = opponent_card
                        opponent_try = False
                        if opponent_card in current_opponent_pul.get_pul() and opponent_card.value not in ("+1", "+5"):
                            card_sum = 1
                            while opponent_card in current_opponent_pul.get_pul():
                                opponent_index = current_opponent_pul.get_pul().index(opponent_card)
                                opponent_light_pul.pop(opponent_index)
                                opponent_dark_pul.pop(opponent_index)
                                card_sum += 1
                            print(f"{opponent_card} x{card_sum}")
                        else:
                            print(opponent_card)
                        if opponent_card.value == "wild draw color":
                            player_light_pul.add(player_dark_pul.extra_add(opponent_card.color, dark_cards, True), light_cards)
                    elif not choose:
                        opponent_try = True
                        print("Ход противника: +")
                        opponent_light_pul.add(1, light_cards)
                        opponent_dark_pul.add(1, dark_cards)
                        print("Количество карт противника:", len(opponent_light_pul.get_pul()))
                        print("Последняя карта:",last_card)
                    if choose and opponent_card.value not in ("block", "reverse", "again"):
                        print("Количество карт противника", len(opponent_light_pul.get_pul()))
                if not (((opponent_card.value in ("block", "reverse", "again")) and not opponent_try) or ((player_card.value in ("block", "reverse", "again")) and not player_try)):
                    print("")

        # Результаты партии

        end_time = datetime.now()
        game_stats = {
            "all_win": 0, "all_game": 0,
            "classic_game": 0, "classic_win": 0, "classic_easy_game": 0, "classic_easy_win": 0, "classic_normal_game": 0, "classic_normal_win": 0,
            "flip_game": 0, "flip_win": 0, "flip_easy_game": 0, "flip_easy_win": 0, "flip_normal_game": 0, "flip_normal_win": 0
        }
        if gamemode=="classic":     # Подсчёт для UNO Classic
            if len(player_pul.get_pul()) == 0:      # Победа игрока
                game_result = "Победа"
                print("Поздравляем, вы выиграли!")
                print("Оставшиеся карты противника:", opponent_pul)
                session_stats["classic_win"] += 1
                session_stats["all_win"] += 1
                session_stats[f"classic_{difficult}_win"] += 1
                game_stats["classic_win"] += 1
                game_stats["all_win"] += 1
                game_stats[f"classic_{difficult}_win"] += 1
            elif len(opponent_pul.get_pul()) == 0:       # Победа противника
                game_result = "Поражение"
                print("Ваши оставшиеся карты:", player_pul)
                print("К сожалению вы проиграли :(")
                print("Повезёт в следующий раз!")
            elif stopgame == True:      # Принудительная остановка
                game_result = "Принудительная остановка"
                print('Игра была принудительно остановалена командой "stop"')
            elif card_is_over == True:      # Колода закончилась
                game_result = "Закончилась колода"
                print("Игра закончилась т.к. колода закончилась и никто не может сделать ход")
            session_stats["classic_game"] += 1
            session_stats["all_game"] += 1
            session_stats[f"classic_{difficult}_game"] += 1
            game_stats["classic_game"] += 1
            game_stats["all_game"] += 1
            game_stats[f"classic_{difficult}_game"] += 1
        elif gamemode == "flip":      # Подсчёт для UNO Flip
            if len(player_light_pul.get_pul()) == 0:   # Победа игрока
                game_result = "Победа"
                print("Поздравляем, вы выиграли!")
                print("Оставшиеся карты противника (светлые):", opponent_light_pul)
                print("Оставшиеся карты противника (тёмные):", opponent_dark_pul)
                session_stats["flip_win"] += 1
                session_stats["all_win"] += 1
                session_stats[f"flip_{difficult}_win"] += 1
                game_stats["flip_win"] += 1
                game_stats["all_win"] += 1
                game_stats[f"flip_{difficult}_win"] += 1
            elif len(opponent_light_pul.get_pul()) == 0:     # Победа противника
                game_result = "Поражение"
                print("Ваши оставшиеся карты (светлые):", player_light_pul)
                print("Ваши оставшиеся карты (тёмные):", player_dark_pul)
                print("К сожалению вы проиграли :(")
                print("Повезёт в следующий раз!")
            elif stopgame:      # Принудительная остановка
                game_result = "Принудительная остановка"
                print('Игра была принудительно остановлена командой "stop"')
            elif card_is_over:      # Колода закончилась
                game_result = "Закончилась колода (ничья)"
                print("Игра закончилась т.к. колода закончилась и никто не может сделать ход")
            session_stats["flip_game"] += 1
            session_stats["all_game"] += 1
            session_stats[f"flip_{difficult}_game"] += 1
            game_stats["flip_game"] += 1
            game_stats["all_game"] += 1
            game_stats[f"flip_{difficult}_game"] += 1
        print("")
        print(f"Длительность игры: {(end_time - start_time).seconds // 60} мин. {(end_time - start_time).seconds % 60} сек.")
        print("")
        print("Статистика сессии (побед/партий):")
        print("")
        print(f"Всего: {session_stats["all_win"]}/{session_stats["all_game"]}")
        if session_stats["classic_game"] != 0:       # Вывод для UNO Classic
            print(f"UNO Classic: {session_stats["classic_win"]}/{session_stats["classic_game"]}")
            if session_stats["classic_easy_game"] > 0:
                print(f"Лёгкая сложность: {session_stats["classic_easy_win"]}/{session_stats["classic_easy_game"]}")
            if session_stats["classic_normal_game"] > 0:
                print(f"Нормальная сложность: {session_stats["classic_normal_win"]}/{session_stats["classic_normal_game"]}")
        if session_stats["flip_game"] != 0:      # Вывод для UNO Flip
            print(f"UNO Flip: {session_stats["flip_win"]}/{session_stats["flip_game"]}")
            if session_stats["flip_easy_game"] != 0:
                print(f"Лёгкая сложность: {session_stats["flip_easy_win"]}/{session_stats["flip_easy_game"]}")
            if session_stats["flip_normal_game"] != 0:
                print(f"Нормальная сложность: {session_stats["flip_normal_win"]}/{session_stats["flip_normal_game"]}")

        with open("stats.json", "r+") as global_stats:
            data = json.load(global_stats)

            stats = data["stats"]
            for key in stats.keys():
                stats[key] += game_stats[key]
            data["stats"] = stats

            replays = data["replays"]
            replay = {
                "start_time": start_time.strftime("%d.%m.%Y %H:%M:%S"),
                "end_time": end_time.strftime("%d.%m.%Y %H:%M:%S"),
                "play_time": f"{(end_time - start_time).seconds // 60} мин. {(end_time - start_time).seconds % 60} сек.",
                "gamemode": gamemode,
                "difficult": difficult,
                "SOSP": SizeOfStartPul,
                "game_result": game_result
            }
            replays.append(replay)
            if len(replays) > 20:
                replays = replays[-20:]
            data["replays"] = replays

            last_parameter = {
                "gamemode": gamemode,
                "difficult": difficult,
                "SOSP": SizeOfStartPul,
            }
            data["last_parameter"] = last_parameter

            global_stats.seek(0)
            json.dump(data, global_stats, indent=4)
            global_stats.truncate()
            
        print("")
        input("Для продолжения нажмите enter: ")

    elif menu_choose == "rules":

        print("")
        print("Правила игры:")
        
        print("Действуют все базовые правила игры UNO")
        print('Игру можно принудительно остановить в любое время командой "stop"')
        print("")
        print("Как играть:")
        print('Для выбора карты введите в окно для ввода её номер в вашей колоде или название вида "7 red" без кавычек')
        print('Если подходящей карты нет введите "+"')
        print("")
        print("Особенности UNO Flip:")
        print("Двухсторонняя колода. У карт есть 2 стороны (тёмная и светлая) которые меняются с помощью специальной карты")
        print("Игра начинается со светлой стороны")
        print("Специальные карты:")
        print('"flip" - Имеет цвет, меняет сторону колоды. Есть светлый и тёмный вариант')
        print('"+1" - Аналог "+2". Имеет только светлый вариант')
        print('"+2 wild card" - Аналог "+4 wild card". Имеет только светлый вариант')
        print('"+5" - Аналог "+2". Имеет только тёмный вариант')
        print('"again" - Имеет цвет, позволяет вам повторить ход. Имеет только тёмный вариант')
        print('"wild draw color" - Дикая карта, заставляет следующего игрока брать карты до тех пор пока не вытянет выбранный цвет или не закончится колода. \nНельзя отбить. Имеет только тёмный вариант')
        print("")
        input("Для продолжения нажмите enter: ")

    elif menu_choose == "n_stats":
        print("")
        with open("stats.json", "r") as file:
            replays = json.load(file)["replays"]

            n = input("Выберите статистику по какому кол-ву игр вы хотите увидеть (не больше 20): ")
            while n not in "1234567891011121314151617181920" or n == "" or (n in "1234567891011121314151617181920" and int(n) > len(replays)):
                if n not in "1234567891011121314151617181920":
                    print("Некорректный ввод")
                    n = input("Выберите статистику по какому кол-ву игр вы хотите увидеть (не больше 20): ")
                else:
                    print("Вы ещё не сыграли столько игр, на данный момент сыграно:", len(replays))
                    n = input("Выберите статистику по какому кол-ву игр вы хотите увидеть (не больше 20): ")

            for i in range(int(n)):
                print("")
                print(i+1)
                replay = replays[i]
                print("Время начала партии:", replay["start_time"])
                print("Время конца партии: ", replay["end_time"])
                print("Длительность партии:", replay["play_time"])
                print("Режим игры:", replay["gamemode"])
                print("Сложность :", replay["difficult"])
                print("Размер стартовой колоды:", replay["SOSP"])
                print("Исход партии:", replay["game_result"])
        print("")
        input("Для продолжения нажмите enter: ")

    elif menu_choose == "global_stats":
        print("")
        print("Общая статистика (побед/партий)")
        print("")
        with open("stats.json", "r") as file:
            stats = json.load(file)["stats"]
            print(f"Всего: {stats["all_win"]}/{stats["all_game"]}")
            if stats["classic_game"] != 0:       # Вывод для UNO Classic
                print(f"UNO Classic: {stats["classic_win"]}/{stats["classic_game"]}")
                if stats["classic_easy_game"] > 0:
                    print(f"Лёгкая сложность: {stats["classic_easy_win"]}/{stats["classic_easy_game"]}")
                if stats["classic_normal_game"] > 0:
                    print(f"Нормальная сложность: {stats["classic_normal_win"]}/{stats["classic_normal_game"]}")
            if stats["flip_game"] != 0:      # Вывод для UNO Flip
                print(f"UNO Flip: {stats["flip_win"]}/{stats["flip_game"]}")
                if stats["flip_easy_game"] != 0:
                    print(f"Лёгкая сложность: {stats["flip_easy_win"]}/{stats["flip_easy_game"]}")
                if stats["flip_normal_game"] != 0:
                    print(f"Нормальная сложность: {stats["flip_normal_win"]}/{stats["flip_normal_game"]}")
        print("")
        input("Для продолжения нажмите enter: ")

    elif menu_choose == "quit":
        running = False

print("Игра завершена")