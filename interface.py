from kivy.app import App
from kivy.uix.widget import Widget


class CubeSolver(Widget):
    pass


class CubeSolverApp(App):
    def build(self):
        return CubeSolver()


if __name__ == '__main__':
    CubeSolverApp().run()
