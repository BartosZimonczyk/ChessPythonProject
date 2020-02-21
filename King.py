from Piece import Piece

## @package King
#
# Contains King class.

## Object of class King is object of class Piece with restricted legal moves
# to king's moves.


class King(Piece):
    def __init__(self, x, y, board):
        """
        The constructor of class King, subclass of Piece.
        Changing attribute name and value.
        :param x: Int. First starting coordinate on given board.
        :param y: Int. Second starting coordinate on given board.
        :param board: Object Board on which this piece will play.
        """
        super().__init__(x, y, board)
        ## str of name of this piece
        self.name = 'K'
        ## int of value of this piece
        self.value = 100

    def update_moves(self, turn):
        """
        Updating legal moves of this piece.
        :param turn: Int. Number of current turn.
        :return: None.
        """
        super().update_moves(turn)
        i, j = self.get_current_position()

        if 0 <= i-1 < 8 and 0 <= j-1 < 8:
            if not self.my_board.get_board()[i-1][j-1].my_color == self.my_color:
                self.possible_moves.add((i-1, j-1))

        if 0 <= i-1 < 8 and 0 <= j+1 < 8:
            if not self.my_board.get_board()[i-1][j+1].my_color == self.my_color:
                self.possible_moves.add((i-1, j+1))

        if 0 <= i+1 < 8 and 0 <= j-1 < 8:
            if not self.my_board.get_board()[i+1][j-1].my_color == self.my_color:
                self.possible_moves.add((i+1, j-1))

        if 0 <= i+1 < 8 and 0 <= j+1 < 8:
            if not self.my_board.get_board()[i+1][j+1].my_color == self.my_color:
                self.possible_moves.add((i+1, j+1))

        if 0 <= i-1 < 8:
            if not self.my_board.get_board()[i-1][j].my_color == self.my_color:
                self.possible_moves.add((i-1, j))

        if 0 <= j+1 < 8:
            if not self.my_board.get_board()[i][j+1].my_color == self.my_color:
                self.possible_moves.add((i, j+1))

        if 0 <= i+1 < 8:
            if not self.my_board.get_board()[i+1][j].my_color == self.my_color:
                self.possible_moves.add((i+1, j))

        if 0 <= j-1 < 8:
            if not self.my_board.get_board()[i][j-1].my_color == self.my_color:
                self.possible_moves.add((i, j-1))

        x, y = self.enemy.my_king.get_current_position()
        self.possible_moves -= {(x+1, y+1), (x+1, y), (x+1, y-1),
                                (x, y+1), (x, y), (x, y-1),
                                (x-1, y+1), (x-1, y), (x-1, y-1)}

        self.my_color.possible_attacks[self] = self.possible_moves
