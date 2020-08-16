#from pathlib import Path
from ftplib import FTP
import multiprocessing
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class FtpServer:
    def __init__(self, lhost, port, username, password):
        self.host = lhost
        self.port = port
        self.username = username
        self.password = password

    def start_ftp_server(self):
        # Instantiate a dummy authorizer for managing 'virtual' users
        authorizer = DummyAuthorizer()
        # Define a new user having full r/w permissions and a read-only
        # anonymous user
        authorizer.add_user(self.username, self.password, '.', perm='elradfmwMT')
        #authorizer.add_anonymous(Path.cwd())

        # Instantiate FTP handler class
        handler = FTPHandler
        handler.authorizer = authorizer

        # Specify a masquerade address and the range of ports to use for
        # passive connections.  Decomment in case you're behind a NAT.
        # handler.masquerade_address = '151.25.42.11'
        # handler.passive_ports = range(60000, 65535)

        # Instantiate FTP server class and listen on 0.0.0.0:2121
        address = (self.host, self.port)
        self.server = FTPServer(address, handler)

        # set a limit for connections
        self.server.max_cons = 256
        self.server.max_cons_per_ip = 5

        # start ftp server
        self.server.serve_forever()

    def stop_ftp_server(self):
        self.server.close_all()

    def run(self):
        p = multiprocessing.Process(target=self.start_ftp_server)
        p.start()

class FtpClient:
    def __init__(self, rhost, port, username, password):
        self.host = rhost
        self.port = port
        self.username = username
        self.password = password
        self.ftp = FTP()

    def connect_to_ftp_server(self):
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)

    def stop_file_transfer(self):
        self.ftp.abort()

    def get_information_of_files(self):
        files = self.ftp.retrlines('LIST')
        return files

    def change_directory(self, directory):

        self.ftp.cwd(directory)

    def get_list_files(self):
        filenames = self.ftp.nlst()
        return filenames

    def download_file(self, file_name):
        with open(file_name, 'wb') as f:
            self.ftp.retrbinary('RETR ' + file_name, f.write)

    def upload_file(self, file_name, file_type):
        if file_type == 'text':
            with open(file_name) as fobj:
                self.ftp.storlines('STOR ' + file_name, fobj)
        else:
            with open(file_name, 'rb') as fobj:
                self.ftp.storbinary('STOR ' + file_name, fobj, 1024)
