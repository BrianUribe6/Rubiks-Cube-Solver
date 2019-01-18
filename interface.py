from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, DictProperty
# from kivy.uix.camera import Camera
from datetime import timedelta
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import Cube
import pickle


# Esta variable es para acceder a los metodos de la clase
Cubo = Cube.Cube()


def write(info, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(info, f)


def load(file_name):
    with open(file_name, 'rb') as f:
        info = pickle.load(f)
    return info


class Face(GridLayout):
    """Agrega """
    pieces = StringProperty('')

    def __init__(self, **kwargs):
        super(Face, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.padding = [18, 5]
        self.spacing = [3, 3]
        # Para forzar las piezas a un tamaño especifico
        self.row_force_default = True
        self.row_default_height = 12
        self.col_force_default = True
        self.col_default_width = 12

        for i in self.pieces:
            self.add_widget(Image(source='atlas://resources/images/elements/Piece_' + i))


class Faces(BoxLayout):
    """Dibuja todas las caras"""

    def __init__(self, **kwargs):
        super(Faces, self).__init__(**kwargs)
        self.orientation = 'horizontal'

    def draw_face(self):
        cube_state = Cubo.kociemba_state()

        for i in range(6):
            cara = Face(pieces=cube_state[i * 9: (i + 1) * 9])
            self.add_widget(cara)


class CubeSolver(BoxLayout):
    faces = Faces()
    scramble = StringProperty(Cubo.shuffle())
    time = NumericProperty(0)
    database = load('.database.times')
    timer_button = StringProperty('atlas://resources/images/elements/play')
    # Guarda el tiempo cuando pausas el timer
    time_stop = 0
    running = False
    database_name = ".database.times"

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
            # self.database.clear()
            write(self.database, self.database_name)
            # Stop timer by removing the event from the scheduler
            Clock.unschedule(self.tick)
            # Get a new Scramble and play/stop button's root direction
            Clock.schedule_once(self.set_scramble)
            Clock.schedule_once(self.get_button)
            # Clock.schedule_once(UserStats().add_time(layout, self.scramble, self.time_format(self.time)))

    def get_button(self, *args):
        pause_button = 'atlas://resources/images/elements/stop'
        play_button = 'atlas://resources/images/elements/play'
        if self.running:
            self.timer_button = pause_button
        else:
            self.timer_button = play_button

    def set_scramble(self, *args):
        self.scramble = Cubo.shuffle()

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


class ItemList(BoxLayout):
    pass


class UserStats(TabbedPanel):
    def __init__(self, **kwargs):
        super(UserStats, self).__init__(**kwargs)
        database = load('.database.times')
        historial_panel = TabbedPanelItem(text='Historial',
                                          background_down='atlas://resources/images/elements/tabs',
                                          background_normal='atlas://resources/images/elements/none')
        layout = BoxLayout(orientation='vertical')
        # for scramble, time in database.items():
        #     add_time(scramble, time)

        historial_panel.add_widget(layout)
        self.add_widget(historial_panel)

    # def add_time(self):


class CubeSolverApp(App):
    def build(self):
        cube_solver = Builder.load_file('CubeSolver.kv')
        return cube_solver


if __name__ == '__main__':
    CubeSolverApp().run()
