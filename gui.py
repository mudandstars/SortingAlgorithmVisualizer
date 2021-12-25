
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

        # lists
        self.items = []
        self.rectangles = []
        self.labels = []
        self.indices = []  # (current_ind, old_ind, new_ind) for every change
        self.alg_iter = {"Insertion Sort": 1, "Heapsort": 0}

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

        self.speed = 1

    def run_algorithm(self):
        """
        When the 'Run Algorithm' Button is pressed, this method is executed.
        It initialises the algorithm.
        :return: None
        """
        self.button_pressed = True
        self.call_algorithm()

    def call_algorithm(self):

        if self.selected_algorithm == "Selection Sort":
            return self.selection_sort()
        elif self.selected_algorithm == "Insertion Sort":
            return self.insertion_sort()
        elif self.selected_algorithm == "Shellsort":
            return self.shell_sort()
        elif self.selected_algorithm == "Merge Sort":
            return self.merge_sort()
        elif self.selected_algorithm == "Heapsort":
            return self.heapsort()
        elif self.selected_algorithm == "Quicksort":
            return self.quick_sort()

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
        # self.speed = 1 / self.slider_value

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

        # disables the calling of the indicate_redrawing function in time
        if self.i == len(self.indices):
            Clock.unschedule(self.indicate_redrawing)
            Clock.unschedule(self.indicate_redrawing)
            Clock.unschedule(self.draw_change)
            self.draw_black_above_rectangles()
            self.draw_done()
            self.button_pressed = False

        # if cancel condition is not met, continue
        else:
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
        if self.i == len(self.indices) - 1:
            self.unschedule_drawing()
        else:
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

    def draw_rectangles(self, dt):
        """
        Combines multiple methods to manage the visual drawing process.
        :param dt: float (time interval that the function is called in)
        :return: None
        """
        # draws on the board as long as conditions are met, else it ends the drawing process
        self.indicate_current_rect()
        self.draw_change()
        # disables the calling of the indicate_redrawing function in time

    def unschedule_drawing(self):
        Clock.unschedule(self.indicate_redrawing)
        Clock.unschedule(self.draw_rectangles)
        self.draw_black_above_rectangles()
        self.draw_done()
        self.button_pressed = False

    def call_redrawing(self, dt):
        """
        Method to call the drawing function. Necessary for Kivy time-dynamics-management.
        :param dt: float (time interval that the function is called in)
        :return: None
        """
        Clock.schedule_interval(self.draw_rectangles, self.speed)

    def call_redrawing_heap(self, dt):

        Clock.schedule_interval(self.redraw_items, self.speed)

    def call_indicating(self, dt):

        Clock.schedule_interval(self.indicate_redrawing, self.speed)

    def call_change_heap(self, dt):

        Clock.schedule_interval(self.draw_change, self.speed)

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

    def selection_sort(self):
        """
        Selection sort algorithm that is augmented to also visualize the process.
        :return: None
        """
        self.indices = []  # i, old_ind, new_ind, old_val, new_val
        self.i = 0
        start_unsorted = 0

        Clock.schedule_once(self.call_indicating)
        Clock.schedule_once(self.call_redrawing, self.speed / 2)

        while start_unsorted < len(self.items):
            smallest_element = self.items[start_unsorted]
            for i in range(start_unsorted + 1, len(self.items)):
                if self.items[i] < smallest_element:
                    self.indices.append((start_unsorted, start_unsorted, i, self.items[start_unsorted], self.items[i]))
                    smallest_element = self.items[i]
                    self.items[i] = self.items[start_unsorted]
                    self.items[start_unsorted] = smallest_element

            start_unsorted += 1

    # todo: ends drawing process one step too early

    def insertion_sort(self):
        """
        Insertion sort algorithm that is augmented to also visualize the process.
        :return: None
        """
        self.indices = []  # i, old_ind, new_ind, old_val, new_val
        self.i = 0

        # this indicates rectangles that are about to be changed just before changing them
        Clock.schedule_once(self.call_indicating)
        Clock.schedule_once(self.call_redrawing, self.speed / 2)

        i = 1
        while i < len(self.items):
            j = i
            while j > 0 and self.items[j - 1] > self.items[j]:

                self.indices.append((i, j - 1, j, self.items[j - 1], self.items[j]))

                print(self.items)
                print(self.indices[-1])
                # swap elements if they are not in order
                self.switch_items(j - 1, j)
                # repeat for each element in the sorted list (left part of array)
                j -= 1

            # go one step to the right and repeat
            i += 1

    def shell_sort(self):
        """
        Shellsort algorithm augmented to also visualize the process.
        :return: None
        """
        # use Ciura gap sequence
        gaps = [701, 301, 132, 57, 23, 10, 4, 1]

        self.indices = []  # i, old_ind, new_ind, old_val, new_val
        self.i = 0

        # this indicates rectangles that are about to be changed just before changing them
        Clock.schedule_once(self.call_indicating)
        Clock.schedule_once(self.call_redrawing, self.speed / 2)

        # start with largest gap and work down to gap of 1
        for gap in gaps:
            offset = 0
            # offset is iterating through the list by 1 step at a time
            while offset < gap:
                i = offset
                # i is iterating through the list, starting with offset and incremented by the gap-value every iteration
                while i < len(self.items):
                    # the current value of list[i] is saved temporarily
                    temp = self.items[i]
                    j = i
                    # j starts at i and decreases by the gap-value each iteration.
                    # j serves to shift earlier gap-sorted elements up until the correct location for list[i] is found
                    while j >= gap and self.items[j - gap] > temp:

                        self.indices.append((offset, j - gap, j, self.items[j- gap], self.items[j]))
                        print(gap)
                        print(self.items)
                        print(self.indices[-1])

                        self.items[j] = self.items[j - gap]
                        j -= gap
                        self.items[j] = temp

                    i += gap
                offset += 1

    def heapsort(self):
        """
        Heapsort algorithm augmented to also visualize the process.
        :return: None
        """
        heapq._heapify_max(self.items)
        count = 0
        length = len(self.items)
        self.indices = []
        self.heap_history = []
        self.i = 0

        # call redrawing
        Clock.schedule_once(self.call_redrawing_heap)
        # call indicating
        Clock.schedule_once(self.call_indicating, self.speed/3)
        # call change
        Clock.schedule_once(self.call_change_heap, (2*self.speed)/3)

        new_ind = length - 1
        while count < length:
            count += 1
            list_subdivision = length - count

            unsorted_part = self.items[:list_subdivision + 1]
            self.heap_history.append(unsorted_part)
            self.indices.append((list_subdivision, 0, list_subdivision, self.items[0], self.items[list_subdivision]))

            # remove the biggest value and insert it at after the end of the unsorted part of the list
            root = self.items.pop(0)
            self.items.insert(new_ind, root)

            # subdivide list and and restore heap property of unsorted part before merging the lists back together
            unsorted_part = self.items[:list_subdivision]
            sorted_part = self.items[list_subdivision:]
            heapq._heapify_max(unsorted_part)
            unsorted_part.extend(sorted_part)
            self.items = unsorted_part
            new_ind -= 1


class GuiApp(App):
    pass


Window.maximize()
GuiApp().run()
