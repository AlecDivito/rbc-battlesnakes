from math import floor
import random
from training.constant import Evolution
from training.snake import Snake
from training.game import Game

mutation_rate = 0.1


class BestSnake(Snake):
    pass


class Population:

    def __init__(self, population_size):
        # Tracking the size of the population of the snakes
        self.population_size = population_size

        # Keep track of the number of current generations
        self.generation = 0

        # Variables that are kept throughout every generation after
        # the first generation has been successfully passed
        self.global_best_snake = None
        self.best_snake = None
        self.current_gen_snake_queue = []

        # List of alive and dead snakes
        # Both alive and dead snakes point to snake games
        self.aliveSnakeIds = []
        self.deadSnakeIds = []
        self.snake_games = {}

    def create_snake(self, id):
        if self.generation == 0 and self.best_snake is None:
            self.snake_games[id] = Game(Snake(11, 11))
            self.aliveSnakeIds.append(id)
        else:
            if len(self.current_gen_snake_queue) != 0:
                snake = self.current_gen_snake_queue.pop()
                self.snake_games[id] = Game(snake)
                self.aliveSnakeIds.append(id)
            else:
                self.evolve()
                self.create_snake(id)

    def snake_died(self, id):
        self.snake_games[id].output_snake_history(id, self.generation, len(self.snake_games))
        self.aliveSnakeIds.remove(id)
        self.deadSnakeIds.append(id)

    def tick(self, id, data):
        return self.snake_games[id].tick(data)

    def evolve(self, evolve_by=Evolution.SELECTION):
        """
        Taking the current population, we will create a new one taking all of the
        data that we learnt from this population.

        This method resets the current population
        """
        # Find the best snake
        self.best_snake = self.find_best_snake()
        if self.global_best_snake is None:
            self.global_best_snake = self.best_snake
        if self.best_snake.fitness > self.global_best_snake.fitness:
            self.global_best_snake = self.best_snake
            self.global_best_snake.save_to_file(self.generation)

        # Create an evolution queue
        if evolve_by is Evolution.SELECTION:
            self.current_gen_snake_queue = self.__evolve_by_random_selection()
        else:
            self.current_gen_snake_queue = self.__evolve_by_best_snake()

        # Increment generation and reset population
        self.generation = self.generation + 1
        self.aliveSnakeIds = []
        self.deadSnakeIds = []
        self.snake_games = {}

    def mutate(self):
        for key in self.snake_games:
            self.snake_games[key].snake.mutate(mutation_rate)

    def find_best_snake(self):
        """
        Find the best snake with the greatest fitness value

        return that snake
        """
        # Get list of snakes id, sorted by fitness
        sorted_snakes_by_fitness = self.__get_sorted_fitness_array()

        return self.snake_games[sorted_snakes_by_fitness[len(sorted_snakes_by_fitness)-1][0]].snake

    def select_snake(self):
        """
        Randomly select a snake

        returns a randomly selected snake
        """
        # Get list of snakes id, sorted by fitness
        sorted_snakes_by_fitness = self.__get_sorted_fitness_array()

        # Find the total fitness value of all snakes
        fitness_sum = sum(fitness for _, fitness in sorted_snakes_by_fitness)

        # set a random value
        rand = floor(random.randrange(0, fitness_sum))

        # keep the running sum
        running_sum = 0

        # Select the random snake from our fitness list
        for (key, fitness) in sorted_snakes_by_fitness:
            running_sum += fitness
            if running_sum > rand:
                return self.snake_games[key].snake

        # default best snake, just in case
        return self.snake_games[self.deadSnakeIds[0]].snake

    def __get_sorted_fitness_array(self):
        fitness_array = []
        for key in self.snake_games:
            game = self.snake_games[key]
            game.snake.calculateFitness()
            fitness_array.append((key, game.snake.fitness))
        return sorted(fitness_array, key=lambda i: i[1])

    def __evolve_by_random_selection(self):
        next_generation_snakes = []
        for _ in range(self.population_size):
            # select 2 parents by fitness
            parent1 = self.select_snake()
            parent2 = self.select_snake()

            # crossover the 2 snakes to create a child
            child = parent1.crossover(parent2)
            child.mutate(mutation_rate)
            next_generation_snakes.append(child)
        return next_generation_snakes

    def __evolve_by_best_snake(self):
        next_generation_snakes = []
        for _ in range(self.population_size):
            # select 2 parents by fitness
            best_snake = self.best_snake
            best_snake.mutate(mutation_rate)
            next_generation_snakes.append(best_snake)
        return next_generation_snakes
