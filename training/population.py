from math import floor
import random
import numpy as np
from training.constant import Evolution
from training.snake import Snake
from training.game import Game

mutation_rate = 0.99


class BestSnake(Snake):
    pass


class Population:

    def __init__(self):
        # Tracking the size of the population of the snakes
        self.population_size = 0

        # Keep track of the number of current generations
        self.generation = 0

        # default folder that a snake will be saved to
        self.snake_save_folder_path = "./network"

        # Variables that are kept throughout every generation after
        # the first generation has been successfully passed
        self.global_best_snake = None
        self.best_snake = None
        self.current_gen_snake_queue = []

        # List of alive and dead snakes
        # Both alive and dead snakes point to snake games
        self.initial_network_path = None
        self.aliveSnakeIds = []
        self.deadSnakeIds = []
        self.snake_games = {}

    def set_initial_network(self, path):
        self.initial_network_path = path

    def set_save_folder(self, path):
        self.snake_save_folder_path = path

    def create_snake(self, id, number_of_snakes):
        if self.generation == 0 and self.best_snake is None:
            self.snake_games[id] = Game(
                Snake(11, 11, number_of_snakes, self.initial_network_path))
            self.aliveSnakeIds.append(id)
            self.population_size = self.population_size + 1
        else:
            if len(self.current_gen_snake_queue) != 0:
                snake = self.current_gen_snake_queue.pop()
                self.snake_games[id] = Game(snake)
                self.aliveSnakeIds.append(id)
            else:
                if (len(self.snake_games) == self.deadSnakeIds):
                    self.evolve()
                    self.create_snake(id)
                else:
                    raise Exception(
                        "For some reason, we don't have many snakes :/")

    def snake_died(self, id, data):
        self.snake_games[id].snake.last_tick(data)
        self.aliveSnakeIds.remove(id)
        self.deadSnakeIds.append(id)

    def tick(self, id, data):
        if id in self.snake_games:
            return self.snake_games[id].tick(data)
        else:
            return ""

    def evolve(self, evolve_by=Evolution.SELECTION):
        """
        Taking the current population, we will create a new one taking all of the
        data that we learnt from this population.

        This method resets the current population
        """
        # Find the best snake
        self.best_snake = self.find_best_snake()
        print("Evolving Gen {}: best fitness = {} living {} turns with a length of {} and died by (Eat:{},OutOfBounds:{})".format(self.generation,
              self.best_snake.fitness, self.best_snake.turn, self.best_snake.length, self.best_snake.death_by_body, self.best_snake.death_by_wall))
        if self.best_snake.fitness > 500:
            self.best_snake.save_to_file(
                self.snake_save_folder_path, self.generation)
        if self.global_best_snake is None:
            self.global_best_snake = self.best_snake
        else:
            if self.best_snake.fitness >= self.global_best_snake.fitness:
                print("New best! {} > {}".format(
                    self.best_snake.fitness, self.global_best_snake.fitness))
                self.global_best_snake = self.best_snake
            else:
                self.snake_games["best"] = Game(self.global_best_snake.clone())

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
        self.population_size = len(self.current_gen_snake_queue)

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
        with open("./temp/{}.txt".format(self.generation), "w") as file:
            for (key, fitness) in sorted_snakes_by_fitness:
                game = self.snake_games[key]
                file.write("{} -> {} = {} or {}\n".format(fitness,
                           key, game.moves, game.snake.decisions))

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
        if fitness_sum > 0:
            rand = floor(random.randrange(0, fitness_sum))
        else:
            rand = 0

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
        with open("./choice/{}.txt".format(self.generation), "w") as file:
            for _ in range(self.population_size + 1):
                # select 2 parents by fitness
                parent1 = self.select_snake()
                parent2 = self.select_snake()
                file.write("fitness {} merged with {}\n".format(
                    parent1.fitness, parent2.fitness))

                # crossover the 2 snakes to create a child
                child = parent1.crossover_and_mutate(parent2, mutation_rate)
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
