import numpy as np
from training.constant import BoardItem


class Game:

    def __init__(self, snake) -> None:
        self.snake = snake
        self.moves = []

    def tick(self, data):
        game_board = data['board']
        foods = game_board['food']
        hazards = game_board['hazards']
        snakes = game_board['snakes']

        you = data['you']
        turn = data['turn']
        health = you['health']
        length = you['length']

        # 1. initialize the boards full of zeros
        board = np.zeros((game_board['width'], game_board['height']))

        # 2. set all of the foods on the board
        for food in foods:
            board[food['x']][food['y']] = BoardItem.FOOD.value

        # 3. set all of the hazards on the board
        # for hazard in hazards:
        #     board[hazard['x']][hazard['y']] = BoardItem.HAZARD.value

        # 4. set enemy snakes and snake heads
        # for snake in snakes:
        #     for body in snake['body']:
        #         board[body['x']][body['y']] = BoardItem.ENEMY_SNAKE.value
        #     board[snake['head']['x']][snake['head']
        #                               ['y']] = BoardItem.ENEMY_SNAKE_HEAD.value

        # 5. set friendly snake and head
        for body in you['body']:
            board[body['x']][body['y']] = BoardItem.FRIENDLY_SNAKE.value
        board[you['head']['x']][you['head']['y']
                                ] = BoardItem.FRIENDLY_SNAKE_HEAD.value

        # 6. Normalize board with values between 0 and 6
        board /= board.max()/6.0

        # 7. straighten board into a 11*11 1D array
        inputBoard = board.ravel()

        # Send the move to the snake
        next_move = self.snake.tick(turn, health, length, inputBoard)
        possible_moves = ["up", "down", "left", "right"]
        self.moves.append(possible_moves[next_move])
        return possible_moves[next_move]

    def output_snake_history(self, id, gen, index):
        print("{} - {} -> {}".format(gen, index, self.moves))
