from kivy.app import App
from kivy.garden.androidtabs import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.camera import Camera
from kivy.uix.actionbar import ActionBar

kvcube = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
BoxLayout:
    orientation: 'vertical'
    ActionBar:
        pos_hint: {'top':1}
        background_image: '/resources/images/background.png'
        background_color: get_color_from_hex('#E87200')
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Action Bar'
                with_previous: False
            ActionOverflow:
                # overflow_image: '/resources/images/menu.png'
                # overflow_color: 0,0,0,1
                ActionButton:
                    text: "Help"
                ActionButton:
                    text: "About"    
    AndroidTabs:
        Tab:
            text: "TIMER"
            orientation: 'vertical'
            Label:
                text: '00:00.00'#str(root.number)[:5]
                font_size: 50
            Button:
                # background_color: 0,0,0,0
                size: self.size
                pos: self.pos
                # on_release: root.start()
        Tab:
            text: "SOLVER"
            # Label:
            #     text: "Hello2"

<AndroidTabsBar>:
    canvas.before:
        Color:
            rgba: get_color_from_hex('#E87200')
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 0.86,0.86,0.86,1
        Rectangle:
            pos: self.pos[0], self.pos[1] 
            size: self.size[0], 1
        Rectangle:
            pos: self.pos[0], self.pos[1] 
            size: self.size[0], 1
        Rectangle:
            pos: self.pos[0], self.pos[1] 
            size: self.size[0], 1
<Tab>:
    canvas:
        Color:
            rgba: 0.86,0.86,0.86,1
        Rectangle:
            size: self.size
            pos: self.pos
        
    '''


# class MyTabs(AndroidTabs):
#     """Contiene las pestañas y se encargada de toda la actividad dentro de las mismas"""
#     number = NumericProperty(0)
#     running = False
#
#     def __init__(self, **kwargs):
#         super(MyTabs, self).__init__(**kwargs)
#
#     def tick(self, dt):
#         self.number += dt
#
#     def start(self):
#         if not self.running:
#             self.running = True
#             self.number = 0
#             Clock.schedule_interval(self.tick, 0.01)
#         else:
#             self.running = False
#             self.stop()
#
#     def stop(self):
#         Clock.unschedule(self.tick)


class Tab(BoxLayout, AndroidTabsBase):
    """This is used to create a Tab"""
    pass


class CubeSolverApp(App):
    def build(self):
        cube_solver= Builder.load_string(kvcube)

        return cube_solver


if __name__ == '__main__':
    CubeSolverApp().run()
