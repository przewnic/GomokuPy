# Author: przewnic

from PyQt5.QtCore import QObject

from Player import Player


class Game(QObject):
    def __init__(self, board):
        self.players = (Player("white"), Player("black"))
        self.next_move = 0
        self.end = False
        self.board = board

    def reset(self):
        for player in self.players:
            player.performed_moves.clear()
        self.next_move = 0
        self.end = False

    def play(self):
        if self.check_win() or self.check_draw():
            return True
        self.change_player()

    def change_player(self):
        if self.next_move == 0:
            self.next_move = 1
            return
        self.next_move = 0

    def check_win(self):
        self.end = "Win"
        currnet_player = self.players[self.next_move]
        last_move = currnet_player.performed_moves[-1]
        to_check = []
        # Check horizontal
        checked = self.check_horizontal(last_move)
        to_check.append(checked)
        # Check vertical
        checked = self.check_vertical(last_move)
        to_check.append(checked)
        # Check diagonal
        checked = self.check_diagonal_lr(last_move)
        to_check.append(checked)
        # Check diagonal
        checked = self.check_diagonal_rl(last_move)
        to_check.append(checked)
        # Delete points beyond board
        for i, checked in enumerate(to_check):
            to_check[i] = [point for point in checked
                           if not self.board.is_beyond_board(*point)]
        # Check for win
        for checked in to_check:
            for i in range(len(checked) - 4):
                _checked = checked[i:5+i]
                if all([x in currnet_player.performed_moves for x in _checked]):
                    return True
        self.end = False
        return False

    def check_horizontal(self, last_move):
        f_size = self.board.field_size
        checked_left = [(last_move[0] - i*f_size, last_move[1])
                        for i in range(4, 0, -1)]
        checked_right = [(last_move[0] + i*f_size, last_move[1])
                         for i in range(1, 5)]
        return checked_left + [last_move] + checked_right

    def check_vertical(self, last_move):
        f_size = self.board.field_size
        checked_up = [(last_move[0], last_move[1] - i*f_size)
                      for i in range(4, 0, -1)]
        checked_down = [(last_move[0], last_move[1] + i*f_size)
                        for i in range(1, 5)]
        return checked_up + [last_move] + checked_down

    def check_diagonal_lr(self, last_move):
        f_size = self.board.field_size
        checked_up_l = [(last_move[0] - i*f_size, last_move[1] - i*f_size)
                        for i in range(4, 0, -1)]
        checked_down_r = [(last_move[0] + i*f_size, last_move[1] + i*f_size)
                          for i in range(1, 5)]
        return checked_up_l + [last_move] + checked_down_r

    def check_diagonal_rl(self, last_move):
        f_size = self.board.field_size
        checked_up_r = [(last_move[0] + (4-i)*f_size, last_move[1] - (4-i)*f_size)
                        for i in range(4)]
        checked_down_l = [(last_move[0] - i*f_size, last_move[1] + i*f_size)
                          for i in range(1, 5)]
        return checked_up_r + [last_move] + checked_down_l

    def check_draw(self):
        """ Check if all fields are taken. """
        nr_of_fields = 225
        if len(self.players[0].performed_moves) +\
                len(self.players[1].performed_moves) == nr_of_fields:
            self.end = "Draw"
            return True
        return False
