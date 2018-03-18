import kivy

kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.button import Label


# Inherit Kivy's App class which represents the window
# for our widgets
# HelloKivy inherits all the fields and methods
# from Kivy
class testk2(App):

    # This returns the content we want in the window
    def build(self):
        # Return a label widget with Hello Kivy
        # The name of the kv file has to be hellokivy
        # minus the app part from this class to
        # match up properly
        return Label()


hello_kivy = testk2()
hello_kivy.run()