import json
from mimetypes import MimeTypes

import config
from ftp_server_class import FtpClient
from host_finder import HostFinder
from server_class import Client


class ClientFunction:
    def get_server_ip(self):
        self.hostfinder = HostFinder()
        self.server_ip = self.hostfinder.get_server()
        return self.server_ip

    def _determine_file_type(self, file):
        magic = MimeTypes()
        type_ = magic.guess_type(file)
        if type_[0]:
            return type_[0].split('/')[0]
        else:
            return 'file'

    def _jsonization(self, url: str, *args):
        string = {
            'url': url
        }
        if args:
            string['args'] = args
        return json.dumps(string)

    def connect_to_server(self):
        try:
            client = Client(self.server_ip, config.PORT)
            client.send(self._jsonization(url='welcome_to_server'))
            if 'welcome' == client.receive():
                print('Yes!')
                self.client = client
            else:
                return False
        except:
            return False

    def send(self, msg):
        try:
            self.client.send(self._jsonization(msg))
            return True
        except:
            return False

    def receive(self):
        return self.client.receive()

    def connect_to_ftp_server(self):
        FTP_client = FtpClient(self.server_ip, config.FTP_PORT, config.FTP_USER, config.FTP_PASSWORD)
        FTP_client.connect_to_ftp_server()
        self.Ftp_client = FTP_client

    def get_information_of_files(self):
        return self.Ftp_client.get_information_of_files()

    def change_directory(self, directory):
        self.Ftp_client.change_directory(directory)

    def get_list_files(self):
        return self.Ftp_client.get_list_files()

    def download_file(self, file):
        self.Ftp_client.download_file(file)

    def upload_file(self, file):
        file_type = self._determine_file_type(file)
        self.Ftp_client.upload_file(file, file_type)
