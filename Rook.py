from Piece import Piece
from King import King

## @package Rook
#
# Contains Rook class.

## Object of class Rook is object of class Piece with restricted legal moves
# to rook's moves and can do a castling with object class King.


class Rook(Piece):
    def __init__(self, x, y, board):
        """
        The constructor of class Rook, subclass of Piece.
        Changing attribute name and value.
        :param x: Int. First starting coordinate on given board.
        :param y: Int. Second starting coordinate on given board.
        :param board: Object Board on which this piece will play.
        """
        super().__init__(x, y, board)
        ## str of name of this piece
        self.name = 'R'
        ## int of value of this piece
        self.value = 5

    def update_moves(self, turn):
        """
        Updating legal moves of this piece.
        :param turn: Int. Number of current turn.
        :return: None.
        """
        super().update_moves(turn)
        i, j = self.get_current_position()
        i = i - 1
        while 0 <= i < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i = i - 1

        i, j = self.get_current_position()
        j = j - 1
        while 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            j = j - 1

        i, j = self.get_current_position()
        i = i + 1
        while 0 <= i < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            i = i + 1

        i, j = self.get_current_position()
        j = j + 1
        while 0 <= j < 8:
            if self.my_board.get_board()[i][j].my_color is not None:
                if self.my_board.get_board()[i][j].my_color == self.my_color:
                    break
                else:
                    self.possible_moves.add((i, j))
                    break
            self.possible_moves.add((i, j))
            j = j + 1

        i, j = self.get_current_position()
        if self.my_board.is_castling_possible(i, j):
            if self.my_color.color == 'white':
                self.possible_moves.add((3, 0))
            elif self.my_color.color == 'black':
                self.possible_moves.add((3, 7))

        self.my_color.possible_attacks[self] = self.possible_moves

    def castling(self, turn):
        if not self.moved and self.my_color.color == 'white':
            king = self.my_board.get_board()[3][0]
            if not isinstance(king, King):
                return False
            if not king.moved:
                if self.get_current_position() == (0, 0):
                    self.set_position(2, 0)
                    king.set_position(1, 0)
                    self.moved = True
                    king.moved = True
                    return True
                elif self.get_current_position() == (7, 0):
                    self.set_position(4, 0)
                    king.set_position(5, 0)
                    self.moved = True
                    king.moved = True
                    return True
            else:
                return False
        elif not self.moved and self.my_color.color == 'black':
            king = self.my_board.get_board()[3][7]
            if not isinstance(king, King):
                return False
            if not king.moved:
                if self.get_current_position() == (0, 7):
                    self.set_position(2, 7)
                    king.set_position(1, 7)
                    self.moved = True
                    king.moved = True
                    return True
                elif self.get_current_position() == (7, 7):
                    self.set_position(4, 7)
                    king.set_position(5, 7)
                    self.moved = True
                    king.moved = True
                    return True
            else:
                return False
        else:
            return False
