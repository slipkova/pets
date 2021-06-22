from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from modules.db import Db, Animal, Pet


class AnimalContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

class AnimalDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super(AnimalDialog, self).__init__(
            type="custom",
            content_cls=AnimalContent(),
            title='Nový druh',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        animal = Animal()
        animal.name = self.content_cls.ids.animal_name.text
        app.pets.database.create_animal(animal)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PetContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super(PetContent, self).__init__(*args, **kwargs)
        if id:
            pet = vars(app.pets.database.session.query(Pet).get(id))
        else:
            pet = {"id":"", "name":"", "animal": ""}

        self.ids.pet_name.text = pet['name']
        animals = app.pets.database.read_animals()
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{animal.name}", "on_release": lambda x=f"{animal.name}": self.set_item(x)} for animal in animals]
        self.menu_animals = MDDropdownMenu(
            caller=self.ids.animal_item,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        print(pet)
        self.ids.animal_item.set_item(pet['animal_name'])
        self.ids.animal_item.text = pet['animal_name']

    def set_item(self, text_item):
        self.ids.animal_item.set_item(text_item)
        self.ids.animal_item.text = text_item
        self.menu_animals.dismiss()


class PetDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(PetDialog, self).__init__(
            type="custom",
            content_cls=PetContent(id=id),
            title='Záznam mazlíčka',
            text='Ahoj',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        pet = {}
        pet['name'] = self.content_cls.ids.pet_name.text
        pet['animal'] = self.content_cls.ids.animal_item.text
        if self.id:
            pet["id"] = self.id
            app.pets.update(pet)
        else:
            app.pets.create(pet)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__(*args, **kwargs)
        self.id = item['id']
        self.text = item['name']
        self.secondary_text = item['animal_name']
        self._no_ripple_effect = True
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):

        self.dialog = PetDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):

        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.pets.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Pets(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Pets, self).__init__(orientation="vertical", *args, **kwargs)
        global app
        app = App.get_running_app()

        scrollview = ScrollView()
        self.list = MDList()
        self.database = Db(dbtype='sqlite', dbname='pets.db')
        print(self.database.session.query(Animal).all())
        print(self.database.read_animals())
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        new_pet_btn = MDFillRoundFlatIconButton()
        new_pet_btn.text = "Nový mazlíček"
        new_pet_btn.icon = "plus"
        new_pet_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_pet_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_pet_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_pet_btn.font_style = "Button"
        new_pet_btn.pos_hint = {"center_x": .5}
        new_pet_btn.on_release = self.on_create_pet
        button_box.add_widget(new_pet_btn)
        new_animal_btn = MDFillRoundFlatIconButton()
        new_animal_btn.text = "Nový druh"
        new_animal_btn.icon = "plus"
        new_animal_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_animal_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_animal_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_animal_btn.font_style = "Button"
        new_animal_btn.pos_hint = {"center_x": .6}
        new_animal_btn.on_release = self.on_create_animal
        button_box.add_widget(new_animal_btn)
        self.add_widget(button_box)


    def rewrite_list(self):

        self.list.clear_widgets()
        pets = self.database.read_all()
        print(pets)
        for pet in pets:

            self.list.add_widget(MyItem(item=vars(pet)))


    def on_create_pet(self, *args):
        self.dialog = PetDialog(id=None)
        self.dialog.open()

    def on_create_animal(self, *args):

        self.dialog = AnimalDialog()
        self.dialog.open()

    def create(self, pet):

        create_pet = Pet()
        create_pet.name = pet['name']
        create_pet.animal = self.database.session.query(Animal).get(pet['animal'])
        self.database.create(create_pet)
        self.rewrite_list()


    def update(self, pet):

        update_pet = self.database.read_by_id(pet['id'])
        update_pet.name = pet['name']
        update_pet.animal = self.database.session.query(Animal).get(pet['animal'])
        self.database.update()
        self.rewrite_list()

    def delete(self, id):

        self.database.delete(id)
        self.rewrite_list()