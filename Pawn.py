from Piece import Piece

## @package Pawn
#
# Contains Pawn class.

## Object of class Pawn is object of class Piece with restricted legal moves
# to pawn's moves.


class Pawn(Piece):
    def __init__(self, x, y, board):
        """
        The constructor of class Pawn, subclass of Piece.
        Changing attribute name and value.
        :param x: Int. First starting coordinate on given board.
        :param y: Int. Second starting coordinate on given board.
        :param board: Object Board on which this piece will play.
        """
        super().__init__(x, y, board)
        ## str of name of this piece
        self.name = '.'
        ## int of value of this piece
        self.value = 1

    def update_moves(self, turn):
        """
        Updating legal moves of this piece.
        :param turn: Int. Number of current turn.
        :return: None.
        """
        super().update_moves(turn)

        i, j = self.get_current_position()

        if not self.moved and self.my_board.get_board()[i][j+2*self.my_color.direction].my_color is None:
            self.possible_moves.add((i, j+2*self.my_color.direction))

        if 0 <= j+self.my_color.direction < 8:
            if self.my_board.get_board()[i][j+self.my_color.direction].my_color is None:
                self.possible_moves.add((i, j+self.my_color.direction))

        if 0 <= i - 1 < 8 and 0 <= j+self.my_color.direction < 8:
            if self.my_board.get_board()[i-1][j+self.my_color.direction].my_color is not None:
                if self.my_board.get_board()[i-1][j+self.my_color.direction].my_color != self.my_color:
                    self.possible_moves.add((i-1, j+self.my_color.direction))
                    self.my_color.possible_attacks.update(self.possible_moves)

        if 0 <= i + 1 < 8 and 0 <= j+self.my_color.direction < 8:
            if self.my_board.get_board()[i+1][j+self.my_color.direction].my_color is not None:
                if self.my_board.get_board()[i+1][j+self.my_color.direction].my_color != self.my_color:
                    self.possible_moves.add((i+1, j+self.my_color.direction))
                    self.my_color.possible_attacks.update(self.possible_moves)

        if 0 <= i - 1 < 8 and (j == 3 or j == 4):
            if self.my_board.get_board()[i-1][j+self.my_color.direction].my_color is None:
                if self.my_board.get_board()[i-1][j].my_color is not None:
                    if isinstance(self.my_board.get_board()[i-1][j], Pawn):
                        if self.my_board.get_board()[i-1][j].my_color != self.my_color:
                            if self.my_board.get_board()[i-1][j].moved_at[0] == turn - 1:
                                self.possible_moves.add((i-1, j+self.my_color.direction))
                                self.fly.add((i-1, j+self.my_color.direction))

        if 0 <= i + 1 < 8 and (j == 3 or j == 4):
            if self.my_board.get_board()[i+1][j+self.my_color.direction].my_color is None:
                if self.my_board.get_board()[i+1][j].my_color is not None:
                    if isinstance(self.my_board.get_board()[i+1][j], Pawn):
                        if self.my_board.get_board()[i+1][j].my_color != self.my_color:
                            if self.my_board.get_board()[i+1][j].moved_at[0] == turn - 1:
                                self.possible_moves.add((i+1, j+self.my_color.direction))
                                self.fly.add((i + 1, j + self.my_color.direction))

        self.my_color.possible_attacks[self] = set()
        if i < 7:
            self.my_color.possible_attacks[self] |= {(i-1, j+self.my_color.direction)}
        if i > 0:
            self.my_color.possible_attacks[self] |= {(i+1, j+self.my_color.direction)}
