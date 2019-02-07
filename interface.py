from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
# from kivy.uix.camera import Camera
from datetime import timedelta
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.recycleview import RecycleView
import Cube
import pickle


# Esta variable es para acceder a los metodos de la clase
Cubo = Cube.Cube()
database_name = ".database.times"


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
        self.padding = [5, 5]
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


class Manager(ScreenManager):
    main_screen = ObjectProperty(None)
    historial = ObjectProperty(None)
    pass


class Main(Screen):
    pass


class Historial(Screen):
    pass


class MainLayout(BoxLayout):
    manager = ObjectProperty(None)
    sm = ScreenManager()
    sm.add_widget(Historial(name='hist'))
    sm.add_widget(Main(name='main'))


class Timer(BoxLayout, AndroidTabsBase):
    """Contains the timer and all the functions necessary to start/ stop timer, generate scramble
    and image representation showing the 6 faces of a Rubik's Cube after executing a particular scramble."""

    faces = Faces()
    scramble = StringProperty(Cubo.shuffle())
    database = load(database_name)
    time = NumericProperty(0)
    timer_button = StringProperty('atlas://resources/images/elements/play')
    time_stop = 0
    running = False

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
            write(self.database, database_name)
            # Stop timer by removing the event from the scheduler
            Clock.unschedule(self.tick)
            # Get a new Scramble and play/stop button's root direction
            Clock.schedule_once(self.set_scramble)
            Clock.schedule_once(self.get_button)
            # Clock.schedule_once(UserStats().add_time(layout, self.scramble, self.time_format(self.time)))

    def get_button(self, *args):
        """Renders the play/stop button based on the timer's state(Running/ stopped)"""
        pause_button = 'atlas://resources/images/elements/stop'
        play_button = 'atlas://resources/images/elements/play'
        if self.running:
            self.timer_button = pause_button
        else:
            self.timer_button = play_button

    def set_scramble(self, *args):
        """Moves lists containing """
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
            return str(timedelta(seconds=time))[3:10]  # string was sliced to show the time in the format 00:00.00
        # Time is in hours
        elif day > time >= hour:
            return str(timedelta(seconds=time))[:10] # string was sliced to show the time in the format 00:00:00.00
        # Time is in days
        elif time >= day:
            return str(timedelta(seconds=time))
        # Time is in seconds
        return str(timedelta(seconds=time))[5:10]  # string was sliced to show the time in the format 00.00


class Solver(BoxLayout, AndroidTabsBase):
    pass


class ItemList(BoxLayout):
    pass


class ColStats(BoxLayout):
    '''Para posicionar los elementos en columnas'''
    pass


class TimeEntry(BoxLayout):
    """"Contains an horizontal line of widgets that displays the time and scramble of each solve. It also
     contains the number correspondent to each value and helpful widgets to eliminate an specific time from
     the historial, and a popup window that also displays the time and scramble"""
    pass


class TimesList(RecycleView):
    def __init__(self, **kwargs):
        """"Deploys a list of TimeEntry from database"""
        super(TimesList, self).__init__(**kwargs)
        database = load(database_name)
        self.data = [{'text': time + ' ' + scramble} for scramble, time in database.items()]


# class TestLayout(BoxLayout):
#     pass


class CubeSolverApp(App):

    def build(self):
        return MainLayout()

    @ staticmethod
    def clear_database():
        """"Clears the dictionary  in .database.times This method can be referenced through the CubeSolver.kv by
        using app.clear_database"""
        database = load(database_name)
        database.clear()
        write(database, database_name)


if __name__ == '__main__':
    CubeSolverApp().run()
