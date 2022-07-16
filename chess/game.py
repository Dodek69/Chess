from chess.board import Classic_board
import pygame as p
from interface.interface import Text, Framed_text, Dialog_box
from chess.piece import Pawn
import pickle
import math
from concurrent.futures import ProcessPoolExecutor

def render(objects, surface):
    for object in objects:
        object.render(surface)

class Time_control:
    def __init__(self, white_time = None, white_increment = None, white_delay = None, black_time = None, black_increment = None, black_delay = None):
        if not white_time:
            self.white_time = black_time
            self.white_increment = black_increment
            self.white_delay = black_delay
        else:
            self.white_time = white_time
            self.white_increment = white_increment
            self.white_delay = white_delay
        
        if not black_time:
            self.black_time = white_time
            self.black_increment = white_increment
            self.black_delay = white_delay
        else:
            self.black_time = black_time
            self.black_increment = black_increment
            self.black_delay = black_delay

        self.delay = self.white_delay
        self.started = False

    def change_turn(self, whites_turn):
        self.started = True

        if whites_turn:
            self.black_time += self.black_increment
            self.delay = self.white_delay
        else:
            self.white_time += self.white_increment
            self.delay = self.black_delay

    def update(self, whites_turn, times = 1):
        if not self.started:
            return False

        self.delay -= times

        if not self.delay < 0:
            return False
        
        if whites_turn:
            self.white_time += self.delay
            if not self.white_time > 0:
                return True
        else:
            self.black_time += self.delay
            if not self.black_time > 0:
                return True
        self.delay = 0
        return False

    def get_time(self, is_white):
        if is_white:
            return (self.white_time, self.white_increment, self.white_delay)
        return (self.black_time, self.black_increment, self.black_delay)

    def to_string(self, is_white):
        import datetime
        if is_white:
            return str(datetime.timedelta(seconds = self.white_time))
        return str(datetime.timedelta(seconds=self.black_time))

