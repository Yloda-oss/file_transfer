import gc
import os

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget, ImageLeftWidget
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar

from client_functions import ClientFunction
from file_manager import FileManagerLocal


class RV(RecycleView):
    def update(self):
        def __return_icon(type_):
            icons = {'application': 'application',
                     'audio': 'file-music',
                     'music': 'file-music',
                     'image': 'image',
                     'message': 'android-message',
                     'model': 'video-3d',
                     'multipart': 'email',
                     'text': 'text',
                     'video': 'video',
                     'directory': 'folder',
                     'file': 'file',
                     'PermissionError': 'alert-octagon'}
            if type_ in icons:
                return icons[type_]
            else:
                return icons['file']

        files = app.file_manager.get_files_list()
        self.data = [{'path': str(file[0]),
                      'type': str(file[1]),
                      'text': str(os.path.basename(file[0])),
                      'icon': __return_icon(type_=file[1])}
                     for file in files]


class IconFile(IconLeftWidget, ImageLeftWidget):
    def __init__(self, **kwargs):
        if self.parent.type == 'image':
            kwargs['image'] = self.parent.type
            kwargs['icon'] = None
        super(IconFile, self).__init__(**kwargs)


class ListItemFile(OneLineIconListItem, TouchBehavior):
    type = StringProperty()
    icon = StringProperty()
    path = StringProperty()
    text = StringProperty()

    def on_release(self):
        if self.type == 'directory':
            app.file_manager.edit_current_dir(self.text)
            app.root.ids.fscreen.update_list_files()
        else:
            pass

    def on_long_touch(self, *args):
        self.return_info()

    def return_info(self):
        return {'type': self.type, 'path': self.path, 'icon': self.icon, 'text': self.text}


class Toolbar(MDToolbar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ObjectProperty()

    def set_screen_from_toolbar(self, new_screen, direction='left'):
        self.screen_manager.current = new_screen
        self.screen_manager.transition.direction = direction


class MainScreen(Screen):
    pass


class FScreen(Screen):
    list_with_files = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

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


class ChooseScreenButton(RaisedButton):
    text = StringProperty()

    def choose_screen(self):
        app.file_manager.edit_current_dir(app.file_manager.paths[self.text])
        app.root.ids.fscreen.__self__.update_list_files()
        app.root.ids.screen_manager.__self__.current = "file_manager"


class TestNavigationDrawer(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = FileManagerLocal()
        self.client = ClientFunction()

    def build(self):
        return Builder.load_file('main.kv')

    def on_start(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE])
        except ImportError:
            pass
        Clock.schedule_interval(lambda dt: print(int(Clock.get_fps())), 0.1)


app = TestNavigationDrawer()
gc.collect()
app.run()
