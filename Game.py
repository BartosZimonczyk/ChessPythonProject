#!/usr/bin/env python
from Color import Color
from Board import Board
from copy import deepcopy
from os import system, name
from time import sleep
from Rook import Rook
from King import King
import pygame
import math

## @package Game
#
# Contains Game class and starting visual_game() in __main__.

## Objects of this class are games themselves.
# There is no need to make another objects to run the game, all of this
# is done by console_game() for console printed game or by
# visual_game() for windowed game with graphics.


class Game:
    def __init__(self):
        """
        The constructor of class Game.
        """
        ## object Color according to player playing with white pieces
        self.white_player = Color('white')
        ## object Color according to player playing with black pieces
        self.black_player = Color('black')
        ## object Board on which game is played
        self.current_board = Board(self.white_player, self.black_player)
        self.white_player.set_pieces(self.current_board)
        self.black_player.set_pieces(self.current_board)
        ## int of number of turns
        self.turn = 0
        ## dict of letters assigned with numbers
        self._letters = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
        ## inverse of _letters
        self._numbers = {v: k for k, v in self._letters.items()}
        ## set of all possible commands that players can input
        self._possible_commands = {k+str(v) for k in self._letters.keys() for v in self._letters.values()}
        self._possible_commands.update({'ff', 'ca'})
        ## copy of current_board
        self.last_board = None
        ## object Surface on which game is drawn
        self.gameDisplay = None
        ## constant value of height of gameDisplay
        self.HEIGHT = 675
        ## constant value of width of gameDisplay
        self.WIDTH = math.floor(self.HEIGHT*1.5)
        ## constant value of size of one drawn block on gameDisplay
        self.BLOCK_SIZE = math.floor(self.HEIGHT/9)
        ## constant value of black color in RGB representation
        self.BLACK = (70, 70, 70)
        ## constant value of white color in RGB representation
        self.WHITE = (255, 255, 255)
        ## constant value of green color in RGB representation
        self.GREEN = (50, 200, 50)
        ## constant value of red color in RGB representation
        self.RED = (200, 50, 50)
        ## constant value of background color in RGB representation
        self.BACKGROUND = (200, 230, 220)
        ## constant value of font color in RGB representation
        self.FONT_COLOR = (10, 10, 50)
        ## constant value of font size
        self.FONT_SIZE = math.floor(self.BLOCK_SIZE*0.3)
        ## object Clock that tracks amount of time and control a game's framrate
        self.clock = pygame.time.Clock()
        ## tuple of coordinates picked by a player in graphic mode
        self.memory = None
        ## object Font of font used in graphic mode
        self.font = None

    def draw_board(self):
        """
        Drawing board on the graphic version of game.
        :return:
        """
        pygame.draw.rect(self.gameDisplay, self.BACKGROUND, [0, 0, self.WIDTH, self.HEIGHT])
        for y in range(9):
            for x in range(9):
                if x < 8 and y < 8:
                    color = self.WHITE if (y+x) % 2 == 0 else self.BLACK
                    rect = [x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE]
                    pygame.draw.rect(self.gameDisplay, color, rect)
                if x == 8 and y < 8:
                    digit = self.font.render('{}'.format(8-y), True, self.FONT_COLOR)
                    rect_digit = digit.get_rect()
                    rect_digit.center = (math.floor(x*self.BLOCK_SIZE + self.BLOCK_SIZE/2),
                                         math.floor(y*self.BLOCK_SIZE + self.BLOCK_SIZE/2))
                    self.gameDisplay.blit(digit, rect_digit)
                if y == 8 and x < 8:
                    digit = self.font.render('{}'.format(self._numbers[x+1]), True, self.FONT_COLOR)
                    rect_digit = digit.get_rect()
                    rect_digit.center = (math.floor(x * self.BLOCK_SIZE + self.BLOCK_SIZE / 2),
                                         math.floor(y * self.BLOCK_SIZE + self.BLOCK_SIZE / 2))
                    self.gameDisplay.blit(digit, rect_digit)

        for i in range(8):
            for j in range(8):
                piece = self.current_board.get_board()[7-i][7-j]
                if piece.my_color is not None:
                    img = pygame.image.load(piece.img)
                    img = pygame.transform.scale(img, (self.BLOCK_SIZE, self.BLOCK_SIZE))
                    self.gameDisplay.blit(img, (i * self.BLOCK_SIZE, j * self.BLOCK_SIZE))
        pygame.display.update()
        self.draw_menu()

    def draw_menu(self):
        """
        Drawing menu on the graphic version of game.
        :return:
        """
        pygame.draw.rect(self.gameDisplay, self.BACKGROUND, [self.HEIGHT, math.floor(self.HEIGHT/4),
                                                             math.floor(self.HEIGHT/2), self.WIDTH-self.HEIGHT])
        pygame.display.update()

        if self.turn % 2 == 1:
            whose_turn = self.font.render('White\'s turn({})'.format(self.turn), True, self.FONT_COLOR)
        else:
            whose_turn = self.font.render('Black\'s turn({})'.format(self.turn), True, self.FONT_COLOR)
        rect_whose_turn = whose_turn.get_rect()
        rect_whose_turn.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 2*self.BLOCK_SIZE+self.FONT_SIZE)
        self.gameDisplay.blit(whose_turn, rect_whose_turn)

        white_points = self.font.render('White\'s points: {}'.format(self.white_player.points), True, self.FONT_COLOR)
        black_points = self.font.render('Black\'s points: {}'.format(self.black_player.points), True, self.FONT_COLOR)
        rect_w_points = white_points.get_rect()
        rect_b_points = black_points.get_rect()
        rect_w_points.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 3*self.BLOCK_SIZE+self.FONT_SIZE)
        rect_b_points.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 4*self.BLOCK_SIZE+self.FONT_SIZE)
        self.gameDisplay.blit(white_points, rect_w_points)
        self.gameDisplay.blit(black_points, rect_b_points)

        if self.current_board.check_mate()[0]:
            check = self.font.render('Check mate!', True, self.FONT_COLOR)
            rect = check.get_rect()
            rect.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 5*self.BLOCK_SIZE+self.FONT_SIZE)
            self.gameDisplay.blit(check, rect)
            who = self.font.render('{} won!'.format(self.current_board.check_mate()[1]), True, self.FONT_COLOR)
            rect = who.get_rect()
            rect.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 5*self.BLOCK_SIZE + 2*self.FONT_SIZE + 5)
            self.gameDisplay.blit(who, rect)
        elif self.current_board.is_check():
            check = self.font.render('Check!', True, self.FONT_COLOR)
            rect = check.get_rect()
            rect.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 5*self.BLOCK_SIZE + self.FONT_SIZE)
            self.gameDisplay.blit(check, rect)
        elif self.current_board.is_pat() and self.turn != 1:
            pat = self.font.render('Draw!', True, self.FONT_COLOR)
            rect = pat.get_rect()
            rect.center = (math.floor(self.HEIGHT + (self.WIDTH - self.HEIGHT)/2), 5*self.BLOCK_SIZE + self.FONT_SIZE)
            self.gameDisplay.blit(pat, rect)

    def visual_game(self):
        """
        Taking my chess to the new level. NOW WITH GRAPHICS.
        Making window display for a game in which the game is running.
        :return:
        """
        self.turn += 1
        self.current_board.turn += 1
        pygame.init()
        self.font = pygame.font.Font('TypewriterScribbled.ttf', self.FONT_SIZE)
        self.gameDisplay = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Chess by Bartosz Zimonczyk')
        self.gameDisplay.fill(self.BACKGROUND)
        self.draw_board()
        quit_game = False
        self.clear()
        self.print_board()
        self.last_board = self.current_board
        self.update_moves_for_check()
        while not quit_game:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and not self.current_board.check_mate()[0] and not self.current_board.is_pat():
                    if event.pos[0] < 8*self.BLOCK_SIZE and event.pos[1] < 8*self.BLOCK_SIZE:
                        cu_color = 'white' if self.turn % 2 == 1 else 'black'
                        x = math.floor(event.pos[0] / self.BLOCK_SIZE)
                        y = math.floor(event.pos[1] / self.BLOCK_SIZE)
                        cu_piece = self.current_board.get_board()[7-x][7-y]
                        if cu_piece.my_color is not None:
                            pygame.draw.rect(self.gameDisplay, self.GREEN,
                                             (x*self.BLOCK_SIZE, y*self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE),
                                             math.floor(self.BLOCK_SIZE/20))
                        for move in cu_piece.possible_moves:
                            if self.current_board.get_board()[move[0]][move[1]].my_color is None:
                                if move in cu_piece.fly:
                                    pygame.draw.circle(self.gameDisplay, self.RED,
                                                       ((7 - move[0]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2),
                                                        (7 - move[1]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2)),
                                                        math.floor(self.BLOCK_SIZE*0.15),
                                                        math.floor(self.BLOCK_SIZE*0.15))
                                else:
                                    pygame.draw.circle(self.gameDisplay, self.GREEN,
                                                       ((7-move[0]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2),
                                                        (7-move[1]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2)),
                                                        math.floor(self.BLOCK_SIZE * 0.15),
                                                        math.floor(self.BLOCK_SIZE*0.15))
                            elif self.current_board.get_board()[move[0]][move[1]].my_color.color != cu_piece.my_color.color:
                                pygame.draw.circle(self.gameDisplay, self.RED,
                                                   ((7 - move[0]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2),
                                                    (7 - move[1]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE/2)),
                                                    math.floor(self.BLOCK_SIZE * 0.15),
                                                    math.floor(self.BLOCK_SIZE*0.15))
                            else:
                                pygame.draw.circle(self.gameDisplay, self.GREEN,
                                                   ((7 - move[0]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE / 2),
                                                    (7 - move[1]) * self.BLOCK_SIZE + math.floor(self.BLOCK_SIZE / 2)),
                                                   math.floor(self.BLOCK_SIZE * 0.15),
                                                   math.floor(self.BLOCK_SIZE * 0.15))
                        if self.memory is not None:
                            last_piece = self.current_board.get_board()[7-self.memory[0]][7-self.memory[1]]
                            self.clear()
                            if cu_color == last_piece.my_color.color:
                                if isinstance(last_piece, Rook) and isinstance(cu_piece, King):
                                    if self.current_board.move_piece(7 - self.memory[0], 7 - self.memory[1], 'c', 'a'):
                                        self.turn += 1
                                        self.current_board.turn += 1
                                        self.update_moves_for_check()
                                elif self.current_board.move_piece(7-self.memory[0], 7-self.memory[1], 7-x, 7-y):
                                    self.turn += 1
                                    self.current_board.turn += 1
                                    self.update_moves_for_check()
                            self.memory = None
                            self.print_board()
                            self.draw_board()
                        else:
                            self.memory = (x, y) if self.current_board.get_board()[7-x][7-y].my_color is not None else None
                        self.last_board = self.current_board
                        self.update_moves_for_check()

                if event.type == pygame.QUIT:
                    quit_game = True
                    pygame.quit()
                    quit()

            pygame.display.flip()
            self.clock.tick(60)

    @staticmethod
    def clear():
        """
        Clearing console.
        :return:
        """
        sleep(0.5)
        if name == 'nt':
            _ = system('cls')
        else:
            _ = system('clear')

    def print_board(self):
        """
        Printing current board state.
        :return:
        """
        print(self.current_board)

    def console_game(self):
        """
        Starting game in the console and managing game's process.
        :return:
        """
        self.clear()
        while True:
            self.turn += 1
            self.current_board.turn += 1
            if self.turn != 1:
                self.update_moves_for_check()
            self.clear()
            self.print_board()
            self.last_board = self.current_board
            self.update_moves_for_check()
            if self.current_board.check_mate():
                input()
                return

            sq = self.make_move()
            if sq == 'ff':
                print('Game has ended')
                return
            sq = self.proper_move(sq)
            if sq == 'ff':
                print('Game has ended')
                return

    def proper_move(self, sq):
        """
        Checking if chosen move is legal to do.
        :param sq: Tuple of 3: (From square; to square; color: 1-white, 0-black, None-none of them)
        :return: Legal move in the same form as tuple in input.
        """
        while self.turn % 2 != sq[2] or \
                not self.current_board.move_piece(sq[0][0], sq[0][1], sq[1][0], sq[1][1]):
            self.clear()
            self.print_board()
            print('Improper move! Do something else!')
            sq = self.make_move()
            if sq == 'ff':
                return 'ff'
        return sq

    def make_move(self):
        """
        Receiving move from a player and printing possible moves for chosen piece.
        :return:
        Returning information about move that player want to do in tuple of 3:
        (From square; to square; color: 1-white, 0-black, None-none of them)
        """
        move_from = input('From:')
        while move_from not in self._possible_commands:
            self.clear()
            self.print_board()
            if move_from == 'author':
                print('This game is a college project of Bartosz Zimonczyk, enjoy the game :)')
            else:
                print('Improper move! Do something else!')
            move_from = input('From:')
        if move_from == 'ff':
            return 'ff'

        move_from = (8 - self._letters[move_from[0]], int(move_from[1]) - 1)
        moves_set = self.current_board.get_board()[move_from[0]][move_from[1]].possible_moves
        print({'{}{}'.format(self._numbers[8 - x], y + 1) for x, y in moves_set})

        move_to = input('To:')
        while move_to not in self._possible_commands:
            self.clear()
            self.print_board()
            print('Improper move! Do something else!')
            move_to = input('From:')
        if move_to == 'ff':
            return 'ff'

        x = move_from[0]
        y = move_from[1]
        piece = self.current_board.get_board()[x][y]
        if piece.my_color is not None and piece.my_color.color == 'white':
            color = 1
        elif piece.my_color is not None and piece.my_color.color == 'black':
            color = 0
        else:
            color = None
        if move_to == 'ca':
            move_to = (move_to[0], move_to[1])
        else:
            move_to = (8 - self._letters[move_to[0]], int(move_to[1]) - 1)
        return move_from, move_to, color

    def update_moves_for_check(self):
        """
        Updating moves of all pieces on the board.
        :return:
        """
        king = self.white_player.my_king if self.turn % 2 == 1 else self.black_player.my_king
        for i in range(8):
            for j in range(8):
                piece = self.current_board.get_board()[i][j]
                piece.update_moves(self.turn)
                if piece.my_color is not None and king.my_color.color == piece.my_color.color:
                    it = deepcopy(piece.possible_moves)
                    for x, y in it:
                        board = deepcopy(self.last_board)
                        board.move_piece(i, j, x, y, sym=True)
                        board.update_all()
                        if board.is_check():
                            piece.possible_moves.remove((x, y))


if __name__ == '__main__':
    g = Game()
    g.visual_game()

    # g.start_game()
