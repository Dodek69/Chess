import pygame as p

class Interface_object:
    def __init__(self, coordinates, hide_color : p.Color = p.Color(0, 0, 0), visible = True):
        self.coordinates = coordinates
        self.hide_color = hide_color
        self.visible = visible

class Rectangular_object(Interface_object):
    def __init__(self, coordinates, dimensions, hide_color : p.Color = p.Color(0, 0, 0), middle = True, color : p.Color = p.Color(255, 255, 255), visible = True):
        if middle:
            coordinates = (coordinates[0] - dimensions[0] // 2, coordinates[1] - dimensions[1] // 2)
        Interface_object.__init__(self, coordinates = coordinates, hide_color = hide_color, visible = visible)
        self.dimensions = dimensions
        self.color = color

    def on_x(self, coordinates):
        return coordinates[0] > self.coordinates[0] and coordinates[0] < self.coordinates[0] + self.dimensions[0]

    def on_y(self, coordinates):
        return coordinates[1] > self.coordinates[1] and coordinates[1] < self.coordinates[1] + self.dimensions[1]

    def on(self, coordinates):
        return self.on_x(coordinates) and self.on_y(coordinates)

    def hide(self, surface):
        p.draw.rect(surface, self.hide_color, (self.coordinates[0], self.coordinates[1], self.dimensions[0], self.dimensions[1]))

    def wait_for_click(self):
        while True:
            event = p.event.wait()
            if event.type == p.MOUSEBUTTONDOWN and self.on(p.mouse.get_pos()):
                return

p.font.init()
class Text(Rectangular_object):
    def __init__(self, coordinates, text = '', middle = True, hide_color = p.Color(0, 0, 0), color = p.Color(255, 255, 255), visible = True, background_color : p.Color = None, font = p.font.SysFont('Comic Sans MS', 50)):
        self.surface = font.render(text, True, color, background_color)
        Rectangular_object.__init__(self, coordinates = coordinates, dimensions = p.Surface.get_size(self.surface), hide_color = hide_color, middle = middle, color = color, visible = visible)

    def render(self, surface):
        if self.visible:
            surface.blit(self.surface, self.coordinates)
        else:
            self.hide(surface)
        return self

    def change_text(self, text = '', color = None, background_color : p.Color = None, font = p.font.SysFont('Comic Sans MS', 50)):
        if not color:
            color = self.color
        self.surface = font.render(text, True, color, background_color)

    def update(self, coordinates):
        pass

    def update_and_render(self, coordinates, surface):
        self.update(coordinates)
        self.render(surface)
        return self

class Framed_text(Rectangular_object):
    def __init__(self, coordinates, text = '', middle = True, hide_color = p.Color(0, 0, 0), color = p.Color(255, 255, 255), text_color : p.Color = p.Color(255, 255, 255), visible = True, background_color : p.Color = None, highlighted = False, font = p.font.SysFont('Comic Sans MS', 50)):
        self.text = Text(coordinates = coordinates, text = text, middle = middle, hide_color = hide_color, color = text_color, visible = visible, background_color = background_color, font = font)
        dimensions = p.Surface.get_size(self.text.surface)
        Rectangular_object.__init__(self, coordinates = coordinates, dimensions = (dimensions[0] * 1.2, dimensions[1] * 1.2), hide_color = hide_color, middle = middle, color = color, visible = visible)
        self.highlighted = highlighted

    def render(self, surface):
        if not self.highlighted:
            self.hide(surface)
        else:
            p.draw.rect(surface, self.color, (self.coordinates[0], self.coordinates[1], self.dimensions[0], self.dimensions[1]), 2, 10)

        if self.visible:
            self.text.render(surface)
        else:
            self.hide(surface)
        return self

    def update(self, coordinates):
        self.highlighted = self.on(coordinates)

    def update_and_render(self, coordinates, surface):
        self.update(coordinates)
        self.render(surface)
        return self

class Text_input(Rectangular_object):
    def __init__(self, coordinates, text = '', middle = True, hide_color = p.Color(0, 0, 0), color = p.Color(255, 255, 255), text_color : p.Color = p.Color(255, 255, 255), visible = True, background_color : p.Color = None, highlighted = False, font = p.font.SysFont('Comic Sans MS', 50)):
        self.text = Text(coordinates = coordinates, text = text, middle = middle, hide_color = hide_color, color = text_color, visible = visible, background_color = background_color, font = font)
        dimensions = p.Surface.get_size(self.text.surface)
        Rectangular_object.__init__(self, coordinates = coordinates, dimensions = dimensions, hide_color = hide_color, middle = middle, color = color, visible = visible)
        self.text1 = text

    def render(self, surface):
        if self.visible:
            p.draw.rect(surface, self.color, (self.coordinates[0], self.coordinates[1], self.dimensions[0], self.dimensions[1]), 2, 10)
            self.text.render(surface)
        else:
            self.hide(surface)
        return self

    def set_text(self, key = None):
        if not key:
            self.text1 = self.text1[:-1]
        else:
            self.text1 = self.text1 + key
        self.text.change_text(self.text1)
        dimensions = p.Surface.get_size(self.text.surface)

        if dimensions[0] != self.dimensions[0] and self.text1:
            self.coordinates = (self.coordinates[0] - (dimensions[0] - self.dimensions[0]) // 2, self.coordinates[1])
            self.text.coordinates = (self.text.coordinates[0] - (dimensions[0] - self.dimensions[0]) // 2, self.text.coordinates[1])
            self.dimensions = dimensions

    def update(self, coordinates):
        self.highlighted = self.visible and self.on(coordinates)

    def update_and_render(self, coordinates, surface):
        self.update(coordinates)
        self.render(surface)
        return self


class Dialog_box(Rectangular_object):
    def __init__(self, coordinates, text = '', left_button_name = 'No', right_button_name = 'Yes', middle = True, hide_color : p.Color = p.Color(0, 0, 0), color = p.Color(255, 255, 255), text_color : p.Color = p.Color(0, 0, 0), visible = True, background_color : p.Color = None, font = p.font.SysFont('Comic Sans MS', 50)):
        self.text = Text(coordinates = coordinates, text = text, middle = middle, hide_color = hide_color, color = text_color, visible = visible, background_color = background_color, font = font)
        dimensions = p.Surface.get_size(self.text.surface)
        self.text.coordinates = (self.text.coordinates[0], self.text.coordinates[1] - dimensions[1])

        width = max(dimensions[0], p.font.Font.size(font, left_button_name)[0] * 2, p.font.Font.size(font, right_button_name)[0] * 2) * 1.2
        self.left_button = Framed_text((coordinates[0] - width // 4, coordinates[1] + dimensions[1]), left_button_name, background_color = color, hide_color = color, text_color = text_color, color = hide_color)
        self.right_button = Framed_text((coordinates[0] + width // 4, coordinates[1] + dimensions[1]), right_button_name, background_color = color, hide_color = color, text_color = text_color, color = hide_color)

        Rectangular_object.__init__(self, coordinates = coordinates, dimensions = (width * 1.2, dimensions[1] * 4), hide_color = hide_color, middle = middle, color = color, visible = visible)

    def render(self, surface):
        if self.visible:
            p.draw.rect(surface, self.color, (self.coordinates[0], self.coordinates[1], self.dimensions[0], self.dimensions[1]), 0, 20)
            self.text.render(surface)
            self.left_button.render(surface)
            self.right_button.render(surface)
        else:
            self.hide(surface)
        return self

    def update(self, coordinates):
        self.left_button.update(coordinates)
        self.right_button.update(coordinates)

    def wait_until_chosen(self, surface):
        p.display.update()
        while True:
            event = p.event.wait()
            coordinates = p.mouse.get_pos()
            if event.type == p.MOUSEBUTTONDOWN:
                if self.left_button.on_y(coordinates):
                    if self.left_button.on_x(coordinates):
                        return False
                    elif self.right_button.on_x(coordinates):
                        return True
            elif event.type == p.MOUSEMOTION:
                self.left_button.update_and_render(coordinates, surface)
                self.right_button.update_and_render(coordinates, surface)
                p.display.update()

