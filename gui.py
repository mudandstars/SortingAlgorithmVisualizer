
import drawing_flow
from algorithms import *

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from random import randint
import time
import threading

import pdb
import heapq

window_sizes = Window.size
colors = {"red": (1, 0, 0), "blue": (0, 0, 1), "green": (0, 1, 0)}

# todo: fix merge_sort
# todo: tidy up the file


class MainScreen(BoxLayout):

    # algorithms = {"Heapsort": self.heapsort(), "Insertion Sort": self.insertion_sort(),
    #              "Selection Sort": self.selection_sort(), "Shellsort": self.shell_sort(),
    #             "Merge Sort": self.merge_sort(),
    #             "Quicksort": self.quick_sort()}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # booleans
        self.algorithm_chosen = False
        self.selected_algorithm = None
        self.button_pressed = False
        self.is_heap_sort = False

        # lists
        self.items = []
        self.rectangles = []
        self.labels = []
        self.indices = []  # (current_ind, old_ind, new_ind) for every change
        self.heap_history = []

        # initialize standard values
        self.slider_value = 22.5
        self.item_counter = int(self.slider_value * 3)
        self.data_width = int(500 / self.slider_value)
        self.data_spacing = int(50 / self.slider_value)
        self.font_size_items = int(9 + (9 - (self.slider_value ** 0.6))) if self.slider_value <= 25 else 0
        self.standard_units = dp(100)
        self.start_pos_y = int(8.5 * self.standard_units)
        self.offset_x = 0
        self.i = 0

        self.speed = .5

    def run_algorithm(self):
        """
        When the 'Run Algorithm' Button is pressed, this method is executed.
        It initialises the algorithm.
        :return: None
        """
        self.button_pressed = True
        self.call_algorithm()

    def call_algorithm(self):

        self.indices = []
        self.i = 0

        if self.selected_algorithm == "Selection Sort":
            self.indices = selection_sort.selection_sort(self)
            drawing_flow.start_drawing(self)
        elif self.selected_algorithm == "Insertion Sort":
            self.indices = insertion_sort.insertion_sort(self)
            drawing_flow.start_drawing(self)
        elif self.selected_algorithm == "Shellsort":
            self.indices = shellsort.shell_sort(self)
            drawing_flow.start_drawing(self)
        elif self.selected_algorithm == "Merge Sort":
            self.indices, self.items = merge_sort.merge_sort(self.items)
            drawing_flow.start_drawing(self)
        elif self.selected_algorithm == "Heapsort":
            self.indices, self.heap_history = heapsort.heapsort(self)
            drawing_flow.start_drawing(self)
        elif self.selected_algorithm == "Quicksort":
            self.indices = quicksort.quick_sort(self.items)
            drawing_flow.start_drawing(self)

    def slider_moved(self):
        """
        Whenever the slider is moved, this method is executed.
        It updates slider-related values, resets lists and draws the items on the GUI.
        :return: None
        """
        self.update_values()
        self.reset_lists()
        self.initialize_items()

    def drop_down_clicked(self, value):
        """
        This method is called whenever the drop-down menu is clicked.
        It sets the selected algorithm to the clicked algorithm and updates the button text.
        :param value: String (Button value)
        :return: None
        """
        self.ids.run_algorithm_button.disabled = False
        self.ids.run_algorithm_button.text = f'Run {value}'
        self.selected_algorithm = value

    def update_values(self):
        """
        Updates slider-related values.
        :return: None
        """
        # update slider information
        self.slider_value = int(self.ids.my_slider.value)
        self.item_counter = int(self.slider_value * 3)
        self.data_width = int(500 / self.slider_value)
        self.data_spacing = int(50 / self.slider_value)
        self.font_size_items = int(9 + (9 - (self.slider_value ** 0.6))) if self.slider_value <= 25 else 0
        self.offset_x = self.width / 10
        # set speed at an 'appropriate' level
        self.speed = ((1 / self.slider_value) ** 2) * 5

    def reset_lists(self):
        """
        Resets the object's lists and populates the items with random integers.
        :return: None
        """
        # reset and populate list
        self.items = [randint(1, 750) for i in range(self.item_counter)]
        self.rectangles = []
        self.labels = []

    def initialize_items(self):
        """
        Draws the rectangles on the board.
        :return: None
        """
        # redraw black screen
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0, self.start_pos_y), size=(self.width, - 9 * self.standard_units))

        # draw rectangles and labels
        offset = self.offset_x - self.width/2
        with self.canvas:
            for data_height in self.items:
                pos_x = int(self.width/2 - self.data_width/2 + offset)
                rectangle_size = (self.data_width, -dp(data_height))
                text_y = 8.4 * self.standard_units - dp(data_height)
                Color(1, 1, 1)
                self.rectangles.append(Rectangle(pos=(pos_x, self.start_pos_y), size=rectangle_size))
                self.labels.append(Label(pos=(pos_x, text_y), width=self.data_width,
                                         height=dp(-5), text=str(data_height), font_size=self.font_size_items, bold=True))
                offset += (self.data_width + self.data_spacing)

    def draw_change(self, dt=0):
        """
        Visualizes the exchange of two items.
        :return: None
        """
        old_ind, new_ind, old_val, new_val = self.indices[self.i][1:]

        offset = (self.data_width + self.data_spacing)
        start_pos_x = int((self.width / 2 - self.data_width / 2) - self.width/2 + self.offset_x)

        old_pos = (start_pos_x + old_ind * offset, self.start_pos_y)
        old_size = (self.data_width, -dp(old_val))
        new_pos = (start_pos_x + new_ind * offset, self.start_pos_y)
        new_size = (self.data_width, -dp(new_val))
        black_box_size = (self.data_width, -int(9 * self.standard_units))

        text_y_old = 8.4 * self.standard_units - dp(old_val)
        text_y_new = 8.4 * self.standard_units - dp(new_val)

        # draw black where the items are
        with self.canvas:
            Color(0, 0, 0)
            self.rectangles[old_ind] = Rectangle(pos=old_pos, size=black_box_size)
            self.rectangles[new_ind] = Rectangle(pos=new_pos, size=black_box_size)

        # draw new items in place
        with self.canvas:
            Color(0, 102/255, 0)  # dark green
            self.rectangles[old_ind] = Rectangle(pos=old_pos, size=new_size)
            self.rectangles[new_ind] = Rectangle(pos=new_pos, size=old_size)
            self.labels.append(Label(pos=(new_pos[0], text_y_old), width=self.data_width, height=dp(-5),
                                     text=str(old_val), font_size=self.font_size_items, bold=True))
            self.labels.append(Label(pos=(old_pos[0], text_y_new), width=self.data_width, height=dp(-5),
                                     text=f'{new_val}', font_size=self.font_size_items, bold=True))

        self.i += 1

    def draw_done(self):
        """
        Changes the rectangles color.
        Called when sorting is completed.
        :return: None
        """
        # draw black
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0, 0), size=(self.width, self.start_pos_y + 30))

        # draw rectangles and labels
        offset = self.offset_x - self.width / 2
        with self.canvas:
            for data_height in self.items:
                pos_x = int(self.width / 2 - self.data_width / 2 + offset)
                rectangle_size = (self.data_width, -dp(data_height))
                text_y = 8.4 * self.standard_units - dp(data_height)
                Color(1, 0, 0)
                self.rectangles.append(Rectangle(pos=(pos_x, self.start_pos_y), size=rectangle_size))
                self.labels.append(Label(pos=(pos_x, text_y), width=self.data_width,
                                         height=dp(-5), text=str(data_height), font_size=self.font_size_items,
                                         bold=True))
                offset += (self.data_width + self.data_spacing)

    def indicate_current_rect(self):
        """
        Draws a violet box above the currently indexed rectangle.
        :return: None
        """
        y_pos = self.start_pos_y + 10
        y_size = 20

        offset = (self.data_width + self.data_spacing)
        start_pos_x = int((self.width / 2 - self.data_width / 2) - self.width/2 + self.offset_x)
        current_ind = self.indices[self.i][0]

        indicator_pos = (start_pos_x + current_ind * offset, y_pos)
        indicator_size = (self.data_width, y_size)
        blackbox_pos = (0, y_pos)
        blackbox_size = (self.width, y_size)

        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=blackbox_pos, size=blackbox_size)

        with self.canvas:
            Color(204/255, 0, 204/255)  # violet
            Rectangle(pos=indicator_pos, size=indicator_size)

    def draw_black_above_rectangles(self):
        """
        Visually removes the indicator of the current index.
        :return: None
        """
        y_pos = self.start_pos_y + 10
        y_size = 20

        blackbox_pos = (0, y_pos)
        blackbox_size = (self.width, y_size)

        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=blackbox_pos, size=blackbox_size)

    def redraw_items(self, dt):

        n = len(self.heap_history[self.i])
        offset = self.offset_x - self.width / 2
        pos_x = int(self.width / 2 - self.data_width / 2 + offset)
        blackbox_size_x = int(n * (self.data_width + self.data_spacing))

        # redraw black screen
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(pos_x, self.start_pos_y), size=(blackbox_size_x, - 9 * self.standard_units))

        # draw rectangles and labels
        with self.canvas:
            for data_height in self.heap_history[self.i]:
                pos_x = int(self.width / 2 - self.data_width / 2 + offset)
                rectangle_size = (self.data_width, -dp(data_height))
                text_y = 8.4 * self.standard_units - dp(data_height)
                Color(0, 0, 1)
                self.rectangles.append(Rectangle(pos=(pos_x, self.start_pos_y), size=rectangle_size))
                self.labels.append(Label(pos=(pos_x, text_y), width=self.data_width,
                                         height=dp(-5), text=str(data_height), font_size=self.font_size_items,
                                         bold=True))
                offset += (self.data_width + self.data_spacing)

    def color_all(self):
        """
        Draws the rectangles on the board.
        :return: None
        """
        self.rectangles = []
        self.labels = []
        # redraw black screen
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0, self.start_pos_y), size=(self.width, - 9 * self.standard_units))

        # draw rectangles and labels
        offset = self.offset_x - self.width / 2
        with self.canvas:
            for data_height in self.items:
                pos_x = int(self.width / 2 - self.data_width / 2 + offset)
                rectangle_size = (self.data_width, -dp(data_height))
                text_y = 8.4 * self.standard_units - dp(data_height)
                Color(0, 0, 1)
                self.rectangles.append(Rectangle(pos=(pos_x, self.start_pos_y), size=rectangle_size))
                self.labels.append(Label(pos=(pos_x, text_y), width=self.data_width,
                                         height=dp(-5), text=str(data_height), font_size=self.font_size_items,
                                         bold=True))
                offset += (self.data_width + self.data_spacing)

    def indicate_redrawing(self, dt):
        """
        Changes color of the rectangles that are about to be exchanged.
        :param dt: float (time interval that the function is called in)
        :return: None
        """
        if self.i == len(self.indices):
            drawing_flow.unschedule_drawing()

        else:
            self.indicate_current_rect()

            old_ind, new_ind, old_val, new_val = self.indices[self.i][1:]

            offset = (self.data_width + self.data_spacing)
            start_pos_x = int((self.width / 2 - self.data_width / 2) - self.width / 2 + self.offset_x)

            old_pos = (start_pos_x + old_ind * offset, self.start_pos_y)
            old_size = (self.data_width, -dp(old_val))
            new_pos = (start_pos_x + new_ind * offset, self.start_pos_y)
            new_size = (self.data_width, -dp(new_val))

            with self.canvas:
                Color(0, 1, 1)
                self.rectangles[old_ind] = Rectangle(pos=old_pos, size=old_size)
                self.rectangles[new_ind] = Rectangle(pos=new_pos, size=new_size)

    def switch_items(self, old_ind, new_ind):
        """
        Switches items' indices.
        :param old_ind: int (old index)
        :param new_ind: int (new index)
        :return: None
        """
        store = self.items[old_ind]
        self.items[old_ind] = self.items[new_ind]
        self.items[new_ind] = store


class GuiApp(App):
    pass


Window.maximize()
GuiApp().run()
