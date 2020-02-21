## @package Piece
#
# Contains Piece class.

## Object of class Piece is a piece on the chessboard.
# Every piece 'knows' where it can move, after calling update_moves().
# Pieces are moving themselves.


class Piece:
    def __init__(self, x, y, board):
        """
        The constructor of class Piece.
        :param x: Int. First starting coordinate on given board.
        :param y: Int. Second starting coordinate on given board.
        :param board: Object Board on which this piece will play.
        """
        ## int of value of this piece
        self.value = 0
        ## true if piece moved, false if it doesn't
        self.moved = False
        ## tuple of coordinates where this piece is at the board
        self._position = (x, y)
        ## set of all legal moves that this piece can do
        self.possible_moves = set()
        ## str of name of this piece
        self.name = '00'
        ## object Color that this piece is playing for
        self.my_color = None
        ## object Color that this piece is playing against
        self.enemy = None
        ## object Board on which this piece is playing
        self.my_board = board
        ## list of turns that this piece moved at
        self.moved_at = list()
        ## set of all legal beats in passing
        self.fly = set()
        ## str of length 2 with name and color of this piece
        self.print_name = '00'
        ## path to file with image to this piece
        self.img = None

    def get_current_position(self):
        """
        :return: Tuple. Tuple of 2 with current coordinates on the board.
        """
        return self._position

    def update_moves(self, turn):
        """
        Updating legal moves of this piece.
        :param turn: Int. Number of current turn.
        :return: None.
        """
        if self.my_color is not None:
            self.my_color.possible_attacks.pop(self, None)
            self.possible_moves.clear()

    def remove(self):
        """
        Removing this piece's legal attacks from all of it's Color possible attacks.
        :return: None.
        """
        if self.my_color is not None:
            self.my_color.possible_attacks.pop(self, None)

    def move(self, x, y, turn):
        """
        Changing attribute _positon if it's legal, adding value of taken opponent's piece and taking note of a move.
        :param x: Int. First board's coordinate of square that player want to move on.
        :param y: Int. Second board's coordinate of square that player want to move on.
        :param turn: Int. Number of current turn.
        :return: Boolean. True if move is legal, False if it isn't.
        """
        if (x, y) in self.possible_moves:
            self.my_color.points += self.my_board.get_board()[x][y].value
            self.my_board.get_board()[x][y].remove()
            self._position = (x, y)
            self.moved = True
            self.moved_at.append(turn)
            return True
        else:
            return False

    def set_enemy(self, color):
        """
        Setting attribute enemy.
        :param color: Color. Color of an enemy.
        :return:
        """
        self.enemy = color

    def castling(self, turn):
        """
        Doing castle.
        :param turn: Int. Number of current turn.
        :return:
        """
        return False

    def set_print_name(self):
        """
        Setting attribute print_name based on a attribute my_color.
        :return:
        """
        if self.my_color.color == 'white':
            self.print_name = '^'+self.name
        elif self.my_color.color == 'black':
            self.print_name = 'v'+self.name

    def set_position(self, x, y):
        """
        Setting _position to (x, y).
        :param x: Int. First board's coordinate of square that player want to move on.
        :param y: Int. Second board's coordinate of square that player want to move on.
        :return:
        """
        self._position = (x, y)
