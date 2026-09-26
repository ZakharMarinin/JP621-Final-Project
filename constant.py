# Цвета
COLORS=["yellow","red","green","blue",
        "purple", "orange", "teal", "pink"]
COLORS_PY=["\033[33m", "\033[31m", "\033[32m", "\033[94m",
          "\033[38;5;129m", "\033[38;5;208m", "\033[38;5;37m", "\033[38;5;205m"]
SPEC_COLOR="\033[1;37m"
COLOR_RESET="\033[0m"

# Карты
RAW_CLASSIC_CARDS = ([('0', 'yellow'), ('0', 'red'), ('0', 'green'), ('0', 'blue'), ('0', 'yellow'), ('0', 'red'), ('0', 'green'), ('0', 'blue'),
                    ('1', 'yellow'), ('1', 'red'), ('1', 'green'), ('1', 'blue'), ('1', 'yellow'), ('1', 'red'), ('1', 'green'), ('1', 'blue'),
                    ('2', 'yellow'), ('2', 'red'), ('2', 'green'), ('2', 'blue'), ('2', 'yellow'), ('2', 'red'), ('2', 'green'), ('2', 'blue'),
                    ('3', 'yellow'), ('3', 'red'), ('3', 'green'), ('3', 'blue'), ('3', 'yellow'), ('3', 'red'), ('3', 'green'), ('3', 'blue'),
                    ('4', 'yellow'), ('4', 'red'), ('4', 'green'), ('4', 'blue'), ('4', 'yellow'), ('4', 'red'), ('4', 'green'), ('4', 'blue'),
                    ('5', 'yellow'), ('5', 'red'), ('5', 'green'), ('5', 'blue'), ('5', 'yellow'), ('5', 'red'), ('5', 'green'), ('5', 'blue'),
                    ('6', 'yellow'), ('6', 'red'), ('6', 'green'), ('6', 'blue'), ('6', 'yellow'), ('6', 'red'), ('6', 'green'), ('6', 'blue'),
                    ('7', 'yellow'), ('7', 'red'), ('7', 'green'), ('7', 'blue'), ('7', 'yellow'), ('7', 'red'), ('7', 'green'), ('7', 'blue'),
                    ('8', 'yellow'), ('8', 'red'), ('8', 'green'), ('8', 'blue'), ('8', 'yellow'), ('8', 'red'), ('8', 'green'), ('8', 'blue'),
                    ('9', 'yellow'), ('9', 'red'), ('9', 'green'), ('9', 'blue'), ('9', 'yellow'), ('9', 'red'), ('9', 'green'), ('9', 'blue'),
                    ('block', 'yellow'), ('block', 'red'), ('block', 'green'), ('block', 'blue'),
                    ('reverse', 'yellow'), ('reverse', 'red'), ('reverse', 'green'), ('reverse', 'blue'),
                    ('+2', 'yellow'), ('+2', 'red'), ('+2', 'green'), ('+2', 'blue'), ('+2', 'yellow'), ('+2', 'red'), ('+2', 'green'), ('+2', 'blue'),
                    "color choose","color choose","color choose","color choose","color choose","color choose","color choose","color choose",
                    "+4 wild card","+4 wild card","+4 wild card","+4 wild card"])
RAW_LIGHT_FLIP_CARDS = [('0', 'yellow'), ('0', 'red'), ('0', 'green'), ('0', 'blue'),
                        ('1', 'yellow'), ('1', 'red'), ('1', 'green'), ('1', 'blue'), ('1', 'yellow'), ('1', 'red'), ('1', 'green'), ('1', 'blue'),
                        ('2', 'yellow'), ('2', 'red'), ('2', 'green'), ('2', 'blue'), ('2', 'yellow'), ('2', 'red'), ('2', 'green'), ('2', 'blue'),
                        ('3', 'yellow'), ('3', 'red'), ('3', 'green'), ('3', 'blue'), ('3', 'yellow'), ('3', 'red'), ('3', 'green'), ('3', 'blue'),
                        ('4', 'yellow'), ('4', 'red'), ('4', 'green'), ('4', 'blue'), ('4', 'yellow'), ('4', 'red'), ('4', 'green'), ('4', 'blue'),
                        ('5', 'yellow'), ('5', 'red'), ('5', 'green'), ('5', 'blue'), ('5', 'yellow'), ('5', 'red'), ('5', 'green'), ('5', 'blue'),
                        ('6', 'yellow'), ('6', 'red'), ('6', 'green'), ('6', 'blue'), ('6', 'yellow'), ('6', 'red'), ('6', 'green'), ('6', 'blue'),
                        ('7', 'yellow'), ('7', 'red'), ('7', 'green'), ('7', 'blue'), ('7', 'yellow'), ('7', 'red'), ('7', 'green'), ('7', 'blue'),
                        ('8', 'yellow'), ('8', 'red'), ('8', 'green'), ('8', 'blue'), ('8', 'yellow'), ('8', 'red'), ('8', 'green'), ('8', 'blue'),
                        ('9', 'yellow'), ('9', 'red'), ('9', 'green'), ('9', 'blue'), ('9', 'yellow'), ('9', 'red'), ('9', 'green'), ('9', 'blue'),
                        ('block', 'yellow'), ('block', 'red'), ('block', 'green'), ('block', 'blue'),
                        ('block', 'yellow'), ('block', 'red'), ('block', 'green'), ('block', 'blue'),
                        ('reverse', 'yellow'), ('reverse', 'red'), ('reverse', 'green'), ('reverse', 'blue'),
                        ('reverse', 'yellow'), ('reverse', 'red'), ('reverse', 'green'), ('reverse', 'blue'),
                        ('+1', 'yellow'), ('+1', 'red'), ('+1', 'green'), ('+1', 'blue'),
                        ('+1', 'yellow'), ('+1', 'red'), ('+1', 'green'), ('+1', 'blue'),
                        ('flip', 'yellow'), ('flip', 'red'), ('flip', 'green'), ('flip', 'blue'),
                        ('flip', 'yellow'), ('flip', 'red'), ('flip', 'green'), ('flip', 'blue'),
                        'color choose', 'color choose', 'color choose', 'color choose',
                        '+2 wild card', '+2 wild card', '+2 wild card', '+2 wild card']
