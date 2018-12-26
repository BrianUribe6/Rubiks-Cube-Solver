from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder


kvcube = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<AndroidTabsBar>:
    canvas.before:
        Color:
            rgba: get_color_from_hex('#E87200')
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 0,0,0,.3
        Rectangle:
            pos: self.pos[0], self.pos[1] - 1
            size: self.size[0], 1
        Color:
            rgba: 0,0,0,.2
        Rectangle:
            pos: self.pos[0], self.pos[1] - 2
            size: self.size[0], 1
        Color:
            rgba: 0,0,0,.05
        Rectangle:
            pos: self.pos[0], self.pos[1] - 3
            size: self.size[0], 1
<MyTab>:
    canvas:
        Color:
            rgba: 0,0,0,0
    Button:
        text: root.text
    '''


class Tabs(BoxLayout, AndroidTabsBase):
    pass


class CubeSolverApp(App):
    def build(self):
        Builder.load_string(kvcube)
        android_tabs = AndroidTabs()

        solver_tab = Tabs(text='Solver')
        timer_tab = Tabs(text='Timer')

        android_tabs.add_widget(solver_tab)
        android_tabs.add_widget(timer_tab)

        return android_tabs


if __name__ == '__main__':
    CubeSolverApp().run()
