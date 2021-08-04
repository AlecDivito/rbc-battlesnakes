
from math import floor
from training.network import Network


class Snake:

    def __init__(self, board_x, board_y):
        self.health = 0  # The current health of the snake
        self.length = 0  # The current length of the snake
        self.turn = 0  # The current turn
        self.fitness = 0  # The current fitness score
        self.network = Network(board_x * board_y, board_x * board_y, 4)

    def tick(self, turn, health, length, inputBoard):
        """
        Update health, length and turn value, than decide where to move

        returns the index of where to move
        """
        self.health = health
        self.length = length
        self.turn = turn
        decision = self.network.calculateOutput(inputBoard)
        return decision.argmax()

    def calculateFitness(self):
        """
        Run this method to calculate the successfullness of the given generated
        network.

        Returns a number
        """
        fitness = self.turn * self.turn
        if (self.length < 10):
            fitness = floor(fitness * pow(2, floor(self.length)))
        else:
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
        filename = "./network/gen:{}-fitness:{}.dat".format(
            generation, self.fitness)
        self.network.save(filename)
