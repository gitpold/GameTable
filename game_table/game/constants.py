from enum import Enum

class GAME_MODE(Enum):
    GAME_1 = 0
    GAME_2 = 1
    GAME_3 = 2
    GAME_4 = 3
    GAME_5 = 4
    GAME_6 = 5
    GAME_7 = 6
    GAME_8 = 7


class GAME_STATE(Enum):
    PLAYER_SELECTION = 0
    GAME_MODE_SELECTION = 1
    GAME_PLAYING = 2
    GAME_OVER = 3
