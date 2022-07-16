import pygame as p
from chess.defaults import DEFAULT_BACKGROUND_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_MENU_MUSIC, DEFAULT_GAME_MUSIC, DEFAULT_WHITE_COLOR, DEFAULT_BLACK_COLOR, ICON_PATH, WINDOW_TITLE
from interface.interface import Text, Framed_text, Dialog_box, Text_input
from chess.game import Classic_PvC_game, Classic_PvP_game
import webbrowser
import pickle

def update(objects, coordinates):
    for object in objects:
        object.update(coordinates)

def render(objects, surface):
    for object in objects:
        object.render(surface)

def update_and_render(objects, coordinates, surface):
    for object in objects:
        object.update_and_render(coordinates, surface)

def load_game():
    try:
        return pickle.load(open("save", "rb"))
    except OSError:
        return None

def setting_string(bool):
    if bool:
        return 'off'
    return 'on'

def main():
    def render_background():
        main_window.fill(background_color)

    def play_music():
        p.mixer.Sound.play(p.mixer.Sound('sounds/music.mp3'), -1)

    def stop_music():
        p.mixer.fadeout(1000)

    def game_start_music_control():
        if menu_music == game_music:
            return
        if game_music:
            play_music()
        else:
            stop_music()

    def game_end_music_control():
        if menu_music == game_music:
            return
        if menu_music:
            play_music()
        else:
            stop_music()
        
    def create_buttons_vertically(names):
        buttons = []
        n = len(names)
        for i, name in enumerate(names):
            buttons.append(Framed_text((window_width // 2, window_height // (n + 1) * (i + 1)), name, hide_color = background_color, text_color = text_color).render(main_window))
        return buttons

    def create_buttons_horizontally(text, names):
        buttons = []
        n = len(names)
        for i, name in enumerate(names):
            buttons.append(Framed_text((window_width // (n + 1) * (i + 1), window_height // 2), name, hide_color = background_color, text_color = text_color).render(main_window))
        buttons.append(Text((window_width // 2, window_height // 3), text, hide_color = background_color, color = text_color).render(main_window))
        return buttons

    def create_inputs_vertically(names):
        buttons = []
        n = len(names)
        space = Text((0, 0), names[0][0]).surface.get_size()[1] // 2
        for i, name in enumerate(names):
            buttons.append(Text((window_width // 2, window_height // (n + 2) * (i + 1) - space), name[0], color = text_color).render(main_window))
            buttons.append(Text_input((window_width // 2, window_height // (n + 2) * (i + 1) + space), name[1], text_color = text_color).render(main_window))
        buttons.append(Framed_text((window_width // 2, window_height // (n + 2) * (n + 1)), 'next >', hide_color = background_color, text_color = text_color).render(main_window))
        return buttons

    def clicked_button_index(buttons):
        p.display.update()
        while True:
            event = p.event.wait()
            coordinates = p.mouse.get_pos()
            if event.type == p.MOUSEMOTION:
                update_and_render(buttons, coordinates, main_window)
                p.display.update()

            elif event.type == p.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.on(coordinates):
                        render_background()
                        return i

    def input_control(buttons, front_pattern, back_pattern):
        p.display.update()
        selected = buttons[1]
        while True:
            event = p.event.wait()
            if event.type == p.MOUSEMOTION:
                buttons[-1].update_and_render(p.mouse.get_pos(), main_window)
                p.display.update()

            elif event.type == p.KEYDOWN:
                if event.key == p.K_BACKSPACE:
                    selected.set_text()
                else:
                    import re
                    if selected.text1 == '':
                        pattern = front_pattern
                    else:
                        pattern = f'^{front_pattern}{back_pattern}$'
                    if re.match(pattern, selected.text1 + event.unicode):
                        selected.set_text(event.unicode)

                render_background()
                render(buttons, main_window)
                p.display.update()

            elif event.type == p.MOUSEBUTTONDOWN:
                coordinates = p.mouse.get_pos()
                for button in buttons[1::2] + [buttons[-1]]:
                    if button.on(coordinates):
                        if button == buttons[-1]:
                            for button2 in buttons[1::2]:
                                if button2.text1 == '':
                                    break
                            else:
                                render_background()
                                return
                        selected = button
                        break

    def game_settings(vs_ai = True):
        render_background()
        if vs_ai:
            buttons = create_inputs_vertically((('player name:', 'Guest'),))
        else:
            buttons = create_inputs_vertically((('bottom player name:', 'Guest1'), ('top player name:', 'Guest2')))
        
        input_control(buttons, '[a-zA-Z]', '.{0,9}')
        bottom_player_name = buttons[1].text1
        if vs_ai:
            top_player_name = 'AI'
        else:
            top_player_name = buttons[3].text1

        whites_down = clicked_button_index(create_buttons_horizontally(f"{bottom_player_name}'s pieces color:", ('black', 'white')))

        buttons = create_inputs_vertically((('all time (in seconds):', '60'), ('time increment (in seconds):', '5'), ('time delay (in seconds):', '5')))
        input_control(buttons, '\d', '\d{0,4}')
        return (bottom_player_name, top_player_name, whites_down, int(buttons[1].text1), int(buttons[3].text1), int(buttons[5].text1))

    def main_menu():
        menu_objects = create_buttons_vertically(('Continue', 'vs. AI', '2 players', 'Settings', 'Creator', 'Exit'))
        while True:
            render_background()
            menu_objects[0].visible = load_game() != None
            render(menu_objects, main_window)
            p.display.update()
            index = clicked_button_index(menu_objects)
            if index == 0:
                while True:
                    game = load_game()
                    if game:
                        game_start_music_control()
                        dialog_box = Dialog_box((window_width // 2, window_height // 2), game.start(main_window), '< Back', 'Retry').render(main_window)
                        game_end_music_control()
                    else:
                        dialog_box = Dialog_box((window_width // 2, window_height // 2), 'Failed to load the game', '< Back', 'Retry').render(main_window)
                    if not dialog_box.wait_until_chosen(main_window):
                        break
            elif index == 1:
                while True:
                    bottom_player_name, top_player_name, whites_down, time, increment, delay = game_settings()
                    game_start_music_control()
                    dialog_box = Dialog_box((window_width // 2, window_height // 2), Classic_PvC_game(board_size = main_window, whites_down = whites_down, bottom_player_name = bottom_player_name, bottom_player_time = time, bottom_player_increment = increment, bottom_player_delay = delay, white_color = white_color, black_color = black_color).start(main_window), '< Back', 'Retry').render(main_window)
                    game_end_music_control()
                    if not dialog_box.wait_until_chosen(main_window):
                        break
            elif index == 2:
                while True:
                    bottom_player_name, top_player_name, whites_down, time, increment, delay = game_settings(False)
                    game_start_music_control()
                    dialog_box = Dialog_box((window_width // 2, window_height // 2), Classic_PvP_game(board_size = main_window, whites_down = whites_down, bottom_player_name = bottom_player_name, top_player_name = top_player_name, bottom_player_time = time, bottom_player_increment = increment, bottom_player_delay = delay, white_color = white_color).start(main_window), '< Back', 'Retry').render(main_window)
                    game_end_music_control()
                    if not dialog_box.wait_until_chosen(main_window):
                        break
            elif index == 3:
                while True:
                    render_background()
                    nonlocal menu_music
                    nonlocal game_music
                    index = clicked_button_index(create_buttons_vertically(((f'turn {setting_string(menu_music)} menu music', f'turn {setting_string(game_music)} game music', 'back'))))
                    if index == 0:
                        menu_music = not menu_music
                        if menu_music:
                            play_music()
                        else:
                            stop_music()
                    elif index == 1:
                        game_music = not game_music
                    else:
                        break
            elif index == 4:
                webbrowser.open('https://github.com/Dodek69')
            elif index == 5:
                return

    # Load defaults
    background_color = DEFAULT_BACKGROUND_COLOR
    text_color = DEFAULT_TEXT_COLOR
    menu_music = DEFAULT_MENU_MUSIC
    game_music = DEFAULT_GAME_MUSIC
    white_color = DEFAULT_WHITE_COLOR
    black_color = DEFAULT_BLACK_COLOR

    p.init()
    p.display.set_caption(WINDOW_TITLE)
    p.display.set_icon(p.image.load(ICON_PATH))
    main_window = p.display.set_mode()
    window_width, window_height = main_window.get_size()
   
    if menu_music:
        play_music()

    main_menu()
    
if __name__ == '__main__':
    main()