from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from logic import ProductManagement
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')


Window.size = (480, 880)


class HomePage(Screen):
    pass


class Search(Screen):
    text_input = ObjectProperty()
    retail = ObjectProperty()
    wholesale = ObjectProperty()
    stock = ObjectProperty()
    distant = ObjectProperty()
    good_name = ObjectProperty()

    def search(self):
        try:
            name_item = self.text_input.text
            item = ProductManagement.search_item(name_item)
            id, name, retail, wholesale = item
            self.good_name.text = name
            self.retail.text = str(retail)
            self.wholesale.text = str(wholesale)

            stock, distant_stock = ProductManagement.find_locate(self, id)
            self.stock.text = stock
            self.distant.text = distant_stock

        except TypeError:
            self.good_name.text = 'This goods not found'
            self.retail.text = ''
            self.wholesale.text = ''
            self.stock.text = ''
            self.distant.text = ''


class AddItem(Screen):
    item_name = ObjectProperty()
    retail_price = ObjectProperty()
    wholesale_price = ObjectProperty()
    near_stock = ObjectProperty()
    distant_stock = ObjectProperty()
    empty_field = ObjectProperty()

    def new_item(self):
        try:
            name = self.item_name.text
            retail = int(self.retail_price.text)
            wholesale = int(self.wholesale_price.text)
            stock = self.near_stock.text
            distant = self.distant_stock.text
            ProductManagement().add_item(name, retail, wholesale, stock, distant)
        except ValueError:
            self.empty_field.text = 'Item name, Retail price Wholesale \n' \
                                   ' price must be filled'

    def clear_text_input(self):
        self.item_name.text = ""
        self.retail_price.text = ""
        self.wholesale_price.text = ""
        self.near_stock.text = ""
        self.distant_stock.text = ""

    def clear_empty(self):
        self.empty_field.text = ''


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('store.kv')


class StoreApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    StoreApp().run()
