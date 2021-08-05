
from math import floor
from training.network import Network
import os


class Snake:

    def __init__(self, board_x, board_y):
        self.health = 0  # The current health of the snake
        self.length = 0  # The current length of the snake
        self.turn = 0  # The current turn
        self.fitness = 0  # The current fitness score
        input_board = board_x * board_y
        nn = [
            (input_board, "relu"),
            (floor(input_board / 4 * 3), "relu"),
            (floor(input_board / 2), "relu"),
            (floor(input_board / 4), "relu"),
            (4, "sigmoid")
        ]
        self.network = Network(nn)
        self.moves = []

    def tick(self, turn, health, length, inputBoard):
        """
        Update health, length and turn value, than decide where to move

        returns the index of where to move
        """
        self.health = health
        self.length = length
        self.turn = turn
        decision = self.network.calculateOutput(inputBoard)
        index = decision.argmax()
        self.moves.append(index)
        return index

    def calculateFitness(self):
        """
        Run this method to calculate the successfullness of the given generated
        network.

        Returns a number
        """
        fitness = self.turn * self.turn
        if (self.turn < 10 or self.length < 10):
            # If all of the moves are the same
            if (all(x == self.moves[0] for x in self.moves)):
                self.fitness = 1
            # If they are not the same, git it the correct score
            else:
                fitness = floor(fitness * pow(2, floor(self.length)))
        else:
            # Finally, if the snake is able to live for many turns and is long,
            # give it a large reward
            fitness *= pow(2, 10)
            fitness *= (self.length - 9)
        self.fitness = fitness

    def mutate(self, rate):
        self.network.mutate(rate)

    def crossover(self, partner):
        child = Snake(11, 11)
        child.network = self.network.crossover(partner.network)
        return child

    def save_to_file(self, generation):
        self.calculateFitness()
        path = "./network/gen:{}-fitness:{}".format(generation, self.fitness)
        os.makedirs(path, exist_ok=True)
        self.network.save(path)
