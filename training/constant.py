from enum import Enum


class Evolution(Enum):
    SELECTION = 1
    BEST = 2


class BoardItem(Enum):
    EMPTY = 0.0
    FOOD = 6.0
    HAZARD = 2.0
    ENEMY_SNAKE = 3.0
    ENEMY_SNAKE_HEAD = 4.0
    FRIENDLY_SNAKE = 5.0
    FRIENDLY_SNAKE_HEAD = 6.0
