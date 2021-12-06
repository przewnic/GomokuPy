from PyQt5 import QtWidgets, uic

# Author: przewnic

from Board import Board
from Game import Game
from MyGraphicsScene import MyGraphicsScene


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main.ui', self)
        self.setWindowTitle("Gomoku")
        self.scene = MyGraphicsScene(None)
        self.graphics_view.setScene(self.scene)

        self.scene.mouse_released_pos.connect(self.on_released)
        self.scene.mouse_hover_pos.connect(self.on_hover)

        self.board = Board()
        self.board.draw_board(self.scene)
        f_size = self.board.field_size
        size_x = self.board.size["height"] + f_size
        size_y = self.board.size["height"] + f_size
        self.scene.setSceneRect(-f_size//2, -f_size//2, size_x, size_y)
        self.game = Game(self.board)

        self.restart.clicked.connect(self.on_restart)
        self.hover_item = None
        self.on_restart()

    def on_released(self, position):
        self.remove_hover_item()
        if self.game.end:
            return
        x, y = position.x(), position.y()
        # Check if clicked beyond board
        if self.board.is_beyond_board(x, y):
            return
        x, y = abs(x), abs(y)
        # Get board coordinates
        point_x, point_y = self.get_board_coordinates(x, y)
        # Check if field empty
        if self.is_field_empty((point_x, point_y)):
            return
        # Adjust coordinates for drawing
        draw_x = point_x - self.board.point_size//2
        draw_y = point_y - self.board.point_size//2
        # Get player and add new move
        currnet_player = self.game.players[self.game.next_move]
        currnet_player.performed_moves.append((point_x, point_y))
        # Draw new point on board
        color = currnet_player.color
        item = self.board.draw_point(draw_x, draw_y, color, self.scene)
        self.board.points.append(item)
        # Check winner or prepare for next move
        if self.game.play():
            self.set_winner(currnet_player)
            return
        # Set next player
        self.set_move(self.game.players[self.game.next_move])

    def get_board_coordinates(self, x, y):
        """ Adjust coordinates. """
        point_x = (x // self.board.field_size)*self.board.field_size
        point_y = (y // self.board.field_size)*self.board.field_size
        if (x - point_x)/self.board.field_size > 0.5:
            point_x += self.board.field_size
        if (y - point_y)/self.board.field_size > 0.5:
            point_y += self.board.field_size
        return point_x, point_y

    def on_hover(self, position):
        self.remove_hover_item()
        if self.game.end:
            return
        x, y = position.x(), position.y()
        # Check if clicked beyond board
        if self.board.is_beyond_board(x, y):
            return
        x, y = abs(x), abs(y)
        # Get board coordinates
        point_x, point_y = self.get_board_coordinates(x, y)
        # Check if field empty
        if self.is_field_empty((point_x, point_y)):
            return
        # Adjust coordinates for drawing
        draw_x = point_x - self.board.point_size//2
        draw_y = point_y - self.board.point_size//2
        currnet_player = self.game.players[self.game.next_move]
        color = currnet_player.color
        self.hover_item = self.board.draw_point(
            draw_x, draw_y, color, self.scene)

    def is_field_empty(self, position):
        for player in self.game.players:
            if position in player.performed_moves:
                return True
        return False

    def remove_hover_item(self):
        if self.hover_item:
            self.scene.removeItem(self.hover_item)
        self.hover_item = None

    def set_winner(self, winning_player):
        if self.game.end == "Win":
            self.winner.setText(winning_player.color.title())
        if self.game.end == "Draw":
            self.winner.setText("Draw")
        self.move.setText("")

    def set_move(self, currnet_player):
        self.move.setText(currnet_player.color.title())

    def on_restart(self):
        self.winner.setText("")
        # Clear board
        for item in self.board.points:
            self.scene.removeItem(item)
        self.board.points.clear()
        # Reset the game
        self.game.reset()
        # Set next player
        self.set_move(self.game.players[self.game.next_move])
