import json
import platform


class SimpleRouter:
    def data_analysis(self, msg):
        msg = json.loads(msg)
        try:
            url = msg['url']
            if 'args' in msg:
                args = msg['args']
                return url, args
            else:
                return url, None
        except KeyError:
            return 'Ошибка в структуре json'

    def execute(self, msg):
        methods = {'get_system_information': Functions.get_system_information,
                   'welcome_to_server': Functions.welcome_to_server,
                   'error': Functions.error}
        url, *args = self.data_analysis(msg)
        if url in methods:
            if args:
                return methods[url](Functions, *args)
            else:
                return methods[url](Functions)
        else:
            return 'Такого метода не существует'


class Functions:
    def error(self):
        return 'error'

    def welcome_to_server(self):
        return 'welcome'

    def get_system_information(self):
        return platform.platform()
