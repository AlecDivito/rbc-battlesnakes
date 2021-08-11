import numpy as np
from training.constant import BOARD_CATEGORIES, BoardItem


class Game:

    def __init__(self, snake) -> None:
        self.snake = snake
        self.moves = []

    def clone(self) -> None:
        game = Game(self.snake.clone())
        game.moves = self.moves
        return game

    def tick(self, data):
        game_board = data['board']
        foods = game_board['food']

        you = data['you']
        turn = data['turn']
        health = you['health']
        length = you['length']
        remaining_snakes = len(data['board']['snakes'])

        # 1. initialize the boards full of zeros
        board = np.empty(
            shape=(game_board['width'], game_board['height']))
        board.fill(BoardItem.EMPTY)

        # 2. set all of the foods on the board
        for food in foods:
            board[food['x']][food['y']] = BoardItem.FOOD

        # 3. set all of the hazards on the board
        if "hazards" in game_board:
            for hazard in game_board['hazards']:
                board[hazard['x']][hazard['y']] = BoardItem.OUT_OF_BOUNDS

        # 4. set enemy snakes and snake heads
        if "snakes" in game_board:
            for snake in game_board['snakes']:
                for body in snake['body']:
                    board[body['x']][body['y']] = BoardItem.OUT_OF_BOUNDS
                board[snake['head']['x']][snake['head']
                                          ['y']] = BoardItem.ENEMYHEAD

        # 5. set friendly snake and head
        for body in you['body']:
            board[body['x']][body['y']] = BoardItem.FRIENDLY_BODY
        board[you['head']['x']][you['head']['y']] = BoardItem.FRIENDLY_HEAD

        # Send the move to the snake
        next_move = self.snake.tick(
            turn, health, length, remaining_snakes, you, board)
        possible_moves = ["up", "down", "left", "right"]
        self.moves.append(possible_moves[next_move])
        return possible_moves[next_move]
