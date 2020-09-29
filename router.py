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
                   'error': Functions.error,
                   'print_msg': Functions.print_msg}
        message = self.data_analysis(msg)
        url = message[0]
        args = message[1]
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

    def print_msg(self, msg):
        print(msg)

    def welcome_to_server(self):
        return 'welcome'

    def get_system_information(self):
        return platform.platform()
