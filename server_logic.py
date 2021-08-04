import random
from training.population import Population
from training.constant import BoardItem
import numpy as np
from training.snake import Snake
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


class State:

    def __init__(self) -> None:
        self.world = {}
        self.population = Population(100)
        self.train = False

    def set_training(self, train=False):
        self.train = train

    def newGame(self, id):
        """
        This function takes an ID and initializes a snake for a new game.

        This function returns nothing
        """
        if self.train is True:
            self.population.create_snake(id)
        else:
            self.world[id] = Game()

    def move(self, id, data):
        """
        This function performs one `tick` of the game world and moves the
        snake depending on what the network tells it.

        This function returns the direction the snake should go. 
        """
        if self.train is True:
            return self.population.tick(id, data)
        else:
            return self.world[id].tick(data)

    def endGame(self, id):
        """
        This function deletes the game from our state. This could also be
        where we can save some of the results of our game for further testing

        returns nothing.
        """
        if self.train is True:
            self.population.snake_died(id)
        else:
            del self.world[id]


class Game:

    def __init__(self, snake) -> None:
        self.snake = snake

    def tick(self, data):
        game_board = data['board']
        foods = game_board['food']
        hazards = game_board['hazards']

        you = data['you']
        turn = data['turn']
        health = you['health']
        length = you['length']

        # 1. initialize the boards full of zeros
        board = np.zeros((game_board['width'], game_board['height']))

        # 2. set all of the foods on the board
        for food in foods:
            board[food.x][food.y] = BoardItem.FOOD

        # 3. set all of the hazards on the board
        for hazard in hazards:
            board[hazard.x][hazard.y] = BoardItem.HAZARD

        # 4. set enemy snakes and snake heads
        for snake in game_board.snakes:
            for body in snake.body:
                board[body.x][body.y] = BoardItem.ENEMY_SNAKE
            board[snake.head.x][snake.head.y] = BoardItem.ENEMY_SNAKE_HEAD

        # 5. set friendly snake and head
        for body in you.body:
            board[body.x][body.y] = BoardItem.FRIENDLY_SNAKE
        board[you.head.x][you.head.y] = BoardItem.FRIENDLY_SNAKE_HEAD

        # 6. Normalize board with values between 0 and 6
        board /= board.max()/6.0

        # 7. straighten board into a 11*11 1D array
        inputBoard = board.ravel()

        # Send the move to the snake
        next_move = self.snake.tick(turn, health, length, inputBoard)
        possible_moves = ["up", "down", "left", "right"]
        return possible_moves[next_move]
