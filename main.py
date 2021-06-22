from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from modules.pets import Pets


class BMIScreen(Screen):
    pass


class DatabaseScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        builder = Builder.load_file('main.kv')
        self.pets = Pets()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.pets)
        return builder


Test().run()