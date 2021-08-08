
from math import floor
import numpy as np
from numpy.core.numeric import cross
from training.constant import BOARD_CATEGORIES, BoardItem
from training.network import Network
import os


def one_point_crossover(a, b):
    middle = np.random.randint(0, a.shape[0] - 1)
    p1 = a[middle:]
    p2 = a[:middle]
    return p1 + p2


def multi_point_crossover(a: np.array, b: np.array):
    # choose two points random points
    (m1, m2) = np.random.choice(len(a), 2)

    if m1 > m2:
        temp = m1
        m1 = m2
        m2 = temp

    a[m1:m2] = b[m1:m2]
    return a


class Snake:

    def __init__(self, board_x, board_y, eye_sight=5):
        self.board_x = board_x
        self.board_y = board_y
        self.health = 0  # The current health of the snake
        self.length = 0  # The current length of the snake
        self.turn = 0  # The current turn
        self.fitness = 0  # The current fitness score
        self.eye_sight = eye_sight  # How much of the board he can see
        input_board = (eye_sight * eye_sight) - 1
        nn = [
            (input_board, "relu"),
            (floor((input_board / 4) * 3), "relu"),
            (floor(input_board / 2), "relu"),
            (floor(input_board / 4), "relu"),
            (4, "sigmoid")
        ]
        self.death_by_wall = False
        self.death_by_body = False
        self.network = Network(nn)
        self.moves = []
        self.decisions = []

    def tick(self, turn, health, length, you, board):
        """
        Update health, length and turn value, than decide where to move

        returns the index of where to move
        """
        # Update personal variables
        self.health = health
        self.length = length
        self.turn = turn
        # Look for food
        head = you['head']

        # I guess we're going to change how the snake acts
        # The snake can only see 5

        begin_x = head['x'] - floor(self.eye_sight / 2)
        end_x = head['x'] + floor(self.eye_sight / 2)
        begin_y = head['y'] - floor(self.eye_sight / 2)
        end_y = head['y'] + floor(self.eye_sight / 2)

        # Calculate the closest food

        vision = np.zeros((self.eye_sight * self.eye_sight) - 1)
        index = 0
        for x in range(begin_x, end_x):
            for y in range(begin_y, end_y):
                if x < 0 or x > 10 or y < 0 or y > 10:
                    vision[index] = -1
                elif board[x][y] == BoardItem.FRIENDLY_HEAD:
                    continue  # Skip the head
                elif board[x][y] == BoardItem.FRIENDLY_BODY:
                    vision[index] = -1
                elif board[x][y] == BoardItem.FOOD:
                    # calculate the max distance to the food
                    x_diff = abs(x - head['x'])
                    y_diff = abs(y - head['y'])
                    vision[index] == 1 / (x_diff + y_diff)
                else:
                    vision[index] == 0
                index = index + 1

        decision = self.network.calculateOutput(vision)
        index = decision.argmax()
        self.moves.append(index)
        self.decisions.append(decision)
        return index

    def last_tick(self, data):
        """
        Record reason for dying. Basically, check if it ran into a wall
        """
        head = data['you']['head']
        body = data['you']['body'][1:]
        if (head['x'] < 0 or head['x'] > 10):
            self.death_by_wall = True
        elif (head['y'] < 0 or head['y'] > 10):
            self.death_by_wall = True
        elif (head in body):
            self.death_by_body = True

    def calculateFitness(self):
        """
        Run this method to calculate the successfullness of the given generated
        network.

        Returns a number
        """
        if self.health < 10:
            if (self.death_by_wall == True):
                self.fitness = 0
            elif (self.death_by_body == True):
                self.fitness = 0
        # elif (all(x == self.moves[0] for x in self.moves)):
        #     self.fitness = 0
        else:
            self.fitness = floor(self.turn * (self.length - 2 ** 2))

    def crossover_and_mutate(self, partner, mutation_rate):
        child = Snake(self.board_x, self.board_y)
        # crossover
        flat_network_x = np.array(self.network.flatten())
        flat_network_y = np.array(partner.network.flatten())
        crossover = multi_point_crossover(flat_network_x, flat_network_y)
        # mutate
        r = np.random.uniform(-1.0, 1.0, crossover.shape) < mutation_rate
        v = np.random.uniform(-1.0, 1.0, crossover.shape)
        crossover = r * v + np.logical_not(r) * crossover
        # return child
        child.network.matrixize(crossover)
        return child

    def save_to_file(self, generation):
        self.calculateFitness()
        path = "./network/gen:{}-fitness:{}".format(generation, self.fitness)
        os.makedirs(path, exist_ok=True)
        self.network.save(path)
