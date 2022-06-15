class OrthokonBoard:
    def __init__(self):
        """Initializes the board"""
        # 1 = red, 2 = yellow, 0 = empty space
        self._board = [[1, 1, 1, 1],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [2, 2, 2, 2]]
        # game state can be: "RED_WON" "YELLOW_WON" "UNFINISHED"
        self._game_state = "UNFINISHED"

    def get_game_state(self):
        """Returns the game state"""
        return self._game_state

    def _out_of_bounds(self, row, col):
        """Check whether a position is out of bounds
            Returns True if out of bounds, False if in bounds"""
        if (0 <= row <= 3) and (0 <= col <= 3):
            return False
        return True

    def _is_valid_move(self, row_1, col_1, row_2, col_2):
        """returns True if the move is valid, False if not"""
        # not moving to start position
        if row_1 == row_2 and col_1 == col_2:
            return False
        # within the bounds of the board
        if self._out_of_bounds(row_1, col_1) or self._out_of_bounds(row_2, col_2):
            return False
        # piece exists in starting position
        if self._board[row_1][col_1] == 0:  # fixed -> was row_2, should be col_1
            return False
        # destination is empty
        if self._board[row_2][col_2] > 0:
            return False
        # movement is horizontal, vertical, or diagonal
        row_mov = row_2 - row_1
        col_mov = col_2 - col_1
        if row_mov != 0 and col_mov != 0 and abs(row_mov) != abs(col_mov):
            return False
        # has a valid stopping point - next position is out of bounds or has a piece in it
        if row_mov != 0:
            row_mov = row_mov // abs(row_mov)
        if col_mov != 0:
            col_mov = col_mov // abs(col_mov)
        next_row = row_2 + row_mov
        next_col = col_2 + col_mov
        if not self._out_of_bounds(next_row, next_col) and self._board[next_row][next_col] == 0:
            return False
        # no obstacles in between
        next_row = row_1 + row_mov
        next_col = col_1 + col_mov  # <- was broken: changed col_2 to col_1
        while next_row != row_2 or next_col != col_2:  # <- was broken: changed from "and" to "or"
            if self._board[next_row][next_col] > 0:  # <- was broken: result of col_2 to col_1
                return False
            next_row += row_mov
            next_col += col_mov
        return True

    def _change_color(self, row_2, col_2, player, opponent):
        """change orthogonal opponent pieces to player's color"""
        if not self._out_of_bounds(row_2 - 1, col_2) and self._board[row_2 - 1][col_2] == opponent:
            self._board[row_2 - 1][col_2] = player
        if not self._out_of_bounds(row_2 + 1, col_2) and self._board[row_2 + 1][col_2] == opponent:
            self._board[row_2 + 1][col_2] = player
        if not self._out_of_bounds(row_2, col_2 - 1) and self._board[row_2][col_2 - 1] == opponent:
            self._board[row_2][col_2 - 1] = player
        if not self._out_of_bounds(row_2, col_2 + 1) and self._board[row_2][col_2 + 1] == opponent:
            self._board[row_2][col_2 + 1] = player
        return

    def _update_game_state(self, opponent):
        """Check whether opponent has valid moves"""
        turtle = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # in honor of YOU
        for row in range(4):
            for col in range(4):
                if self._board[row][col] == opponent:
                    for tu in turtle:
                        if not self._out_of_bounds(row + tu[0], col + tu[1]) and self._board[row + tu[0]][col + tu[1]] == 0:
                            return
        if opponent == 1:
            self._game_state = "YELLOW_WON"
        else:
            self._game_state = "RED_WON"
        return

    def make_move(self, row_1, col_1, row_2, col_2):
        """Returns false if move invalid or game over; makes move and returns True if valid"""
        if not self._game_state == "UNFINISHED":
            return False
        if not self._is_valid_move(row_1, col_1, row_2, col_2):
            return False
        self._board[row_2][col_2] = self._board[row_1][col_1]
        self._board[row_1][col_1] = 0  # fixed -> forgot to change starting position to 0
        player = self._board[row_2][col_2]
        if player == 1:
            opponent = 2
        else:
            opponent = 1
        self._change_color(row_2, col_2, player, opponent)
        self._update_game_state(opponent)
        return True
