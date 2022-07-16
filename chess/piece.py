import pygame as p

images = {}

class Piece:
    def __init__(self, is_white = True):
        self.is_white = is_white
        self.positions = []

    def load_image(self, square_size):
        if self.is_white:
            images['w' + self.__class__.__name__] = p.transform.scale(p.image.load(f"images/pieces/{'white_' + self.__class__.__name__.lower()}.png"), (square_size, square_size))
        else:
            images['b' + self.__class__.__name__] = p.transform.scale(p.image.load(f"images/pieces/{'black_' + self.__class__.__name__.lower()}.png"), (square_size, square_size))

    def render(self, surface):
        if self.is_white:
            surface.blit(images['w' + self.__class__.__name__], (self.coordinates[0], self.coordinates[1]))
        else:
            surface.blit(images['b' + self.__class__.__name__], (self.coordinates[0], self.coordinates[1]))

    def move(self, square):
        square.piece = self
        self.coordinates = square.coordinates

    def select(self, board):
        if self.positions:
            for position in self.positions:
                board.get_square(position).accessible = True

    def unselect(self, board):
        if self.positions:
            for position in self.positions:
                board.get_square(position).accessible = False

    def get_moves(self, board, position):
        moves = []
        for position in self.get_positions(board, position):
            move = board.get_square(position)
            if move.piece and move.piece.is_white == self.is_white:
                continue
            moves.append(move)
        return moves

class Piece_moved(Piece):
    def __init__(self, is_white = True):
        Piece.__init__(self, is_white)
        self.already_moved = False

class Pawn(Piece):
    value = 10
    def get_positions(self, board, position):
        moves = []
        if self.is_white:
            if not board.get_square((position[0]-1, position[1])).piece:
                moves.append((position[0]-1, position[1]))
                if position[0] == 6 and not board.get_square((position[0]-2, position[1])).piece:
                    moves.append((position[0]-2, position[1]))
            if position[1] != 0 and (board.get_square((position[0]-1, position[1]-1)).piece or board.get_square((position[0]-1, position[1]-1)) == board.invisible_pawn_square):
                moves.append((position[0]-1, position[1]-1))
            if position[1] != 7 and (board.get_square((position[0]-1, position[1]+1)).piece or board.get_square((position[0]-1, position[1]+1)) == board.invisible_pawn_square):
                moves.append((position[0]-1, position[1]+1))
        else:
            if not board.get_square((position[0]+1, position[1])).piece:
                moves.append((position[0]+1, position[1]))
                if position[0] == 1 and not board.get_square((position[0]+2, position[1])).piece:
                    moves.append((position[0]+2, position[1]))
            if position[1] != 0 and (board.get_square((position[0]+1, position[1]-1)).piece or board.get_square((position[0]+1, position[1]-1)) == board.invisible_pawn_square):
                moves.append((position[0]+1, position[1]-1))
            if position[1] != 7 and (board.get_square((position[0]+1, position[1]+1)).piece or board.get_square((position[0]+1, position[1]+1)) == board.invisible_pawn_square):
                moves.append((position[0]+1, position[1]+1))
        return moves

class Bishop(Piece):
    value = 30
    def get_positions(self, board, position):
        moves = []
        for i in range(1, min(8-position[0], 8-position[1])):
            moves.append((position[0]+i, position[1]+i))
            if board.get_square((position[0]+i, position[1]+i)).piece:
                break

        for i in range(1, min(7-position[0], position[1])+1):
            moves.append((position[0]+i, position[1]-i))
            if board.get_square((position[0]+i, position[1]-i)).piece:
                break

        for i in range(1, min(position[0], position[1])+1):
            moves.append((position[0]-i, position[1]-i))
            if board.get_square((position[0]-i, position[1]-i)).piece:
                break

        for i in range(1, min(position[0], 7-position[1])+1):
            moves.append((position[0]-i, position[1]+i))
            if board.get_square((position[0]-i, position[1]+i)).piece:
                break
        return moves

class King(Piece_moved):
    value = 100
    def get_positions(self, board, position):
        moves = []
        if position[0] != 0:
            moves.append((position[0]-1, position[1]))
            if position[1] != 0:
                moves.append((position[0]-1, position[1]-1))
                moves.append((position[0], position[1]-1))
            if position[1] != 7:
                moves.append((position[0]-1, position[1]+1))
                moves.append((position[0], position[1]+1))
        else:
            if position[1] != 0:
                moves.append((position[0], position[1]-1))
            if position[1] != 7:
                moves.append((position[0], position[1]+1))
            
        if position[0] != 7:
            moves.append((position[0]+1, position[1]))
            if position[1] != 0:
                moves.append((position[0]+1, position[1]-1))
            if position[1] != 7:
                moves.append((position[0]+1, position[1]+1))
        
        if not self.already_moved and board.whites_turn == self.is_white:
            if not board.get_square((position[0],5)).piece and not board.get_square((position[0],6)).piece and board.get_square((position[0],7)).piece and isinstance(board.get_square((position[0],7)).piece, Rook) and not board.get_square((position[0],7)).piece.already_moved and not board.check(self.is_white) and board.simulate_move(position, (position[0], 5)) and board.simulate_move(position, (position[0], 6)):
                moves.append((position[0], 6))
            if not board.get_square((position[0],1)).piece and not board.get_square((position[0],2)).piece and not board.get_square((position[0],3)).piece and board.get_square((position[0],0)).piece and isinstance(board.get_square((position[0],0)).piece, Rook) and not board.get_square((position[0],0)).piece.already_moved and not board.check(self.is_white) and board.simulate_move(position, (position[0], 1)) and board.simulate_move(position, (position[0], 2)) and board.simulate_move(position, (position[0], 3)):
                moves.append((position[0], 2))
        return moves
        
class Knight(Piece):
    value = 30
    def get_positions(self, board, position):
        moves = []
        if position[0] > 0:
            if position[1] > 1:
                moves.append((position[0]-1, position[1]-2))
            if position[1] < 6:
                moves.append((position[0]-1, position[1]+2))

            if position[0] > 1:
                if position[1] > 0:
                    moves.append((position[0]-2, position[1]-1))

                if position[1] < 7:
                    moves.append((position[0]-2, position[1]+1))

        if position[0] < 7:
            if position[1] > 1:
                moves.append((position[0]+1, position[1]-2))
            if position[1] < 6:
                 moves.append((position[0]+1, position[1]+2))

            if position[0] < 6:
                if position[1] > 0:
                    moves.append((position[0]+2, position[1]-1))
                if position[1] < 7:
                    moves.append((position[0]+2, position[1]+1))
        return moves

class Queen(Piece):
    value = 90
    def get_positions(self, board, position):
        return Bishop.get_positions(self, board, position) + Rook.get_positions(self, board, position)

class Rook(Piece_moved):
   value = 50
   def get_positions(self, board, position):
        moves = []
        for x in range(position[0]+1, 8):
            moves.append((x, position[1]))
            if board.get_square((x,position[1])).piece:
                break

        for x in range(position[1]+1, 8):
            moves.append((position[0], x))
            if board.get_square((position[0],x)).piece:
                break

        for x in range(position[0]-1, -1, -1):
            moves.append((x, position[1]))
            if board.get_square((x,position[1])).piece:
                break

        for x in range(position[1]-1, -1, -1):
            moves.append((position[0], x))
            if board.get_square((position[0],x)).piece:
                break
        return moves