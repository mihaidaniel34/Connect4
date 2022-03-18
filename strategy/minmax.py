import math
import random

from board.cell import Cell


class Strategy:
    def __init__(self, game):
        self.game = game

    def move(self, board, value):
        """
        Call the minimax method and make a move
        :param board: The game board
        :param value: The move value
        :return: The Cell where the move was made
        """
        col, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)
        if col in board.get_valid_columns():
            row = board.get_bottom_of_column(col)
            board.set_value(row, col, value)
            return Cell(row, col, value)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = board.get_valid_columns()
        is_terminal = board.verdict is not None
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.verdict == 'lose':
                    if board.latest_move.value == 1:
                        return None, 100000000000000
                    elif board.verdict == 'win':
                        return None, -10000000000000
                    else:  # Game is over, no more valid moves
                        return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, 1)
        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_bottom_of_column(col)
                b_copy = board.copy()
                b_copy.set_value(row, col, 1)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_bottom_of_column(col)
                b_copy = board.copy()
                b_copy.set_value(row, col, 2)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def score_position(self, board, value):
        """
        Calculates the score of the current board
        :param board: The game board
        :param value: The searched value
        :return: The score of the current board
        """
        column_count = 7
        row_count = 6
        sequence_length = 4
        score = 0

        # Score center column
        center_array = board.get_line_values(3)
        center_count = center_array.count(value)
        score += center_count * 3

        # Score Horizontal
        for row in range(row_count):
            row_array = board.get_line_values(row)
            for column in range(column_count - 3):
                sequence = row_array[column:column + sequence_length]
                score += self.evaluate_window(sequence, value)

        # Score Vertical
        for column in range(column_count):
            col_array = board.get_column_values(column)
            for row in range(row_count - 3):
                sequence = col_array[row:row + sequence_length]
                score += self.evaluate_window(sequence, value)

        # Score for diagonals that go from bottom left to top right
        for row in range(row_count - 3):
            for column in range(column_count - 3):
                sequence = [board.cells()[row + i][column + i] for i in range(sequence_length)]
                score += self.evaluate_window(sequence, value)

        for row in range(row_count - 3):
            for column in range(column_count - 3):
                sequence = [board.cells()[row + 3 - i][column + i] for i in range(sequence_length)]
                score += self.evaluate_window(sequence, value)

        return score

    @staticmethod
    def evaluate_window(sequence, value):
        """
        Calculates the score of a sequence
        :param sequence: the sequence
        :param value: the value to be searched
        :return: The score of the sequence
        """
        score = 0
        opponent_value = 2
        if value == 2:
            opponent_value = 1

        if sequence.count(value) == 4:
            score += 100
        elif sequence.count(value) == 3 and sequence.count(0) == 1:
            score += 5
        elif sequence.count(value) == 2 and sequence.count(0) == 2:
            score += 2

        if sequence.count(opponent_value) == 3:
            score -= 100

        return score
