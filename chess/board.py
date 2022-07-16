import pygame as p
from .piece import Knight, Bishop, Queen, King, Pawn, Rook, Piece, Piece_moved
from .square import Classic_white_square, Classic_black_square
import copy
from interface.interface import Dialog_box

class Board:
    def __init__(self, size, coordinates = (0,0), white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        self.square_size = size // 8
        self.coordinates = coordinates
        self.white_color = white_color
        self.black_color = black_color

class Classic_board(Board):
    def __init__(self, size, coordinates = (0, 0), whites_down = True, white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        Board.__init__(self, size = size, coordinates = coordinates, white_color = white_color, black_color = black_color)
        self.squares = [
            [Classic_white_square(coordinates, Rook(False)), Classic_black_square((coordinates[0] + self.square_size, coordinates[1]), Knight(False)), Classic_white_square((coordinates[0] + 2 * self.square_size, coordinates[1]), Bishop(False)), Classic_black_square((coordinates[0] + 3 * self.square_size, coordinates[1]), Queen(False)), Classic_white_square((coordinates[0] + 4 * self.square_size, coordinates[1]), King(False)), Classic_black_square((coordinates[0] + 5 * self.square_size, coordinates[1]), Bishop(False)), Classic_white_square((coordinates[0] + 6 * self.square_size, coordinates[1]), Knight(False)), Classic_black_square((coordinates[0] + 7 * self.square_size, coordinates[1]), Rook(False))],
            [Classic_black_square((coordinates[0], coordinates[1] + self.square_size), Pawn(False)), Classic_white_square((coordinates[0] + self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_black_square((coordinates[0] + 2 * self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_white_square((coordinates[0] + 3 * self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_black_square((coordinates[0] + 4 * self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_white_square((coordinates[0] + 5 * self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_black_square((coordinates[0] + 6 * self.square_size, coordinates[1] + self.square_size), Pawn(False)), Classic_white_square((coordinates[0] + 7 * self.square_size, coordinates[1] + self.square_size), Pawn(False))],
            [Classic_white_square((coordinates[0], coordinates[1] + 2 * self.square_size)), Classic_black_square((coordinates[0] + self.square_size, coordinates[1] + 2 * self.square_size)), Classic_white_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 2 * self.square_size)), Classic_black_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 2 * self.square_size)), Classic_white_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 2 * self.square_size)), Classic_black_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 2 * self.square_size)), Classic_white_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 2 * self.square_size)), Classic_black_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 2 * self.square_size))],
            [Classic_black_square((coordinates[0], coordinates[1] + 3 * self.square_size)), Classic_white_square((coordinates[0] + self.square_size, coordinates[1] + 3 * self.square_size)), Classic_black_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 3 * self.square_size)), Classic_white_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 3 * self.square_size)), Classic_black_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 3 * self.square_size)), Classic_white_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 3 * self.square_size)), Classic_black_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 3 * self.square_size)), Classic_white_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 3 * self.square_size))],
            [Classic_white_square((coordinates[0], coordinates[1] + 4 * self.square_size)), Classic_black_square((coordinates[0] + self.square_size, coordinates[1] + 4 * self.square_size)), Classic_white_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 4 * self.square_size)), Classic_black_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 4 * self.square_size)), Classic_white_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 4 * self.square_size)), Classic_black_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 4 * self.square_size)), Classic_white_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 4 * self.square_size)), Classic_black_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 4 * self.square_size))],
            [Classic_black_square((coordinates[0], coordinates[1] + 5 * self.square_size)), Classic_white_square((coordinates[0] + self.square_size, coordinates[1] + 5 * self.square_size)), Classic_black_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 5 * self.square_size)), Classic_white_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 5 * self.square_size)), Classic_black_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 5 * self.square_size)), Classic_white_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 5 * self.square_size)), Classic_black_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 5 * self.square_size)), Classic_white_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 5 * self.square_size))],
            [Classic_white_square((coordinates[0], coordinates[1] + 6 * self.square_size), Pawn()), Classic_black_square((coordinates[0] + self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_white_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_black_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_white_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_black_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_white_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn()), Classic_black_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 6 * self.square_size), Pawn())],
            [Classic_black_square((coordinates[0], coordinates[1] + 7 * self.square_size), Rook()), Classic_white_square((coordinates[0] + self.square_size, coordinates[1] + 7 * self.square_size), Knight()), Classic_black_square((coordinates[0] + 2 * self.square_size, coordinates[1] + 7 * self.square_size), Bishop()), Classic_white_square((coordinates[0] + 3 * self.square_size, coordinates[1] + 7 * self.square_size), Queen()), Classic_black_square((coordinates[0] + 4 * self.square_size, coordinates[1] + 7 * self.square_size), King()), Classic_white_square((coordinates[0] + 5 * self.square_size, coordinates[1] + 7 * self.square_size), Bishop()), Classic_black_square((coordinates[0] + 6 * self.square_size, coordinates[1] + 7 * self.square_size), Knight()), Classic_white_square((coordinates[0] + 7 * self.square_size, coordinates[1] + 7 * self.square_size), Rook())]
        ]
        self.whites_down = whites_down
        if not whites_down:
            self.invert()
        self.whites_turn = True
        self.king_square_position = [(0, 4), (7, 4)]
        self.selected_square = None
        self.invisible_pawn_square = None
        self.evaluation = 0
        self.top_captured_pieces = []
        self.bottom_captured_pieces = []

    def basic_move(self, square, move, surface, captured):
        if captured:
            temp = move
            move = Classic_white_square((0,0), captured)
        if move.piece or captured:
            p.mixer.Sound.play(p.mixer.Sound("sounds/capture.mp3"))
            if square.piece.is_white == self.whites_down:
                append_to = self.bottom_captured_pieces
                if not len(append_to):
                    move.piece.coordinates = (self.coordinates[0] + self.square_size * 8, 6 * self.square_size)
                else:
                    x = append_to[-1].coordinates[0] + self.square_size
                    y = append_to[-1].coordinates[1]
                    if x + self.square_size > surface.get_size()[0]:
                        y -= self.square_size
                        x = self.coordinates[0] + self.square_size * 8
                    move.piece.coordinates = (x, y)
            else:
                append_to = self.top_captured_pieces
                if not len(append_to):
                    move.piece.coordinates = (self.coordinates[0] + self.square_size * 8, self.square_size)
                else:
                    x = append_to[-1].coordinates[0] + self.square_size
                    y = append_to[-1].coordinates[1]
                    if x + self.square_size > surface.get_size()[0]:
                        y += self.square_size
                        x = self.coordinates[0] + self.square_size * 8
                    move.piece.coordinates = (x, y)
            append_to.append(move.piece)
        else:
            p.mixer.Sound.play(p.mixer.Sound("sounds/move.mp3"))
        if captured:
            move = temp
        square.move(move)

    def set_king_square_position(self, new_king_square_position):
        self.king_square_position[self.whites_turn] = new_king_square_position
        
    def get_position(self, coordinates):
        if self.whites_down:
            row = (coordinates[1] - self.coordinates[1]) // self.square_size
        else:
            row = (self.coordinates[1] + self.square_size * 8 - coordinates[1]) // self.square_size
        if row < 0 or row > 7:
            return None
        column = (coordinates[0] - self.coordinates[0]) // self.square_size
        if column < 0 or column > 7:
            return None
        return (row, column)

    def render(self, surface):
        for row in self.squares:
            for square in row:
                square.render(surface, self.square_size, self.white_color, self.black_color)

    def invert(self):
        for row in range(4):
            for column in range(8):
                temp = self.get_square((row,column)).coordinates
                self.get_square((row,column)).coordinates = self.get_square((7-row,column)).coordinates
                self.get_square((7-row,column)).coordinates = temp
                if self.get_square((row,column)).piece:
                    self.get_square((row,column)).piece.coordinates = self.get_square((row,column)).coordinates
                if self.get_square((7-row,column)).piece:
                    self.get_square((7-row,column)).piece.coordinates = self.get_square((7-row,column)).coordinates

    def check(self, is_white):
        for row in range(8):
            for column in range(8):
                square = self.get_square((row, column))

                if not square.piece or square.piece.is_white == is_white:
                    continue

                positions = square.piece.get_positions(self, (row, column))
                if positions and self.king_square_position[is_white] in positions:
                    return True
        return False

    def search(self, depth, alpha, beta):
        if depth == 0:
            self.get_moves()
            return (self.evaluation,)

        best_evaluation = float("-inf") if self.whites_turn else float("+inf")

        best_position = None
        selected_square_position = None
        queen = None

        for row in range(8):
            for column in range(8):
                square = self.get_square((row, column))
                if not square.piece or square.piece.is_white != self.whites_turn:
                    continue

                positions = square.piece.get_positions(self, (row, column))
                if positions:
                    for position in positions:
                        move = self.get_square(position)
                        if move.piece and move.piece.is_white == square.piece.is_white:
                            continue

                        test_board = copy.deepcopy(self)
                        if test_board.search_move(test_board.get_square((row, column)), row, test_board.get_square(position), position, True):
                            test_board.evaluation = test_board.search(depth - 1, alpha, beta)[0]
                            if square.piece.is_white:
                                if test_board.evaluation > best_evaluation:
                                    best_evaluation = test_board.evaluation
                                    best_position = position
                                    selected_square_position = (row, column)
                                    queen = True
                                    
                                    alpha = max(alpha, best_evaluation)
                                    if beta <= alpha:
                                        return (best_evaluation, selected_square_position, best_position, queen)
                            else:
                                if test_board.evaluation < best_evaluation:
                                    best_evaluation = test_board.evaluation
                                    best_position = position
                                    selected_square_position = (row, column)
                                    queen = True

                                    beta = min(beta, best_evaluation)
                                    if beta <= alpha:
                                        return (best_evaluation, selected_square_position, best_position, queen)
                   
                        if isinstance(square.piece, Pawn) and ((position[0] == 0 and square.piece.is_white) or (position[0] == 7 and not square.piece.is_white)):
                            test_board = copy.deepcopy(self)
                            if test_board.search_move(test_board.get_square((row, column)), row, test_board.get_square(position), position, False):
                                test_board.evaluation = test_board.search(depth - 1, alpha, beta)[0]
                                if square.piece.is_white:
                                    if test_board.evaluation > best_evaluation:
                                        best_evaluation = test_board.evaluation
                                        best_position = position
                                        selected_square_position = (row, column)
                                        queen = False

                                        alpha = max(alpha, best_evaluation)
                                        if beta <= alpha:
                                            return (best_evaluation, selected_square_position, best_position, queen)
                                else:
                                    if test_board.evaluation < best_evaluation:
                                        best_evaluation = test_board.evaluation
                                        best_position = position
                                        selected_square_position = (row, column)

                                        beta = min(beta, best_evaluation)
                                        if beta <= alpha:
                                            return (best_evaluation, selected_square_position, best_position, queen)
                                
        return (best_evaluation, selected_square_position, best_position, queen)

    def change_turn(self):
        self.whites_turn = not self.whites_turn

    def load_images(self):
        for row in self.squares:
            for square in row:
                if square.piece:
                    square.piece.load_image(self.square_size)

    def get_moves(self):
        self.evaluation = 0
        no_white_moves = True
        no_black_moves = True
        white_check = False
        black_check = False
        for row in range(8):
            for column in range(8):
                square = self.get_square((row, column))
                if not square.piece:
                    continue
                square.piece.positions = []
                if square.piece.is_white:
                    self.evaluation += square.piece.value
                    positions = square.piece.get_positions(self, (row, column))
                    if positions:
                        for position in positions:
                            move = self.get_square(position)
                            if move.piece:
                                if move.piece.is_white == square.piece.is_white:
                                    continue
                                self.evaluation += move.piece.value / 4
                            self.evaluation += 0.5
                            if position == self.king_square_position[False]:
                                black_check = True
                            if self.whites_turn:
                                if self.simulate_move((row, column), position):
                                    no_white_moves = False
                                    square.piece.positions.append(position)
                            elif no_white_moves:
                                if self.simulate_move((row, column), position):
                                    no_white_moves = False
                else:
                    self.evaluation -= square.piece.value
                    positions = square.piece.get_positions(self, (row, column))
                    if positions:
                        for position in positions:
                            move = self.get_square(position)
                            if move.piece:
                                if move.piece.is_white == square.piece.is_white:
                                    continue
                                self.evaluation -= move.piece.value / 4
                            self.evaluation -= 0.5
                            if position == self.king_square_position[True]:
                                white_check = True
                            if not self.whites_turn:
                                if self.simulate_move((row, column), position):
                                    no_black_moves = False
                                    square.piece.positions.append(position)
                            elif no_black_moves:
                                if self.simulate_move((row, column), position):
                                    no_black_moves = False

        if self.whites_turn and no_white_moves:
            if white_check:
                self.evaluation = float("-inf")
            else:
                self.evaluation = 0
            return True
        elif not self.whites_turn and no_black_moves:
            if black_check:
                self.evaluation = float("+inf")
            else:
                self.evaluation = 0
            return True
        return False

    def get_square(self, position):
        return self.squares[position[0]][position[1]]

    def select_square(self, square):
        self.selected_square = square
        square.select(self)

    def unselect_square(self):
        self.selected_square.unselect(self)
        self.selected_square = None

    def move_logic(self, square, square_row, move, move_position):
        captured = None
        if self.invisible_pawn_square:
            if move == self.invisible_pawn_square and isinstance(square.piece, Pawn):
                if move_position[0] == 2:
                    captured = self.get_square((3, move_position[1])).piece
                    self.get_square((3, move_position[1])).piece = None
                else:
                    captured = self.get_square((4, move_position[1])).piece
                    self.get_square((4, move_position[1])).piece = None
            self.invisible_pawn_square = None
        if isinstance(square.piece, Piece_moved):
            if isinstance(square.piece, King):
                self.set_king_square_position(move_position)
                if not square.piece.already_moved:
                    if move_position[1] == 6:
                        self.get_square((move_position[0], 7)).move(self.get_square((move_position[0], 5)))
                    elif move_position[1] == 2:
                        self.get_square((move_position[0], 7)).move(self.get_square((move_position[0], 3)))
            square.piece.already_moved = True
        elif isinstance(square.piece, Pawn) and ((square_row == 1 and not square.piece.is_white) or (square_row == 6 and square.piece.is_white)):
            if move_position[0] == 3:
                self.invisible_pawn_square = self.get_square((2,move_position[1]))
            elif move_position[0] == 4:
                self.invisible_pawn_square = self.get_square((5,move_position[1]))
        self.change_turn()
        return captured

    def move(self, square, square_row, move, move_position, surface, queen):
        captured = self.move_logic(square, square_row, move, move_position)
        if isinstance(square.piece, Pawn) and (move_position[0] == 0 or move_position[0] == 7):
            if queen == None:
                window_width, window_height = surface.get_size()
                dialog_box = Dialog_box((window_width // 2, window_height // 2), 'Choose piece:', 'Knight', 'Queen').render(surface)
                p.display.update()
                if dialog_box.wait_until_chosen(surface):
                    square.piece = Queen(square.piece.is_white)
                else:
                    square.piece = Knight(square.piece.is_white)
            else:
                if queen:
                    square.piece = Queen(square.piece.is_white)
                else:
                    square.piece = Knight(square.piece.is_white)
            square.piece.coordinates = square.coordinates
        self.basic_move(square, move, surface, captured)
        self.selected_square = move
        move.highlighted = True

    def search_move(self, square, square_row, move, move_position, queen = True):
        self.move_logic(square, square_row, move, move_position)
        if isinstance(square.piece, Pawn) and (move_position[0] == 0 or move_position[0] == 7):
            if queen:
                square.piece = Queen(square.piece.is_white)
            else:
                square.piece = Knight(square.piece.is_white)
        square.move(move)
        return not self.check(move.piece.is_white)

    def simulate_move(self, square_position, move_position):
        test_board = copy.deepcopy(self)
        return test_board.search_move(test_board.get_square(square_position), square_position[0], test_board.get_square(move_position), move_position)

