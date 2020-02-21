from Piece import Piece\

## @package Bishop
#
# Contains Bishop class.

## Object of class Bishop is object of class Piece with restricted legal moves
# to bishop's moves.


class Bishop(Piece):
    def __init__(self, x, y, board):
        """
        The constructor of class Queen, subclass of Piece.
        Changing attribute name and value.
        :param x: Int. First starting coordinate on given board.
        :param y: Int. Second starting coordinate on given board.
        :param board: Object Board on which this piece will play.
        """
        super().__init__(x, y, board)
        ## str of name of this piece
        self.name = 'B'
        ## int of value of this piece
        self.value = 3

    def update_moves(self, turn):
        """
        Updating legal moves of this piece.
        :param turn: Int. Number of current turn.
        :return: None.
        """
        super().update_moves(turn)
        i, j = self.get_current_position()
        i, j = i - 1, j - 1
        while 0 <= i < 8 and 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i, j = i - 1, j - 1

        i, j = self.get_current_position()
        i, j = i - 1, j + 1
        while 0 <= i < 8 and 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i, j = i - 1, j + 1

        i, j = self.get_current_position()
        i, j = i + 1, j - 1
        while 0 <= i < 8 and 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i, j = i + 1, j - 1

        i, j = self.get_current_position()
        i, j = i + 1, j + 1
        while 0 <= i < 8 and 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i, j = i + 1, j + 1

        self.my_color.possible_attacks[self] = self.possible_moves
