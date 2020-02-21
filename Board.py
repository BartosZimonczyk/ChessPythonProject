from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook
from Piece import Piece
from King import King

## @package Board
#
# Contains Board class.

## Object of class Board are esentially matrices 8x8 with elements of class Piece.
# Any action done by a player in game has to be done by methods of ths class.
# Boards can check themselves to find a check, check mate or pat situation.


class Board:
    def __init__(self, white, black, board=None):
        """
        The constructor of class Board.
        :param white: object Color. Player playing with white pieces.
        :param black: object Color. Player playing with black pieces
        :param board: matrix 8x8 or None. If given matrix it builds boards according to given matrix.
        """
        ## matrix 8x8 with elements of class Piece
        self._board = board if board is not None else [[Piece(i, j, self) for i in range(8)] for j in range(8)]
        ## object Color according to player playing with white pieces
        self.white_player = white
        ## object Color according to player playing with black pieces
        self.black_player = black
        ## int of number of turns
        self.turn = 0

    def add_pieces(self, pieces):
        """
        Adding pieces to a board and setting their attributes.
        :param pieces: List. List of a pieces to add to a board.
        :return:
        """
        for piece in pieces:
            x = piece.get_current_position()[0]
            y = piece.get_current_position()[1]
            piece.set_print_name()
            if piece.my_color.color == 'white':
                piece.set_enemy(self.black_player)
            elif piece.my_color.color == 'black':
                piece.set_enemy(self.white_player)
            self._board[x][y] = piece

    def move_piece(self, x1, y1, x2, y2, sym=False):
        """
        Moving piece on a board. If x2=='c' and y2=='a' then castling.
        :param x1: Int. First board's coordinate of piece player want to move.
        :param y1: Int. Second board's coordinate of piece player want to move.
        :param x2: Int. First board's coordinate of square that player want to move on.
        :param y2: Int. Second board's coordinate of square that player want to move on.
        :param sym: Boolean. Declaring if this function is called in simulation (default: False).
        :return: Boolean. True if move has been done, or false if hasn't.
        """
        if x2 + y2 == 'ca':
            return self.castling(x1, y1, self.turn)
        elif self._board[x1][y1].move(x2, y2, self.turn):
            self._board[x2][y2] = self._board[x1][y1]
            self._board[x1][y1] = Piece(x1, y1, self)
            if isinstance(self._board[x2][y2], Pawn):
                if (x2, y2) in self._board[x2][y2].fly:
                    self._board[x2][y2-1] = Piece(x2, y2-1, self)
            if isinstance(self._board[x2][y2], Pawn) and (y2 == 0 or y2 == 7) and not sym:
                self.evolve(x2, y2)

            return True
        else:
            return False

    def is_check(self):
        """
        Checking if king is in check.
        :return: Boolean. True if king is in check, False if it isn't.
        """
        n = self.turn % 2
        king = self.white_player.my_king if n == 1 else self.black_player.my_king
        # print(king.enemy.all_attacks(), king.get_current_position())
        if king.get_current_position() in king.enemy.all_attacks():
            return True
        else:
            return False

    def is_castling_possible(self, x1, y1):
        """
        Checking if castle for given Piece at position x1, y1 is possible.
        :param x1: Int. First board's coordinate of Rook player want to castle.
        :param y1: Int. Second board's coordinate of Rook player want to castle.
        :return: Boolean. True if castle can be done.
        """
        if isinstance(self._board[x1][y1], Rook):
            if self._board[x1][y1].my_color.color == 'white':
                if (x1, y1) == (0, 0):
                    if self.black_player.all_attacks().isdisjoint({(3, 0), (2, 0), (1, 0)}):
                        if self._board[1][0].my_color is None and self._board[2][0].my_color is None:
                            if not self._board[3][0].moved and isinstance(self._board[3][0], King):
                                return True
                elif (x1, y1) == (7, 0):
                    if self.black_player.all_attacks().isdisjoint({(3, 0), (4, 0), (5, 0)}):
                        if self._board[4][0].my_color is None and self._board[5][0].my_color is None and self._board[6][0].my_color is None:
                            if not self._board[3][0].moved and isinstance(self._board[3][0], King):
                                return True
            elif self._board[x1][y1].my_color.color == 'black':
                if (x1, y1) == (0, 7):
                    if self.white_player.all_attacks().isdisjoint({(3, 7), (2, 7), (1, 7)}):
                        if self._board[1][7].my_color is None and self._board[2][7].my_color is None:
                            if not self._board[3][7].moved and isinstance(self._board[3][7], King):
                                return True
                elif (x1, y1) == (7, 7):
                    if self.white_player.all_attacks().isdisjoint({(3, 7), (4, 7), (5, 7)}):
                        if self._board[4][7].my_color is None and self._board[5][7].my_color is None and self._board[6][7].my_color is None:
                            if not self._board[3][7].moved and isinstance(self._board[3][7], King):
                                return True
        return False

    def castling(self, x1, y1, turn):
        """
        Doing castle if it is possible for given Piece at position x1, y1.
        :param x1: Int. First board's coordinate of Rook player want to castle.
        :param y1: Int. Second board's coordinate of Rook player want to castle.
        :param turn: Int. Number of current turn.
        :return: Boolean. True if castle has been done, False if it hasn't.
        """
        if isinstance(self._board[x1][y1], Rook):
            if self._board[x1][y1].my_color.color == 'white':
                if (x1, y1) == (0, 0):
                    if self.black_player.all_attacks().isdisjoint({(3, 0), (2, 0), (1, 0)}):
                        if self._board[1][0].my_color is None and self._board[2][0].my_color is None:
                            if self._board[x1][y1].castling(turn):
                                self._board[2][0], self._board[x1][y1] = self._board[x1][y1], self._board[2][0]
                                self._board[1][0], self._board[3][0] = self._board[3][0], self._board[1][0]
                                return True
                            else:
                                print('Improper move! Do something else!')
                                return False
                        else:
                            print('Improper move! Do something else!')
                            return False
                    print('Improper move! Do something else!')
                    return False
                elif (x1, y1) == (7, 0):
                    if self.black_player.all_attacks().isdisjoint({(3, 0), (4, 0), (5, 0)}):
                        if self._board[4][0].my_color is None and self._board[5][0].my_color is None \
                                and self._board[6][0].my_color is None:
                            if self._board[x1][y1].castling(turn):
                                self._board[4][0], self._board[x1][y1] = self._board[x1][y1], self._board[4][0]
                                self._board[5][0], self._board[3][0] = self._board[3][0], self._board[5][0]
                                return True
                            else:
                                print('Improper move! Do something else!')
                                return False
                        else:
                            print('Improper move! Do something else!')
                            return False
                    else:
                        print('Improper move! Do something else!')
                        return False
            elif self._board[x1][y1].my_color.color == 'black':
                if (x1, y1) == (0, 7):
                    if self.white_player.all_attacks().isdisjoint({(3, 7), (2, 7), (1, 7)}):
                        if self._board[1][7].my_color is None and self._board[2][7].my_color is None:
                            if self._board[x1][y1].castling(turn):
                                self._board[2][7], self._board[x1][y1] = self._board[x1][y1], self._board[2][7]
                                self._board[1][7], self._board[3][7] = self._board[3][7], self._board[1][7]
                                return True
                            else:
                                print('Improper move! Do something else!')
                                return False
                        else:
                            print('Improper move! Do something else!')
                            return False
                    else:
                        print('Improper move! Do something else!')
                        return False
                elif (x1, y1) == (7, 7):
                    if self.white_player.all_attacks().isdisjoint({(3, 7), (4, 7), (5, 7)}):
                        if self._board[4][7].my_color is None and self._board[5][7].my_color is None\
                                and self._board[6][7].my_color is None:
                            if self._board[x1][y1].castling(turn):
                                self._board[4][7], self._board[x1][y1] = self._board[x1][y1], self._board[4][7]
                                self._board[5][7], self._board[3][7] = self._board[3][7], self._board[5][7]
                                return True
                            else:
                                print('Improper move! Do something else!')
                                return False
                        else:
                            print('Improper move! Do something else!')
                            return False
                    else:
                        print('Improper move! Do something else!')
                        return False
        else:
            print('Improper move! Do something else!')
            return False

    def get_board(self):
        """
        :return: List 8x8. Matrix of all Pieces on the board.
        """
        return self._board

    def evolve(self, x, y):
        """
        Evolving Pawn into Knight, Bishop, Rook or Queen on position x, y.
        :param x: Int. First board's coordinate on which Pawn is evolving.
        :param y: Int. Second board's coordinate on which Pawn is evolving.
        :return: None.
        """
        pawn = self.get_board()[x][y]
        color = pawn.my_color
        text = 'Pick one of: Knight, Bishop, Rook, Queen\n'
        figure = input(text+'Select a figure:')
        while figure not in {'Knight', 'Bishop', 'Rook', 'Queen'}:
            figure = input(text+'Select proper figure:')
        color.my_pawns.remove(pawn)
        if figure == 'Knight':
            self._board[x][y] = Knight(x, y, self)
            self._board[x][y].my_color = color
            color.my_knights.append(self._board[x][y])
        elif figure == 'Bishop':
            self._board[x][y] = Bishop(x, y, self)
            self._board[x][y].my_color = color
            color.my_bishops.append(self._board[x][y])
        elif figure == 'Rook':
            self._board[x][y] = Rook(x, y, self)
            self._board[x][y].my_color = color
            color.my_rooks.append(self._board[x][y])
        elif figure == 'Queen':
            self._board[x][y] = Queen(x, y, self)
            self._board[x][y].my_color = color
            color.my_queens.append(self._board[x][y])
        color.set_starting_pieces()
        self._board[x][y].set_print_name()
        self._board[x][y].img = './ChessArt/' + self._board[x][y].my_color.color[0].upper() + self._board[x][y].name + '.png'

    def check_mate(self):
        """
        Checking if there is check mate on the board.
        :return: Tuple of Boolean and string. True if there is, False if there isn't. Str of color which won the game.
        """
        if self.is_check():
            white = set()
            black = set()
            for i in range(8):
                for j in range(8):
                    piece = self._board[i][j]
                    if piece.my_color is not None:
                        if piece.my_color.color == 'white':
                            white.update(piece.possible_moves)
                        elif piece.my_color.color == 'black':
                            black.update(piece.possible_moves)
            if white == set() and self.turn % 2 == 1:
                return True, 'Black'
            if black == set() and self.turn % 2 == 0:
                return True, 'White'
        return False, None

    def is_pat(self):
        """
        Checking if there is pat by no possible moves for one color on the board.
        :return: Boolean. True if there is, False if there isn't.
        """
        if not self.is_check():
            white = set()
            black = set()
            for i in range(8):
                for j in range(8):
                    piece = self._board[i][j]
                    if piece.my_color is not None:
                        if piece.my_color.color == 'white':
                            white.update(piece.possible_moves)
                        elif piece.my_color.color == 'black':
                            black.update(piece.possible_moves)
            if white == set() and self.turn % 2 == 1:
                return True
            if black == set() and self.turn % 2 == 0:
                return True
        return False

    def update_all(self):
        """
        Updating moves of all pieces on the board.
        :return:
        """
        for i in range(8):
            for j in range(8):
                self._board[i][j].update_moves(self.turn)

    def __str__(self):
        """
        :return: Str of current position on the board with information of check, pat and mat.
        """
        ret = ' A  B  C  D  E  F  G  H\n -----------------------\n'
        for i in range(8):
            ret += ' '
            for j in range(8):
                ret += self._board[7-j][7-i].print_name
                ret += ' '
            ret += '|'+str(8-i)
            if i != 2 and i != 4 and i != 0 and i != 6:
                ret += '\n'
            elif i == 2:
                ret += '\t\tWhite\'s points: {}\n'.format(self.white_player.points)
            elif i == 4:
                ret += '\t\tBlack\'s points: {}\n'.format(self.black_player.points)
            elif i == 0:
                if self.turn % 2 == 1:
                    ret += '\t\tWhite\'s turn({})\n'.format(self.turn)
                else:
                    ret += '\t\tBlack\'s turn({})\n'.format(self.turn)
            elif i == 6:
                if self.is_check():
                    ret += '\t\tCheck!\n'
                elif self.is_pat():
                    ret += '\t\tPat!\n'
                elif self.check_mate()[0]:
                    ret += '\t\tCheck mate!\n'
                else:
                    ret += '\n'
            elif i == 7:
                if self.check_mate()[0]:
                    ret += '\t\t{} won!'.format(self.check_mate()[1])

        return ret
