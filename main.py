"""
Runs the software.
"""
from kivy.core.window import Window
import gui
from gui import GuiApp


if __name__ == "__main__":

    Window.maximize()
    GuiApp().run()
