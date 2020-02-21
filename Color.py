from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook

## @package Color
#
# Contains Color class.

## Objects of this class can be identify with players playing the game.
# There are essentially 2 types of this class. One with attribute color == 'white'
# and color == 'black' which defines position of pieces.


class Color:
    def __init__(self, color):
        """
        The constructor of class Color.
        :param color: Str with value 'black' or 'white'.
        """
        ## str with value 'black' or 'white'
        self.color = color
        ## int of number of points that this player has
        self.points = 0
        ## int of second coordinate on board where this color pawns starts
        self.y = None
        ## int, value of which second coordinate of pawns should change when moved
        self.direction = None
        if color == 'white':
            self.y = 0
            self.direction = 1
        elif color == 'black':
            self.y = 7
            self.direction = -1
        else:
            raise ValueError('Pick white or black color')
        ## dict of all possible attacks that piece in key can do
        self.possible_attacks = dict()
        ## list of objects Pawn of this color
        self.my_pawns = list()
        ## object King of this color
        self.my_king = None
        ## list of objects Queen of this color
        self.my_queens = list()
        ## list of objects Bishop of this color
        self.my_bishops = list()
        ## list of objects Rook of this color
        self.my_rooks = list()
        ## list of objects Knight of this color
        self.my_knights = list()
        ## list of objects Piece of this color
        self.starting_pieces = list()

    def set_pieces(self, board):
        """
        Pairing this Color's pieces on Board.
        :param board: Board. Board with which pieces will be paired with.
        :return: None.
        """
        self.my_pawns = [Pawn(i, self.y + self.direction, board) for i in range(8)]
        self.my_bishops = [Bishop(2, self.y, board), Bishop(5, self.y, board)]
        self.my_knights = [Knight(1, self.y, board), Knight(6, self.y, board)]
        self.my_rooks = [Rook(0, self.y, board), Rook(7, self.y, board)]
        self.my_queens = [Queen(4, self.y, board)]
        self.my_king = King(3, self.y, board)
        self.set_starting_pieces()
        for piece in self.starting_pieces:
            piece.my_board = board
            piece.my_color = self
            piece.img = './ChessArt/'+self.color[0].upper()+piece.name+'.png'
        board.add_pieces(self.starting_pieces)

    def set_starting_pieces(self):
        """
        Setting attribute starting_pieces.
        :return:
        """
        self.starting_pieces = self.my_bishops + [
            self.my_king] + self.my_knights + self.my_pawns + self.my_queens + self.my_rooks

    def all_attacks(self):
        """
        :return: Set. Set of all possible attacks on the board by this Color.
        """
        ret = set()
        for attack in self.possible_attacks.values():
            if isinstance(attack, set):
                ret.update(attack)
        return ret

    def __eq__(self, other):
        """
        :param other: Object Color.
        :return: True if objects are equal, False if they don't.
        """
        if other is None:
            return False
        return self.color == other.color
