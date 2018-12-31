from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.camera import Camera
from kivy.uix.actionbar import ActionBar
import Cube


class CubeSolver(BoxLayout):

    scramble = StringProperty(Cube.scramble())
    time = NumericProperty(0)
    running = False

    def __init__(self, **kwargs):
        super(CubeSolver, self).__init__(**kwargs)

    def tick(self, dt):
        """Gets Delta time from the CLock object and adds it to the time"""
        self.time+= dt

    def start(self):
        if not self.running:
            self.running = True
            # Resetting the timer before starting again
            self.time = 0
            # Starting the timer
            Clock.schedule_interval(self.tick, 0.01)
        else:  # Timer already running, so stop the time
            self.running = False
            self.stop()
            # Get a new Scramble
            Clock.schedule_once(self.set_scramble)

    def stop(self):
        Clock.unschedule(self.tick)

    def set_scramble(self, *args):
        self.scramble = Cube.scramble()


class Tab(BoxLayout, AndroidTabsBase):
    """This is used to create a Tab"""
    pass


class CubeSolverApp(App):
    def build(self):
        cube_solver = Builder.load_file('CubeSolver.kv')
        return cube_solver


if __name__ == '__main__':
    CubeSolverApp().run()
