from enum import Enum

import numpy as np


class Evolution(Enum):
    SELECTION = 1
    BEST = 2


BOARD_CATEGORIES = 3

SNAKE_EYESIGHT = 11

class BoardItem():
    EMPTY = 0
    ENEMY_BODY = 1
    ENEMY_HEAD = 2
    FOOD = 3
    FRIENDLY_HEAD = 4
    FRIENDLY_BODY = 5
    OUT_OF_BOUNDS = 6
