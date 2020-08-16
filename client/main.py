import gc
import os
from time import sleep
from threading import Thread
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar

from file_manager import FileManagerLocal




class RV(RecycleView):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.update()

    def update(self):
        def __return_icon(type):
            icons = {'application': 'application',
                     'audio': 'file-music',
                     'music': 'music',
                     'image': 'image',
                     'message': 'android-message',
                     'model': 'video-3d',
                     'multipart': 'email',
                     'text': 'text',
                     'video': 'video',
                     'directory': 'folder',
                     'file': 'file',
                     'PermissionError': 'alert-octagon'}
            if type in icons:
                return icons[type]
            else:
                return icons['file']

        files = app.file_manager.get_files_list()
        self.data = [{'path': str(file[0]), 'type': str(file[1]), 'text': str(os.path.basename(file[0])),
                      'icon': __return_icon(file[1])} for file in files]
        print(self.data)


class ListItemFile(RecycleDataViewBehavior, OneLineIconListItem):
    icon = StringProperty()
    path = StringProperty()
    type = StringProperty()
    text = StringProperty()

    def on_release(self):
        print(self.return_info())
        if self.type == 'directory':
            app.file_manager.edit_current_dir(self.text)
            app.root.ids.fscreen.update_list_files()
        else:
            print(self.type)

    def return_info(self):
        return [self.type, self.path, self.icon, self.text]


class Toolbar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ObjectProperty()

    def set_screen_from_toolbar(self, new_screen, direction='left'):
        self.screen_manager.current = new_screen
        self.screen_manager.transition.direction = direction


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class FScreen(Screen):
    list_with_files = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.files_inside = False

    def update_list_files(self):
        self.list_with_files.update()

    def current_directory_up(self):
        up_dir = app.file_manager.current_dir.parent
        app.file_manager.edit_current_dir(up_dir)
        self.update_list_files()

    def directory_come_back(self):
        if app.file_manager.history_navigation:
            app.file_manager.come_back()
            self.update_list_files()


class RaisedButton(MDRaisedButton):
    pass


class TestNavigationDrawer(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = FileManagerLocal()

    def build(self):
        return Builder.load_file('main.kv')



def enable_garbage_collector():
    sleep(10)
    gc.enable()

gc.disable()
Thread(target=enable_garbage_collector, daemon=True).start()
app = TestNavigationDrawer()
app.run()