class Game:
    def __init__(self, white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        self.white_color = white_color
        self.black_color = black_color

    def save_game(self):
        with open('save', 'wb') as handle:
            pickle.dump(self, handle)

    def try_save_game(self):
        try:
            self.save_game()
        except Exception as e:
            return str(e)
        return None

class Two_player_game(Game):
    def __init__(self, bottom_player_name = 'Guest1', top_player_name = 'Guest2', white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        Game.__init__(self, white_color = white_color, black_color = black_color)
        self.bottom_player_name = bottom_player_name
        self.top_player_name = top_player_name

class Classic_game(Two_player_game):
    def __init__(self, board_size = None, whites_down = True, bottom_player_name = 'Guest1', top_player_name = 'Guest2', bottom_player_time = 60, bottom_player_increment = 5, bottom_player_delay = 5, top_player_time = None, top_player_increment = None, top_player_delay = None, white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        Two_player_game.__init__(self, bottom_player_name = bottom_player_name, top_player_name = top_player_name, white_color = white_color, black_color = black_color)
        if isinstance(board_size, p.Surface):
            surface_size = p.Surface.get_size(board_size)
            board_size = min(surface_size[0] - surface_size[0] % 8, surface_size[1] - surface_size[1] % 8)

        self.board = Classic_board(size = board_size, coordinates = (board_size // 16, 0), whites_down = whites_down, white_color = white_color, black_color = black_color)

        if whites_down:
            self.time_control = Time_control(bottom_player_time, bottom_player_increment, bottom_player_delay, top_player_time, top_player_increment, top_player_delay)
        else:
            self.time_control = Time_control(top_player_time, top_player_increment, top_player_delay, bottom_player_time, bottom_player_increment, bottom_player_delay)

    def init(self, surface):
        self.board.load_images()
        self.render(surface)
        self.board.get_moves()
        self.type = p.event.custom_type()
        p.time.set_timer(self.type, 1000)

    def render_evaluation(self, surface, coordinates = (0, 0)):
        half_board_size = self.board.square_size * 4
        if self.board.evaluation > half_board_size:
            self.board.evaluation = half_board_size
        elif self.board.evaluation < -half_board_size:
           self.board.evaluation = -half_board_size
        
        temp1 = half_board_size - self.board.evaluation
        temp2 = half_board_size + self.board.evaluation
        width = self.board.square_size // 2

        if self.board.whites_down:
            p.draw.rect(surface, p.Color(0, 0, 0), (coordinates[0], coordinates[1], width, temp1))
            p.draw.rect(surface, p.Color(255, 255, 255), (coordinates[0], coordinates[1] + temp1, width, temp2))
        else:
            p.draw.rect(surface, p.Color(255, 255, 255), (coordinates[0], coordinates[1], width, temp2))
            p.draw.rect(surface, p.Color(0, 0, 0), (coordinates[0], coordinates[1] + temp2, width, temp1))
          
    def create_buttons(self, surface):
        surface_size = p.Surface.get_size(surface)
        draw_button = Framed_text((0, 0), "Draw", False, hide_color = p.Color(100, 100, 100))
        draw_button_size = p.Surface.get_size(draw_button.text.surface)
        draw_button.coordinates = (surface_size[0] - draw_button_size[0], 0)
        draw_button.text.coordinates = draw_button.coordinates

        resign_button = Framed_text((0, 0), "Resign", False, hide_color = p.Color(100, 100, 100))
        resign_button_size = p.Surface.get_size(resign_button.text.surface)
        resign_button.coordinates = (surface_size[0] - resign_button_size[0], surface_size[1] - resign_button_size[1])
        resign_button.text.coordinates = resign_button.coordinates

        bigger_button_width = max(draw_button_size[0], resign_button_size[0])
        
        x = self.board.coordinates[0] + self.board.square_size * 8
        top_player_name_text = Text((x, self.board.coordinates[1]), self.top_player_name, middle = False).render(surface)
        bottom_player_name_text = Text((x, self.board.coordinates[1] + self.board.square_size * 7.4), self.bottom_player_name, middle = False).render(surface)
        left = max(top_player_name_text.coordinates[0] + top_player_name_text.dimensions[0], bottom_player_name_text.coordinates[0] + bottom_player_name_text.dimensions[0])
        top_timer = Text((left + ((surface_size[0] - bigger_button_width) - (left)) // 2, top_player_name_text.coordinates[1]), self.time_control.to_string(not self.board.whites_down), middle = False)
        top_timer.coordinates = (top_timer.coordinates[0] - p.Surface.get_size(top_timer.surface)[0] // 2, top_timer.coordinates[1])
        bottom_timer = Text((left + ((surface_size[0] - bigger_button_width) - (left)) // 2, bottom_player_name_text.coordinates[1]), self.time_control.to_string(self.board.whites_down), middle = False)
        bottom_timer.coordinates = (bottom_timer.coordinates[0] - p.Surface.get_size(bottom_timer.surface)[0] // 2, bottom_timer.coordinates[1])

        return (top_timer, draw_button, bottom_timer, resign_button)

    def render_interface(self, surface):
        render(self.create_buttons(surface), surface)
        
    def render_captured_pieces(self, surface):
        for piece in self.board.top_captured_pieces + self.board.bottom_captured_pieces:
            piece.render(surface)
        
    def render(self, surface):
        surface.fill(p.Color(100, 100, 100))
        self.render_captured_pieces(surface)
        self.render_evaluation(surface)
        self.render_interface(surface)
        self.board.render(surface)

    def play(self, surface):
        self.mouse_button_down = False
        while True:
            event = p.event.wait()
            coordinates = p.mouse.get_pos()
            if event.type == p.MOUSEMOTION: # drag animation
                if self.mouse_button_down and self.board.selected_square:
                    self.render(surface)
                    self.board.selected_square.piece.coordinates = coordinates[0] - self.board.square_size // 2, coordinates[1] - self.board.square_size // 2
                    self.board.selected_square.piece.render(surface)
                
                draw_button, bottom_timer, resign_button = self.create_buttons(surface)[1:4]
                draw_button.update_and_render(coordinates, surface)
                resign_button.update_and_render(coordinates, surface)
            elif event.type == p.MOUSEBUTTONDOWN:
                self.mouse_button_down = True
                position = self.board.get_position(coordinates)
                if not position:
                    message = self.interface_click_handler(coordinates, surface)
                    if message:
                        return message
                    if self.board.selected_square:
                        self.board.unselect_square()
                    self.board.render(surface)
                else:
                    move = self.board.get_square(position)
                    if move.accessible: # move piece
                        message = self.move_handler(move, position, surface)
                        if message:
                            return message
                    elif move.piece: # select
                        if self.board.selected_square:
                            self.board.selected_square.unselect(self.board)
                        
                        self.board.select_square(move)
                        self.board.selected_square_row = position[0]
                    else: # unselect
                        if self.board.selected_square:
                            self.board.unselect_square()
                    self.board.render(surface)
                    self.try_save_game()
            elif event.type == p.MOUSEBUTTONUP:
                self.mouse_button_down = False
                if self.board.selected_square and self.board.selected_square.piece:
                    position = self.board.get_position(coordinates)
                    if position:
                        move = self.board.get_square(position)
                        if move and move.accessible: # move piece
                            message = self.move_handler(move, position, surface)
                            if message:
                                return message
                        else: # bring back dragged piece
                            self.board.selected_square.piece.coordinates = self.board.selected_square.coordinates
                    else:
                        self.board.selected_square.piece.coordinates = self.board.selected_square.coordinates
                    self.render(surface)
            elif event.type == p.QUIT:
                return 'Quitted'
            elif event.type == self.type:
                if self.time_control.update(self.board.whites_turn):
                    if self.board.whites_turn == self.board.whites_down:
                        return f'{self.bottom_player_name} is out of time, {self.top_player_name} won'
                    return f'{self.top_player_name} is out of time, {self.bottom_player_name} won'
                self.render(surface)
            else:
                continue

            p.display.update()

    def lost_checker(self):
        if self.board.get_moves():
            if self.board.check(self.board.whites_turn):
                if self.board.whites_turn == self.board.whites_down:
                    return f'Checkmate, {self.top_player_name} won'
                return f'Checkmate, {self.bottom_player_name} won'
            else:
                if self.board.whites_turn == self.board.whites_down:
                    return f'Stalemate, {self.top_player_name} won'
                return f'Stalemate, {self.bottom_player_name} won'
            
class Classic_PvC_game(Classic_game):
    def __init__(self, board_size = None, whites_down = True, bottom_player_name = 'Guest', bottom_player_time = 60, bottom_player_increment = 5, bottom_player_delay = 5, top_player_time = None, top_player_increment = None, top_player_delay = None, white_color = p.Color(238, 238, 210), black_color = p.Color(118, 150, 86)):
        Classic_game.__init__(self, board_size = board_size, whites_down = whites_down, bottom_player_name = bottom_player_name, top_player_name = 'AI', bottom_player_time = bottom_player_time, bottom_player_increment = bottom_player_increment, bottom_player_delay = bottom_player_delay, top_player_time = top_player_time, top_player_increment = top_player_increment, top_player_delay = top_player_delay, white_color = white_color, black_color = black_color)
        self.depth_time = [None]

    def start(self, surface):
        self.init(surface)
        if not self.board.whites_down:
            self.make_best_move(surface)
            self.board.get_moves()
            self.time_control.change_turn(self.board.whites_turn)
        return self.play(surface)

    def interface_click_handler(self, coordinates, surface):
        draw_button, bottom_timer, resign_button = self.create_buttons(surface)[1:4]
        if draw_button.on(coordinates):
            x = 0
            y = 5
            for row in self.board.squares:
                for square in row:
                    if square.piece:
                        x += y
            if (self.board.whites_down and self.board.evaluation > x) or (not self.board.whites_down and -self.board.evaluation > x):
                return 'Draw accepted'
            else:
                window_width, window_height = surface.get_size()
                dialog_box = Dialog_box((window_width // 2, window_height // 2), f'{self.top_player_name} rejected draw.', 'OK', 'Huge mistake.').render(surface)
                dialog_box.wait_until_chosen(surface)
                self.render(surface)
        elif resign_button.on(coordinates):
            window_width, window_height = surface.get_size()
            dialog_box = Dialog_box((window_width // 2, window_height // 2), f'Are you sure you want to resign {self.bottom_player_name}?', 'No', 'Yes').render(surface)
            if dialog_box.wait_until_chosen(surface):
                self.render(surface)
                return f'{self.bottom_player_name} resigned'
            self.render(surface)

    def make_best_move(self, surface):
        if not self.depth_time[0]:
            depth = 0
        else:
            timer, increment, delay = self.time_control.get_time(self.board.whites_turn)
            depth = self.previous_depth
            if increment + delay > self.depth_time[0]:
                timer += delay + increment
                if len(self.depth_time) > depth + 1:
                    if self.depth_time[depth + 1] * 3 < timer:
                        depth += 1
                elif self.depth_time[depth] * 30 < timer:
                    depth += 1
                elif timer < self.depth_time[depth] * 2:
                    depth -= 1
            else:
                timer2, increment2, delay2 = self.time_control.get_time(not self.board.whites_turn)
                if timer <= timer2:
                    depth -= 1
                elif len(self.depth_time) > depth + 1:
                    if timer - self.depth_time[depth + 1] * 3 > timer2:
                        depth += 1
                elif timer - self.depth_time[depth] * 30 > timer2:
                    depth += 1
            depth = max(0, depth)
        #print(f"chosen deph: {depth}")
        import time
        start = time.perf_counter()
        pool = ProcessPoolExecutor(3)
        future = pool.submit(self.board.search, depth + 1, float("-inf"), float("inf"))
        self.mouse_button_down = False
        new = None
        new_pos = None
        while not future.done():
            for event in p.event.get():
                coordinates = p.mouse.get_pos()
                if event.type == p.MOUSEMOTION: # drag animation
                    if self.mouse_button_down and self.board.selected_square:
                        self.render(surface)
                        self.board.selected_square.piece.coordinates = coordinates[0] - self.board.square_size // 2, coordinates[1] - self.board.square_size // 2
                        self.board.selected_square.piece.render(surface)
                
                    draw_button, bottom_timer, resign_button = self.create_buttons(surface)[1:4]
                    draw_button.update_and_render(coordinates, surface)
                    resign_button.update_and_render(coordinates, surface)
                elif event.type == p.MOUSEBUTTONDOWN:
                    self.mouse_button_down = True
                    position = self.board.get_position(coordinates)
                    if not position:
                        message = self.interface_click_handler(coordinates, surface)
                        if message:
                            return message
                        if self.board.selected_square:
                            self.board.unselect_square()
                        self.board.render(surface)
                    else:
                        move = self.board.get_square(position)
                        if move.piece: # select
                            if self.board.selected_square:
                                self.board.unselect_square()
                            move.piece.positions = []
                            if self.board.whites_down == move.piece.is_white:
                                new = move
                                new_pos = position
                                
                                for pos in move.piece.get_positions(self.board, position):
                                    if self.board.get_square(pos).piece and self.board.get_square(pos).piece.is_white == move.piece.is_white:
                                        continue
                                    if self.board.simulate_move(position, pos) and self.board.get_square(pos) != self.board.invisible_pawn_square:
                                        move.piece.positions.append(pos)

                            self.board.select_square(move)
                        else: # unselect
                            if self.board.selected_square:
                                self.board.unselect_square() 
                            self.board.selected_square = None
                        self.board.render(surface)
                        self.try_save_game()
                elif event.type == p.MOUSEBUTTONUP:
                    self.mouse_button_down = False
                    if self.board.selected_square and self.board.selected_square.piece:
                        self.board.selected_square.piece.coordinates = self.board.selected_square.coordinates
                        self.render(surface)
                elif event.type == p.QUIT:
                    return 'Quitted'
                elif event.type == self.type:
                    if self.time_control.update(self.board.whites_turn):
                        if self.board.whites_turn == self.board.whites_down:
                            return f'{self.bottom_player_name} is out of time'
                        return f'{self.top_player_name} is out of time'
                    self.render(surface)
                else:
                    continue
                p.display.update()

        selected_square_position, best_move_position, queen = future.result()[1:]
        if not best_move_position:
            if self.board.check(self.board.whites_turn):
                return f'Checkmate, {self.bottom_player_name} won'
            return 'Stalemate, draw'

        if len(self.depth_time) == depth:
            self.depth_time.append(int(math.ceil(time.perf_counter() - start)))
        else:
            self.depth_time[depth] = int(math.ceil(time.perf_counter() - start))
        #print(f'AI time: {self.depth_time[depth]}\ndepth = {depth+1}\n')
        self.previous_depth = depth
        best_move = self.board.get_square(best_move_position)
        if self.board.selected_square:
            self.board.unselect_square()

        self.board.move(self.board.get_square(selected_square_position), selected_square_position[0], best_move, best_move_position, surface, queen)

        if new:
            self.board.unselect_square()
            new.piece.positions = []
            for pos in new.piece.get_positions(self.board, new_pos):
                if self.board.get_square(pos).piece and self.board.get_square(pos).piece.is_white == new.piece.is_white:
                    continue
                if self.board.simulate_move(new_pos, pos):
                    new.piece.positions.append(pos)

            self.board.select_square(new)
        self.board.render(surface)
        self.render_evaluation(surface)
        p.display.update()

        return None

    def move_handler(self, move, position, surface):
        self.board.selected_square.unselect(self.board)
        self.board.move(self.board.selected_square, self.board.selected_square_row, move, position, surface, None)
        self.board.render(surface)
        p.display.update()
        self.time_control.change_turn(self.board.whites_turn)
        message = self.make_best_move(surface)
        if message:
            return message
        message = self.lost_checker()
        if message:
            self.render_evaluation(surface)
            return message
        self.time_control.change_turn(self.board.whites_turn)
        
class Classic_PvP_game(Classic_game):
    def start(self, surface):
        self.init(surface)
        return self.play(surface)

    def interface_click_handler(self, coordinates, surface):
        top_timer, draw_button, bottom_timer, resign_button = self.create_buttons(surface)
        if draw_button.on(coordinates):
            window_width, window_height = surface.get_size()
            if self.board.whites_turn == self.board.whites_down:
                dialog_box = Dialog_box((window_width // 2, window_height // 2), f'{self.bottom_player_name} proposes a draw. Do you accept {self.top_player_name}?', 'No', 'Yes').render(surface)
            else:
                dialog_box = Dialog_box((window_width // 2, window_height // 2), f'{self.top_player_name} proposes a draw. Do you accept {self.bottom_player_name}?', 'No', 'Yes').render(surface)
            if dialog_box.wait_until_chosen(surface):
                self.render(surface)
                return 'Draw'
            self.render(surface)
        elif resign_button.on(coordinates):
            window_width, window_height = surface.get_size()
            if self.board.whites_turn == self.board.whites_down:
                dialog_box = Dialog_box((window_width // 2, window_height // 2), f'Are you sure you want to resign {self.bottom_player_name}?', 'No', 'Yes').render(surface)
            else:
                dialog_box = Dialog_box((window_width // 2, window_height // 2), f'Are you sure you want to resign {self.top_player_name}?', 'No', 'Yes').render(surface)
            if dialog_box.wait_until_chosen(surface):
                self.render(surface)
                if self.board.whites_turn == self.board.whites_down:
                    return f'{self.top_player_name} won'
                return f'{self.bottom_player_name} won'
            self.render(surface)

    def move_handler(self, move, position, surface):
        self.board.selected_square.unselect(self.board)
        self.board.move(self.board.selected_square, self.board.selected_square_row, move, position, surface, None)
        self.board.render(surface)
        p.display.update()
        message = self.lost_checker()
        if message:
            self.render_evaluation(surface)
            return message
        self.time_control.change_turn(self.board.whites_turn)
