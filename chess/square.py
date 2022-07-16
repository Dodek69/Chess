import pygame as p

class Square:
    def __init__(self, coordinates, piece = None):
        self.coordinates = coordinates
        self.piece = piece
        if piece:
            self.piece.coordinates = self.coordinates
    
class Classic_square(Square):
    def __init__(self, coordinates, piece = None):
        Square.__init__(self, coordinates, piece)
        self.accessible = False
        self.highlighted = False

    def render(self, window, square_size):
        if self.piece:
            self.piece.render(window)
        if self.accessible:
            p.draw.circle(window, p.Color(214, 214, 189), (self.coordinates[0] + square_size // 2, self.coordinates[1] + square_size // 2), square_size // 5)
    
    def position(self, board):
        for row in range(8):
            for column in range(8):
                if self is board.get_square((row,column)):
                    return (row, column)
        return None

    def move(self, square):
        self.piece.move(square)
        self.piece = None

    def unselect(self, board):
        self.highlighted = False
        self.piece.unselect(board)

    def select(self, board):
        self.highlighted = True
        self.piece.select(board)

class Classic_white_square(Classic_square):
    def render(self, window, square_size, white_color, black_color):
        if self.highlighted:
            p.draw.rect(window, p.Color(246, 246, 105), (self.coordinates[0], self.coordinates[1], square_size, square_size))
        else:
            p.draw.rect(window, white_color, (self.coordinates[0], self.coordinates[1], square_size, square_size))
        Classic_square.render(self, window, square_size)

class Classic_black_square(Classic_square):
    def render(self, window, square_size, white_color, black_color):
        if self.highlighted:
            p.draw.rect(window, (186, 202, 43), (self.coordinates[0], self.coordinates[1], square_size, square_size))
        else:
            p.draw.rect(window, black_color, (self.coordinates[0], self.coordinates[1], square_size, square_size))
        Classic_square.render(self, window, square_size)