RAW_DARK_FLIP_CARDS = [('flip', 'purple'), ('flip', 'orange'), ('flip', 'teal'), ('flip', 'pink'),
                        ('reverse', 'purple'), ('reverse', 'orange'), ('reverse', 'teal'), ('reverse', 'pink'),
                        ('reverse', 'purple'), ('reverse', 'orange'), ('reverse', 'teal'), ('reverse', 'pink'),
                        ('9', 'purple'), ('9', 'orange'), ('9', 'teal'), ('9', 'pink'), ('9', 'purple'), ('9', 'orange'), ('9', 'teal'), ('9', 'pink'),
                        ('8', 'purple'), ('8', 'orange'), ('8', 'teal'), ('8', 'pink'), ('8', 'purple'), ('8', 'orange'), ('8', 'teal'), ('8', 'pink'),
                        ('7', 'purple'), ('7', 'orange'), ('7', 'teal'), ('7', 'pink'), ('7', 'purple'), ('7', 'orange'), ('7', 'teal'), ('7', 'pink'),
                        ('6', 'purple'), ('6', 'orange'), ('6', 'teal'), ('6', 'pink'), ('6', 'purple'), ('6', 'orange'), ('6', 'teal'), ('6', 'pink'),
                        ('5', 'purple'), ('5', 'orange'), ('5', 'teal'), ('5', 'pink'), ('5', 'purple'), ('5', 'orange'), ('5', 'teal'), ('5', 'pink'),
                        ('4', 'purple'), ('4', 'orange'), ('4', 'teal'), ('4', 'pink'), ('4', 'purple'), ('4', 'orange'), ('4', 'teal'), ('4', 'pink'),
                        ('3', 'purple'), ('3', 'orange'), ('3', 'teal'), ('3', 'pink'), ('3', 'purple'), ('3', 'orange'), ('3', 'teal'), ('3', 'pink'),
                        ('2', 'purple'), ('2', 'orange'), ('2', 'teal'), ('2', 'pink'), ('2', 'purple'), ('2', 'orange'), ('2', 'teal'), ('2', 'pink'),
                        ('again', 'purple'), ('again', 'orange'), ('again', 'teal'), ('again', 'pink'),
                        ('again', 'purple'), ('again', 'orange'), ('again', 'teal'), ('again', 'pink'),
                        ('1', 'purple'), ('1', 'orange'), ('1', 'teal'), ('1', 'pink'),
                        ('1', 'purple'), ('1', 'orange'), ('1', 'teal'), ('1', 'pink'),
                        ('+5', 'purple'), ('+5', 'orange'), ('+5', 'teal'), ('+5', 'pink'),
                        ('+5', 'purple'), ('+5', 'orange'), ('+5', 'teal'), ('+5', 'pink'),
                        ('0', 'purple'), ('0', 'orange'), ('0', 'teal'), ('0', 'pink'),
                        ('0', 'purple'), ('0', 'orange'), ('0', 'teal'), ('0', 'pink'),
                        'color choose', 'color choose', 'color choose', 'color choose',
                        'wild draw color', 'wild draw color', 'wild draw color', 'wild draw color']

# Игровые списки / счётчики
GAMEMODES = ["classic", "flip"]
DIFICULTS = ["easy", "normal"]
KEYS = [
    "all_game", "all_win",
    "classic_game", "classic_easy_game", "classic_normal_game",
    "classic_win", "classic_easy_win", "classic_normal_win",
    "flip_game", "flip_easy_game", "flip_normal_game",
    "flip_win", "flip_easy_win", "flip_normal_win"
]
session_stats = dict.fromkeys(KEYS, 0)