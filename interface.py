from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, DictProperty
# from kivy.uix.camera import Camera
from datetime import timedelta
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
# from kivy.atlas import Atlas
from kivy.config import Config
import Cube


# Colores de las piezas
# Color = {
#     'U': [1, 1, 1, 1], 'L': [.95, .61, .07, 1], 'F': [.02, .65, .42, 1],
#     'R': [.91, .34, .34, 1], 'B': [0, .69, .94, 1], 'D': [1, 1, .31, 1]
# }

Piece = {}


class CubeSolver(BoxLayout):

    scramble = StringProperty(Cube.scramble())
    database = DictProperty()
    time = NumericProperty(0)
    timer_button = StringProperty('atlas://resources/images/elements/play')
    # Guarda el tiempo cuando pausas el timer
    time_stop = 0
    running = False

    def __init__(self, **kwargs):
        super(CubeSolver, self).__init__(**kwargs)

    def tick(self, dt):
        """Gets Delta time from the CLock object and adds it to the time"""
        self.time = round(self.time + dt, 2)

    def start(self):
        if not self.running and self.time_stop == 0:
            self.running = True
            # Resetting the timer before starting again
            self.time = 0
            # Starting the timer
            Clock.schedule_interval(self.tick, 0.01)
            Clock.schedule_once(self.get_button)
        else:
            # Resetea el tiempo en stop
            self.time_stop = 0

    def stop(self):
        if self.running:
            # Timer already running, so stop the time
            self.running = False
            # Guarda el tiempo del timer cuando
            self.time_stop = self.time
            # Save time and scramble to database
            self.database[self.scramble] = self.time_format(self.time)
            # Stop timer by removing the event from the scheduler
            print(self.database)
            Clock.unschedule(self.tick)
            # Get a new Scramble and play/stop button's root direction
            Clock.schedule_once(self.set_scramble)
            Clock.schedule_once(self.get_button)

    def get_button(self, *args):
        pause_button = 'atlas://resources/images/elements/stop'
        play_button = 'atlas://resources/images/elements/play'
        if self.running:
            self.timer_button = pause_button
        else:
            self.timer_button = play_button

    def set_scramble(self, *args):
        self.scramble = Cube.scramble()

    @staticmethod
    def time_format(time):
        """Converts and integer or floating-point number into standardized time format 00:00:00"""
        minute = 60
        hour = 3600
        day = hour * 24
        if time == 0:
            return "00.00"
        # Time is in minutes
        elif hour > time >= minute:
            return str(timedelta(seconds=time))[3:10]
        # Time is in hours
        elif day > time >= hour:
            return str(timedelta(seconds=time))[:10]
        # Time is in days
        elif time >= day:
            return str(timedelta(seconds=time))
        # Time is in seconds
        return str(timedelta(seconds=time))[5:10]


class Tab(BoxLayout, AndroidTabsBase):
    """This is used to create a Tab"""
    pass


class UserStats(TabbedPanel):
    pass


class Face(GridLayout):
    """Esta es para mostrar los stats """
    cube_state = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'  # Ejemplo de un cubo desarmado
    center_color = StringProperty()

    def __init__(self, **kwargs):
        super(Face, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.padding = [5, 5]
        self.spacing = [2, 5]
        # Para forzar las piezas a un tamaño especifico
        self.row_force_default = True
        self.row_default_height = 20
        self.col_force_default = True
        self.col_default_width = 20

        if self.center_color == 'White':
            for color in self.cube_state[0: 9]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))
        elif self.center_color == 'Red':
            for color in self.cube_state[9: 18]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))
        elif self.center_color == 'Green':
            for color in self.cube_state[18: 27]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))
        elif self.center_color == 'Yellow':
            for color in self.cube_state[27: 36]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))
        elif self.center_color == 'Orange':
            for color in self.cube_state[36: 45]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))
        elif self.center_color == 'Blue':
            for color in self.cube_state[45:]:
                self.add_widget(Button(text=' ', background_normal='atlas://resources/images/elements/Piece_' + color))


class CubeFaces(BoxLayout):
    def __init__(self, **kwargs):
        super(CubeFaces, self).__init__(**kwargs)
        self.padding = [self.width * .025, 0]
        self.add_widget(Face(center_color='White'))
        self.add_widget(Face(center_color='Red'))
        self.add_widget(Face(center_color='Green'))
        self.add_widget(Face(center_color='Yellow'))
        self.add_widget(Face(center_color='Orange'))
        self.add_widget(Face(center_color='Blue'))


class CubeSolverApp(App):
    def build(self):
        cube_solver = Builder.load_file('CubeSolver.kv')

        return cube_solver


if __name__ == '__main__':
    CubeSolverApp().run()
