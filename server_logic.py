import os
from training.snake import Snake
from training.game import Game
from training.population import Population
from training.constant import BoardItem, Evolution
import numpy as np
import shutil

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


class State:

    def __init__(self, debug) -> None:
        self.world = {}
        self.population = Population(debug)
        self.train = True
        self.default_network_path = None
        self.training_iterations = None
        self.iterations = 0
        self.allow_download_of_training_data = False

    def set_training(self, train=True):
        self.train = train

    def set_initial_network(self, path):
        self.default_network_path = path
        self.population.set_initial_network(path)

    def set_save_folder(self, folder):
        # check if it exists, if it doesn't, create it
        os.makedirs(folder, exist_ok=True)
        self.population.set_save_folder(folder)

    def set_training_iterations(self, iterations):
        self.training_iterations = iterations
        self.population.set_multisnake_iteration_size(iterations)

    def enable_download_training_data(self, can_download_training_data):
        self.allow_download_of_training_data = can_download_training_data

    def build_data_zip_file(self):
        if self.allow_download_of_training_data == False:
            return "./no.txt"
        output = "./data.zip"
        shutil.make_archive(
            output, 'zip', self.population.snake_save_folder_path)
        return output

    def newGame(self, id, number_of_snakes):
        """
        This function takes an ID and initializes a snake for a new game.

        This function returns nothing
        """
        if self.train is True:
            self.population.create_snake(id, number_of_snakes)
        else:
            self.world[id] = Game(
                Snake(11, 11, number_of_snakes, self.default_network_path))

    def move(self, id, data):
        """
        This function performs one `tick` of the game world and moves the
        snake depending on what the network tells it.

        This function returns the direction the snake should go. 
        """
        if self.train is True:
            return self.population.tick(id, data)
        else:
            if id in self.world:
                return self.world[id].tick(data)
            else:
                self.world[id] = Game(Snake(11, 11, self.default_network_path))
                return self.world[id].tick(data)

    def endGame(self, id, data):
        """
        This function deletes the game from our state. This could also be
        where we can save some of the results of our game for further testing

        returns nothing.
        """
        if self.train is True:
            self.population.snake_died(id, data)
            if self.training_iterations is not None:
                self.iterations = self.iterations + 1
            if self.iterations == self.training_iterations:
                self.population.evolve(Evolution.SELECTION)
                self.iterations = 0
        else:
            self.world[id].snake.last_tick(data)
            del self.world[id]

    def evolve(self):
        if self.train is True:
            self.population.evolve(Evolution.SELECTION)
        else:
            raise ValueError(
                'You can\'t evolve the network without it being in train mode.')
