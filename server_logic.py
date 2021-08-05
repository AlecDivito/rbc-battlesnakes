from training.game import Game
from training.population import Population
from training.constant import BoardItem
import numpy as np

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


class State:

    def __init__(self) -> None:
        self.world = {}
        self.population = Population(100)
        self.train = True

    def set_training(self, train=True):
        self.train = train

    def newGame(self, id):
        """
        This function takes an ID and initializes a snake for a new game.

        This function returns nothing
        """
        with open("test.txt", "a") as myfile:
            myfile.write('new game')
            if self.train is True:
                myfile.write('create snake')
                self.population.create_snake(id)
            else:
                myfile.write('random game')
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

    def evolve(self):
        if self.train is True:
            self.population.evolve()
            self.population.save_best()
        else:
            raise ValueError(
                'You can\'t evolve the network without it being in train mode.')
