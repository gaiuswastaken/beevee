# main_app.py
from kivymd.app import MDApp
from kivy.uix.label import Label

def mainapp():
    class MainApp(MDApp):
        def build(self):
            return Label(text="Main App Running", halign="center")

    #if __name__ == "__main__":
    MainApp().run()