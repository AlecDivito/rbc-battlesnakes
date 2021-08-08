from enum import Enum

import numpy as np


class Evolution(Enum):
    SELECTION = 1
    BEST = 2


BOARD_CATEGORIES = 3


class BoardItem():
    EMPTY = 0
    ENEMYHEAD = 1
    FOOD = 2
    FRIENDLY_HEAD = 3
    FRIENDLY_BODY = 4
    OUT_OF_BOUNDS = 5
