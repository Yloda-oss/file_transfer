import json

import config
from ftp_server_class import FtpClient
from host_finder import HostFinder
from server_class import Client


class ClientFunction:
    def __init__(self):
        self.server_ip = self.get_server_ip()
        self.client = self.connect_to_server(self.get_server_ip())
        self.Ftp_client = self.connect_to_ftp_server()

    def get_server_ip(self):
        hostfinder = HostFinder()
        self.server_ip = hostfinder.get_server()
        return self.server_ip

    def _determine_file_type(file):
        try:
            import magic
            return magic.from_file(file, mime=True).split('/')[0]
        except ImportError:
            from winmagic import magic as winmagic
            return winmagic.from_file(file, mime=True).split('/')[0]

    def _jsonization(self, url: str, *args):
        if args:
            string = {
                'url': url,
                'args': args
            }
        else:
            string = {
                'url': url
            }
        return json.loads(string)

    def get_client_server(self):
        hostfinder = HostFinder()
        return hostfinder.ip

    def connect_to_server(self, ip):
        try:
            client = Client(ip, config.PORT)
            if 'welcome' == client.receive(self._jsonization('welcome_to_server')):
                return client
            else:
                return False
        except:
            return False

    def send(self, msg):
        try:
            self.client.send(msg)
            return True
        except:
            return False

    def receive(self):
        return self.client.receive()

    def connect_to_ftp_server(self):
        FTP_client = FtpClient(self.server_ip, config.FTP_PORT, config.FTP_USER, config.FTP_PASSWORD)
        FTP_client.connect_to_ftp_server()
        return FTP_client

    def get_information_of_files(self):
        return self.Ftp_client.get_information_of_files()

    def change_directory(self, directory):
        self.Ftp_client.change_directory(directory)
        return True

    def get_list_files(self):
        return self.Ftp_client.get_list_files()

    def download_file(self, file):
        self.Ftp_client.download_file(file)
        return True

    def upload_file(self, file):
        file_type = self._determine_file_type(file)
        self.Ftp_client.upload_file(file, file_type)
