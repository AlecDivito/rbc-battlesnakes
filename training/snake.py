
from math import floor
import numpy as np
from training.constant import BOARD_CATEGORIES, BoardItem, SNAKE_EYESIGHT
from training.network import Network
import os


def one_point_crossover(a, b):
    result = {}
    for key in a:
        middle = np.random.randint(0, a[key].shape[0] - 1)
        result[key] = a[key]
        result[key][:middle] = b[key][:middle]
    return result


def multi_point_crossover(a: np.array, b: np.array):
    # choose two points random points
    (m1, m2) = np.random.choice(len(a), 2)

    if m1 > m2:
        temp = m1
        m1 = m2
        m2 = temp

    a[m1:m2] = b[m1:m2]
    return a


def binomial(n, k):
    if 0 <= k <= n:
        ntok = ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0


def P(L, n, p): return binomial(L, n) * p**n * (1-p)**(L-n)


class Snake:

    def __init__(self, board_x, board_y, number_of_snakes, initial_network_path):
        self.board_x = board_x
        self.board_y = board_y
        self.number_of_snakes = number_of_snakes
        self.remaining_snakes = number_of_snakes
        self.health = 0  # The current health of the snake
        self.length = 0  # The current length of the snake
        self.turn = 0  # The current turn
        self.fitness = 0  # The current fitness score
        self.eye_sight = SNAKE_EYESIGHT  # How much of the board he can see
        input_board = (SNAKE_EYESIGHT * SNAKE_EYESIGHT) - 1
        nn = [
            (input_board, "relu"),
            # (floor((input_board / 4) * 3), "relu"),
            (floor(input_board / 2), "relu"),
            (floor(input_board / 4), "relu"),
            (4, "sigmoid")
        ]
        self.network = Network(nn)
        if initial_network_path != None:
            self.network.load_network_from_path(initial_network_path)
        self.death_by_wall = False
        self.death_by_body = False
        self.moves = []
        self.decisions = []
        self.penalty = []

    def clone(self):
        snake = Snake(self.board_x, self.board_y, self.number_of_snakes, None)
        snake.health = self.health
        snake.length = self.length
        snake.turn = self.turn
        snake.fitness = self.fitness
        snake.death_by_wall = self.death_by_wall
        snake.death_by_body = self.death_by_body
        snake.network = self.network.clone()
        snake.moves = self.moves
        snake.decisions = self.decisions
        snake.penalty = self.penalty
        return snake

    def tick(self, turn, health, length, remaining_snakes, you, board):
        """
        Update health, length and turn value, than decide where to move

        returns the index of where to move
        """
        # Update personal variables
        self.health = health
        self.length = length
        self.turn = turn
        self.remaining_snakes = remaining_snakes
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
                    x_diff = abs(x - head['x'])
                    y_diff = abs(y - head['y'])
                    vision[index] == (1 / (x_diff + y_diff)) * -1
                elif board[x][y] == BoardItem.FOOD:
                    # calculate the max distance to the food
                    x_diff = abs(x - head['x'])
                    y_diff = abs(y - head['y'])
                    vision[index] == 1 / (x_diff + y_diff)
                index = index + 1

        decision = self.network.calculateOutput(vision)
        index = decision.argmax()

        # Our fitness function needs to be more complicated. Therefore, we need
        # some way of tracking the "penalties" that the snake commits during the
        # game. The biggest one is if it tries to move where it's body is.
        if index == 0:  # up
            y = head['y'] + 1
            if y > 0 and y < 10 and board[head['x']][y] == BoardItem.FRIENDLY_BODY:
                self.penalty.append(1)
        elif index == 1:  # down
            y = head['y'] - 1
            if y > 0 and y < 10 and board[head['x']][y] == BoardItem.FRIENDLY_BODY:
                self.penalty.append(1)
        elif index == 2:  # left
            head['x'] - 1
            if x > 0 and x < 10 and board[x][head['y']] == BoardItem.FRIENDLY_BODY:
                self.penalty.append(1)
        elif index == 3:  # right
            head['x'] + 1
            if x > 0 and x < 10 and board[x][head['y']] == BoardItem.FRIENDLY_BODY:
                self.penalty.append(1)

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
        if (self.death_by_wall == True):
            self.fitness = floor((self.length - 3) - len(self.penalty))
        elif (self.death_by_body == True):
            self.fitness = floor((self.length - 3) -
                                 len(self.penalty) + (self.turn / 10))
        else:
            self.fitness = self.turn * (self.length - 2)

        if self.remaining_snakes > 1:
            self.fitness = self.fitness / self.remaining_snakes

    def crossover_and_mutate(self, partner, mutation_rate):
        child = Snake(self.board_x, self.board_y, self.number_of_snakes, None)
        # crossover
        flat_network_x = self.network.flatten()
        flat_network_y = partner.network.flatten()
        crossover = one_point_crossover(flat_network_x, flat_network_y)
        # mutate
        for key in crossover:
            r = np.random.uniform(-1.0, 1.0,
                                  crossover[key].shape) > mutation_rate
            v = np.random.uniform(-1.0, 1.0, crossover[key].shape)
            for index in range(len(r)):
                result = r[index]
                if result == True:
                    crossover[key][index] = v[index]
        # return child
        child.network.matrixize(crossover)
        return child

    def save_to_file(self, folder, generation):
        self.calculateFitness()
        path = "{}/gen:{}-fitness:{}".format(folder, generation, self.fitness)
        os.makedirs(path, exist_ok=True)
        self.network.save(path)
