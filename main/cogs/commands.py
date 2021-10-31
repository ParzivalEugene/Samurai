from types import SimpleNamespace


class Names(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, Names(value))
            else:
                self.__setattr__(key, value)


commands_names_dict = {
    "chatting":     {
        "help": "help",

    },
    "birthdays":    {
        "help":      "bd_help",
        "set_chat":  "bd_set_chat",
        "up_chat":   "bd_up_chat",
        "del_chat":  "bd_del_chat",
        "show_chat": "bd_show_chat",
        "add":       "bd_add",
        "up":        "bd_update",
        "delete":    "bd_delete",
        "show_bd":   "bd",
        "show_bds":  "bd_show"
    },
    "translator":   {
        "help":                  "tr_help",
        "translate":             "tr_trans",
        "detect_language":       "tr_detect_lang",
        "languages_list":        "tr_list",
        "game_detect_languages": "tr_game"
    },
    "connect_four": {
        "help":      "c4_help",
        "rules":     "c4_rules",
        "init game": "c4",
        "place":     "c4_place",
        "lose":      "c4_lose"
    },
    "mini_cogs":    {
        "help":          "mini_help",
        "head_or_tails": "toss",
        "magic_ball":    "8ball",
        "get_forecast":  "forecast",
        "get_quote":     "inspire"
    },
    "music_player": {
        "help":                  "player_help",
        "join":                  "join",
        "leave":                 "leave",
        "queue":                 "queue",
        "play":                  "play",
        "pause":                 "pause",
        "resume":                "resume",
        "stop":                  "stop",
        "skip":                  "skip",
        "previous":              "previous",
        "shuffle":               "shuffle",
        "loop":                  "loop",
        "volume":                "volume",
        "volume_up":             "up",
        "volume_down":           "down",
        "lyrics":                "lyrics",
        "equalizer":             "eq",
        "advanced_equalizer":    "adveq",
        "now_playing":           "np",
        "skip_to_current_index": "skipto",
        "restart":               "restart",
        "seek":                  "seek",

    },
    "tic_tac_toe":  {
        "game_help": "xo_help",
        "rules":     "xo_rules",
        "init_game": "xo",
        "place":     "xo_place",
        "lose":      "xo_lose"
    },
    "level":        {
        "help":        "level_help",
        "add":         "level_add",
        "up":          "level_up",
        "delete":      "level_del",
        "show_levels": "level_show",
        "show_level":  "level",
        "dashboard":   "level_dashboard"
    },
    "wikipedia":    {
        "help":             "wp_help",
        "wikipedia_search": "wp"
    },
    "glossary":     {
        "help":         "gl_help",
        "view_status":  "gl",
        "set_language": "gl_lang",
        "set_vibe":     "gl_vibe"
    }
}
commands_names = Names(commands_names_dict)
