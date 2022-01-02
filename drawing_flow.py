"""
Implements the drawing control flow to visually display the distinct elements of the drawing process.
"""

from kivy.clock import Clock

main_object = None


def call_draw_change(dt):
    """
    Calls the draw_change function in intervals at the appropriate speed.
    :param dt: float (time, required for Clock._ functions)
    :return: none
    """
    global main_object
    Clock.schedule_interval(main_object.draw_change, main_object.speed)


def call_redraw_items(dt):
    """
    Calls the redraw_items function in intervals at the appropriate speed.
    :param dt: float (time, required for Clock._ functions)
    :return: none
    """
    global main_object
    Clock.schedule_interval(main_object.redraw_items, main_object.speed)


def call_indicate_redrawing(dt):
    """
    Calls the indicate_redrawing function in intervals at the appropriate speed.
    :param dt: float (time, required for Clock._ functions)
    :return: none
    """
    global main_object
    Clock.schedule_interval(main_object.indicate_redrawing, main_object.speed)


def start_drawing(object):
    """
    Starts the drawing process.
    :param object: Instance of MainScreen class
    :return: none
    """
    global main_object
    main_object = object

    if object.is_heap_sort:
        Clock.schedule_once(call_redraw_items)
        Clock.schedule_once(call_indicate_redrawing, main_object.speed * 1/3)
        Clock.schedule_once(call_draw_change, main_object.speed * 2/3)
    else:
        Clock.schedule_once(call_indicate_redrawing)
        Clock.schedule_once(call_draw_change, main_object.speed * 1/2)


def unschedule_drawing():
    """
    Unschedules the drawing process.
    :return: none
    """
    Clock.unschedule(main_object.indicate_redrawing)
    Clock.unschedule(main_object.draw_change)

    main_object.draw_black_above_rectangles()
    main_object.draw_done()
    main_object.button_pressed = False
